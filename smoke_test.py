# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Kaido-MSVC
"""Opt-in integration check of the actual GUI; also bundled for EXE verification."""
import ctypes
import json
import sys
import time
import traceback
from pathlib import Path
from tkinter import simpledialog

import pymupdf
from PIL import Image, ImageGrab


def attach_smoke_test(app, folder):
    folder = folder.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    report = {'frozen': bool(getattr(sys, 'frozen', False)), 'checks': [], 'passed': False}
    started = time.monotonic()
    sources = folder / '中文 日本語 來源'
    sources.mkdir(exist_ok=True)
    normal = sources / '中文 にほんご.pdf'
    encrypted = sources / '加密.pdf'
    broken = sources / '損壞.pdf'
    long_pdf = sources / '取消測試.pdf'
    def make(path, pages, locked=False):
        with pymupdf.open() as doc:
            for index in range(pages):
                page = doc.new_page(width=288, height=216)
                page.insert_text((25, 35), f'GUI smoke page {index + 1}', fontsize=18)
                page.draw_rect(pymupdf.Rect(25, 65, 180, 160), color=(0, .3, .8), fill=(0, .3, .8))
            options = dict(encryption=pymupdf.PDF_ENCRYPT_AES_256, user_pw='驗證pass', owner_pw='owner') if locked else {}
            doc.save(str(path), **options)
    make(normal, 2)
    make(encrypted, 1, True)
    make(long_pdf, 80)
    broken.write_bytes(b'%PDF-broken')
    original_prompt = simpledialog.askstring
    simpledialog.askstring = lambda *args, **kwargs: '驗證pass'
    app.output_var.set(str(folder / 'JPG 輸出'))
    errors = []
    state = {'phase': 'start', 'ticks': 0}

    def finish(error=None):
        simpledialog.askstring = original_prompt
        if error:
            report['error'] = error
        report['elapsed_seconds'] = round(time.monotonic() - started, 2)
        (folder / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
        app.destroy()

    def callback_error(kind, value, tb):
        errors.append(''.join(traceback.format_exception(kind, value, tb)))
        app.cancel_event.set()
        finish(errors[-1])
    app.report_callback_exception = callback_error

    def screenshot(name):
        app.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(app.winfo_id())
        ImageGrab.grab(window=hwnd).save(folder / name)
        report['checks'].append(name)

    def tick():
        try:
            assert time.monotonic() - started < 90, 'GUI check timed out'
            if state['phase'] == 'start':
                app.add_paths([normal, encrypted, broken, normal])
                assert len(app.files) == 3, 'duplicate file not filtered'
                app.tree.selection_set('2')
                app.remove_files()
                assert len(app.files) == 2
                app.add_paths([broken])
                app.theme.set('淺色')
                app.set_theme('淺色')
                report['checks'].append('add / deduplicate / remove / re-add')
                state['phase'] = 'light'
            elif state['phase'] == 'light':
                screenshot('light.png')
                app.start_button.invoke()
                assert app.busy
                assert app.start_button.cget('state') == 'disabled'
                state['phase'] = 'batch'
            elif state['phase'] == 'batch' and not app.busy:
                r = app.last_result
                assert r and (r.saved, r.completed, r.failed) == (3, 2, 1), repr(r)
                for path in (folder / 'JPG 輸出').rglob('*.jpg'):
                    with Image.open(path) as image:
                        image.load()
                        assert image.info['dpi'] == (200, 200)
                report['checks'].append('GUI batch + encrypted password + corrupt-file continuation + JPEG decode / DPI')
                app.set_theme('深色')
                app.theme.set('深色')
                state['phase'] = 'dark'
                state['dark_at'] = time.monotonic()
            elif state['phase'] == 'dark' and time.monotonic() - state['dark_at'] < 1.5:
                pass  # CustomTkinter redraws all widgets after a theme switch; let it finish.
            elif state['phase'] == 'dark':
                screenshot('dark.png')
                hwnd = ctypes.windll.user32.GetParent(app.winfo_id())
                native_icon = ctypes.windll.user32.SendMessageW(hwnd, 0x007F, 1, 0)
                assert native_icon, 'missing native window icon'
                report['checks'].append('window icon loaded')
                app.about_button.invoke()
                app.update()
                about = app.about_window
                assert about is not None and about.winfo_exists(), 'about window missing'
                about.update_idletasks()
                ImageGrab.grab(window=ctypes.windll.user32.GetParent(about.winfo_id())).save(folder / 'about.png')
                assert 'GNU AFFERO GENERAL PUBLIC LICENSE' in app.read_bundled('LICENSE')
                assert 'PyMuPDF' in app.read_bundled('THIRD-PARTY-NOTICES.md')
                third_party = app.read_third_party()
                for marker in ('licenses/CustomTkinter-6.0.0/LICENSE', 'Tom Schimansky',
                               'licenses/Pillow-13.0.0/LICENSE', 'licenses/darkdetect-0.8.0/LICENSE',
                               'licenses/Python-3.13.17/LICENSE.txt', 'licenses/Roboto/',
                               'licenses/MuPDF-1.28.5/thirdparty/freetype/FTL.TXT',
                               'licenses/MuPDF-1.28.5/fonts/noto/COPYING',
                               'Independent JPEG Group'):
                    assert marker in third_party, f'missing bundled license: {marker}'
                about.destroy()
                report['checks'].append('about window + bundled license texts')
                app.clear_files()
                app.add_paths([long_pdf])
                app.dpi.set('300')
                app.start_button.invoke()
                app.after(180, app.cancel_button.invoke)
                state['phase'] = 'cancel'
            elif state['phase'] == 'cancel' and not app.busy:
                assert app.last_result.cancelled, 'cancel button failed'
                assert app.last_result.saved < 80
                assert app.start_button.cget('state') == 'normal'
                report['checks'].append('cancel button + controls restored')
                app.clear_files()
                app.add_paths([normal])
                app.dpi.set('150')
                app.start_button.invoke()
                app.after(60, app.close_app)
                state['phase'] = 'close'
            elif state['phase'] == 'close':
                # The app closes itself after its worker has stopped. Capture report before destroy.
                return
            app.after(120, tick)
        except Exception:
            app.cancel_event.set()
            finish(traceback.format_exc())

    original_destroy = app.destroy
    def destroy():
        if state['phase'] == 'close':
            assert not app.busy, 'closed with active conversion'
            report['checks'].append('close during conversion waits for worker')
            report['passed'] = True
            report['elapsed_seconds'] = round(time.monotonic() - started, 2)
            simpledialog.askstring = original_prompt
            (folder / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf8')
        original_destroy()
    app.destroy = destroy
    app.after(500, tick)
