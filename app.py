# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Kaido-MSVC
from __future__ import annotations

import os
import queue
import sys
import threading
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

import customtkinter as ctk

from converter import DPI_CHOICES, Settings, convert_batch

VERSION = '1.0.0'
AUTHOR = 'Kaido-MSVC'
LICENSE_NAME = 'GNU AGPL-3.0-or-later'
BASE = Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))
HOME = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('PDF to JPG  •  v1.0')
        self.geometry('1000x850')
        self.minsize(880, 790)
        self.iconbitmap(str(BASE / 'assets' / 'app.ico'))
        self.configure(fg_color=('#F2F5FA', '#101722'))
        self.files: list[Path] = []
        self.events = queue.Queue()
        self.cancel_event = threading.Event()
        self.password_ready = threading.Event()
        self.password_value = None
        self.busy = False
        self.closing = False
        self.last_result = None
        self.active_output = None
        self.controls = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.font = 'Microsoft JhengHei UI'
        self.build_ui()
        self.protocol('WM_DELETE_WINDOW', self.close_app)
        self.after(80, self.poll_events)

    def label(self, parent, text, size=14, **kwargs):
        return ctk.CTkLabel(parent, text=text, font=(self.font, size), **kwargs)

    def button(self, parent, text, command, **kwargs):
        button = ctk.CTkButton(parent, text=text, command=command,
                               font=(self.font, 14), height=34, **kwargs)
        self.controls.append(button)
        return button

    def build_ui(self):
        header = ctk.CTkFrame(self, fg_color='transparent')
        header.grid(row=0, column=0, sticky='ew', padx=28, pady=(22, 14))
        header.grid_columnconfigure(0, weight=1)
        self.label(header, 'PDF → JPG', 29, anchor='w').grid(row=0, column=0, sticky='w')
        self.label(header, '逐頁轉換 · 批次處理 · 全程在本機執行', 13,
                   text_color=('#526176', '#A7B5CA')).grid(row=1, column=0, sticky='w')
        self.theme = ctk.CTkOptionMenu(header, values=['系統', '淺色', '深色'],
                                     command=self.set_theme, width=106, font=(self.font, 13))
        self.theme.grid(row=0, column=2, rowspan=2)
        self.theme.set('系統')
        self.about_button = ctk.CTkButton(header, text='關於', command=self.show_about, width=70,
                                          font=(self.font, 13), fg_color=('#536680', '#41516A'))
        self.about_button.grid(row=0, column=1, rowspan=2, padx=(0, 8))
        self.about_window = None

        card = ctk.CTkFrame(self, corner_radius=14)
        card.grid(row=1, column=0, padx=28, pady=(0, 12), sticky='nsew')
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=1)
        toolbar = ctk.CTkFrame(card, fg_color='transparent')
        toolbar.grid(row=0, column=0, sticky='ew', padx=18, pady=14)
        toolbar.grid_columnconfigure(0, weight=1)
        self.count_label = self.label(toolbar, '01  選擇 PDF  ·  0 個檔案', 16)
        self.count_label.grid(row=0, column=0, sticky='w')
        self.button(toolbar, '加入 PDF', self.add_files, width=112).grid(row=0, column=1, padx=(8, 0))
        self.button(toolbar, '移除選取', self.remove_files, width=105,
                    fg_color=('#536680', '#41516A')).grid(row=0, column=2, padx=(8, 0))
        self.button(toolbar, '清空', self.clear_files, width=70,
                    fg_color=('#536680', '#41516A')).grid(row=0, column=3, padx=(8, 0))
        table = ctk.CTkFrame(card, fg_color='transparent')
        table.grid(row=1, column=0, sticky='nsew', padx=18, pady=(0, 14))
        table.grid_columnconfigure(0, weight=1)
        table.grid_rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(table, columns=('name', 'path'), show='headings', height=6,
                                 selectmode='extended', style='PDF.Treeview')
        self.tree.heading('name', text='檔案名稱')
        self.tree.heading('path', text='來源路徑')
        self.tree.column('name', width=250, minwidth=140)
        self.tree.column('path', width=550, minwidth=200)
        self.tree.grid(row=0, column=0, sticky='nsew')
        scroll = ttk.Scrollbar(table, command=self.tree.yview)
        scroll.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=scroll.set)
        horizontal = ttk.Scrollbar(table, orient='horizontal', command=self.tree.xview)
        horizontal.grid(row=1, column=0, sticky='ew')
        self.tree.configure(xscrollcommand=horizontal.set)

        settings = ctk.CTkFrame(self, corner_radius=14)
        settings.grid(row=2, column=0, sticky='ew', padx=28, pady=(0, 12))
        settings.grid_columnconfigure(1, weight=1)
        self.label(settings, '02  輸出設定', 16).grid(row=0, column=0, sticky='w', padx=18, pady=(12, 8))
        self.label(settings, '輸出目錄').grid(row=1, column=0, sticky='w', padx=18)
        self.output_var = ctk.StringVar(value=str(HOME / 'JPG輸出'))
        self.output_entry = ctk.CTkEntry(settings, textvariable=self.output_var,
                                        font=(self.font, 13), height=34)
        self.output_entry.grid(row=1, column=1, sticky='ew', pady=4)
        self.controls.append(self.output_entry)
        self.button(settings, '瀏覽…', self.choose_output, width=90).grid(row=1, column=2, padx=18)
        options = ctk.CTkFrame(settings, fg_color='transparent')
        options.grid(row=2, column=0, columnspan=3, sticky='ew', padx=18, pady=10)
        self.label(options, '解析度 DPI').pack(side='left', padx=(0, 12))
        self.dpi = ctk.CTkSegmentedButton(options, values=[str(x) for x in DPI_CHOICES],
                                         font=(self.font, 13))
        self.dpi.set('200')
        self.dpi.pack(side='left')
        self.controls.append(self.dpi)
        self.label(options, 'JPG 品質').pack(side='left', padx=(28, 10))
        self.quality_label = self.label(options, '92', 14, width=32)
        self.quality_label.pack(side='right')
        self.quality = ctk.CTkSlider(options, from_=1, to=100, number_of_steps=99,
                                    command=lambda value: self.quality_label.configure(text=str(round(value))),
                                    width=180)
        self.quality.set(92)
        self.quality.pack(side='left', fill='x', expand=True)
        self.controls.append(self.quality)
        self.label(settings, '每份 PDF 建立獨立資料夾；同名自動編號。600 DPI 需要較多時間與記憶體。',
                   12, text_color=('#526176', '#A7B5CA')).grid(row=3, column=0, columnspan=3,
                                                            sticky='w', padx=18, pady=(0, 12))

        progress = ctk.CTkFrame(self, corner_radius=14)
        progress.grid(row=3, column=0, sticky='ew', padx=28, pady=(0, 12))
        progress.grid_columnconfigure(0, weight=1)
        self.status = self.label(progress, '準備就緒', 15, anchor='w')
        self.status.grid(row=0, column=0, sticky='ew', padx=18, pady=(12, 6))
        self.progress = ctk.CTkProgressBar(progress)
        self.progress.set(0)
        self.progress.grid(row=1, column=0, sticky='ew', padx=18, pady=(0, 6))
        self.detail = self.label(progress, '加入 PDF 後，按「開始轉換」。可按住 Ctrl / Shift 選取多檔。', 12, anchor='w')
        self.detail.grid(row=2, column=0, sticky='ew', padx=18, pady=(0, 4))
        self.log = ctk.CTkTextbox(progress, height=86, font=(self.font, 12), wrap='word')
        self.log.grid(row=3, column=0, sticky='ew', padx=18, pady=(0, 14))
        self.log.configure(state='disabled')

        footer = ctk.CTkFrame(self, fg_color='transparent')
        footer.grid(row=4, column=0, sticky='ew', padx=28, pady=(0, 20))
        footer.grid_columnconfigure(0, weight=1)
        self.open_button = ctk.CTkButton(footer, text='開啟輸出目錄', command=self.open_output,
                                        font=(self.font, 14), fg_color=('#536680', '#41516A'), height=40)
        self.open_button.grid(row=0, column=0, sticky='w')
        self.cancel_button = ctk.CTkButton(footer, text='取消', command=self.cancel_job,
                                          font=(self.font, 14), width=110, height=40, state='disabled',
                                          fg_color='#A44343', hover_color='#813333')
        self.cancel_button.grid(row=0, column=1, padx=12)
        self.start_button = self.button(footer, '開始轉換', self.start_job, width=160)
        self.start_button.configure(height=40)
        self.start_button.grid(row=0, column=2)
        self.apply_table_theme()

    def set_theme(self, value):
        ctk.set_appearance_mode({'系統': 'System', '淺色': 'Light', '深色': 'Dark'}[value])
        self.apply_table_theme()

    def apply_table_theme(self):
        dark = ctk.get_appearance_mode() == 'Dark'
        style = ttk.Style(self)
        style.theme_use('clam')
        bg, fg = ('#202B3B', '#E3EAF5') if dark else ('#FFFFFF', '#203049')
        style.configure('PDF.Treeview', background=bg, fieldbackground=bg, foreground=fg,
                        font=(self.font, 11), rowheight=32, borderwidth=0)
        style.configure('PDF.Treeview.Heading', font=(self.font, 11),
                        background='#334258' if dark else '#E6EDF7', foreground=fg)
        style.map('PDF.Treeview', background=[('selected', '#176BCE')],
                   foreground=[('selected', '#FFFFFF')])

    def add_files(self):
        if self.busy:
            return
        selected = filedialog.askopenfilenames(parent=self, title='選擇一份或多份 PDF',
                                               filetypes=[('PDF 檔案', '*.pdf *.PDF')])
        self.add_paths(selected)

    def add_paths(self, paths):
        for value in paths:
            path = Path(value).resolve()
            if path.suffix.lower() == '.pdf' and path not in self.files:
                self.files.append(path)
        self.refresh_files()

    def refresh_files(self):
        self.tree.delete(*self.tree.get_children())
        for index, path in enumerate(self.files):
            self.tree.insert('', 'end', iid=str(index), values=(path.name, str(path.parent)))
        self.count_label.configure(text=f'01  選擇 PDF  ·  {len(self.files)} 個檔案')

    def remove_files(self):
        if not self.busy:
            selected = {int(x) for x in self.tree.selection()}
            self.files = [p for i, p in enumerate(self.files) if i not in selected]
            self.refresh_files()

    def clear_files(self):
        if not self.busy:
            self.files.clear()
            self.refresh_files()

    def choose_output(self):
        path = filedialog.askdirectory(parent=self, title='選擇 JPG 輸出目錄')
        if path:
            self.output_var.set(path)

    def append_log(self, message):
        self.log.configure(state='normal')
        self.log.insert('end', message + '\n')
        # Bound UI log size; complete errors remain available in Result.
        if int(self.log.index('end-1c').split('.')[0]) > 2000:
            self.log.delete('1.0', '500.0')
        self.log.see('end')
        self.log.configure(state='disabled')

    def start_job(self):
        if self.busy:
            return
        if not self.files:
            messagebox.showinfo('尚未選擇 PDF', '請先加入一份或多份 PDF。', parent=self)
            return
        try:
            text = self.output_var.get().strip()
            if not text:
                raise ValueError('請指定輸出目錄。')
            output = Path(text).expanduser().resolve()
            settings = Settings(output, int(self.dpi.get()), round(self.quality.get()))
            settings.validate()
            if output.exists() and not output.is_dir():
                raise ValueError('輸出位置是檔案，請改選資料夾。')
        except Exception as exc:
            messagebox.showerror('設定錯誤', str(exc), parent=self)
            return
        self.busy = True
        self.last_result = None
        self.active_output = output
        self.cancel_event.clear()
        self.password_ready.clear()
        self.progress.set(0)
        self.status.configure(text='正在準備轉換…')
        self.append_log(f'開始：{settings.dpi} DPI / 品質 {settings.quality} / {output}')
        for control in self.controls:
            control.configure(state='disabled')
        self.cancel_button.configure(state='normal')
        threading.Thread(target=self.worker, args=(tuple(self.files), settings), daemon=True).start()

    def request_password(self, path):
        self.password_ready.clear()
        self.password_value = None
        self.events.put(dict(type='password', path=str(path)))
        while not self.password_ready.wait(0.1):
            if self.cancel_event.is_set():
                return None
        value = self.password_value
        self.password_value = None
        return value

    def worker(self, paths, settings):
        try:
            result = convert_batch(paths, settings, self.cancel_event, self.events.put, self.request_password)
            self.events.put(dict(type='done', result=result))
        except Exception as exc:
            self.events.put(dict(type='fatal', message=str(exc)))

    def poll_events(self):
        try:
            for _ in range(150):
                event = self.events.get_nowait()
                kind = event['type']
                if kind == 'password':
                    if not self.cancel_event.is_set():
                        self.password_value = simpledialog.askstring('PDF 密碼',
                            f'{Path(event["path"]).name}\n請輸入開啟密碼；取消將略過此檔案。',
                            parent=self, show='*')
                    self.password_ready.set()
                elif kind == 'file':
                    self.status.configure(text=f'處理第 {event["index"]} / {event["total"]} 份 PDF')
                    self.append_log(f'處理：{event["name"]}')
                elif kind == 'progress':
                    fraction = (event['file'] + event['page'] / event['pages']) / event['files']
                    self.progress.set(fraction)
                    self.detail.configure(text=f'{event["name"][:64]}  ·  第 {event["page"]} / {event["pages"]} 頁')
                elif kind == 'file_done':
                    self.progress.set(event['done'] / event['total'])
                elif kind == 'error':
                    self.append_log('錯誤：' + event['message'])
                elif kind in ('done', 'fatal'):
                    self.finish_job(event)
        except queue.Empty:
            pass
        if self.closing and not self.busy:
            self.destroy()
            return
        self.after(80, self.poll_events)

    def finish_job(self, event):
        self.busy = False
        self.password_value = None
        for control in self.controls:
            control.configure(state='normal')
        self.cancel_button.configure(state='disabled')
        if event['type'] == 'fatal':
            self.status.configure(text='轉換失敗')
            self.detail.configure(text='請查看下方錯誤，確認輸出目錄可寫入。')
            self.append_log('無法執行：' + event['message'])
        else:
            result = self.last_result = event['result']
            state = '已取消' if result.cancelled else ('完成，部分檔案有錯誤' if result.failed else '轉換完成')
            self.status.configure(text=f'{state}  ·  已輸出 {result.saved} 張 JPG')
            self.detail.configure(text=f'完整成功 {result.completed} 份 / 有錯誤或略過 {result.failed} 份；已完成的 JPG 會保留。')
            self.append_log(f'{state}：成功 {result.completed} 份，有錯誤 {result.failed} 份，{result.saved} 張 JPG。')
            if not result.cancelled:
                self.progress.set(1)

    def cancel_job(self):
        if self.busy:
            self.cancel_event.set()
            self.cancel_button.configure(state='disabled')
            self.status.configure(text='正在取消…目前頁面處理結束後停止')
            self.append_log('要求取消；已完成的 JPG 將保留。')

    def close_app(self):
        if self.busy:
            self.closing = True
            self.cancel_job()
        else:
            self.destroy()

    def show_about(self):
        if self.about_window is not None and self.about_window.winfo_exists():
            self.about_window.focus()
            return
        window = self.about_window = ctk.CTkToplevel(self)
        window.title('關於 PDF to JPG')
        window.geometry('720x560')
        window.minsize(560, 420)
        window.transient(self)
        # CTkToplevel resets its icon shortly after creation; set ours afterwards.
        window.after(250, lambda: window.iconbitmap(str(BASE / 'assets' / 'app.ico')))
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)
        tabs = ctk.CTkTabview(window)
        tabs.grid(row=0, column=0, sticky='nsew', padx=16, pady=(8, 0))
        about = (f'PDF to JPG  v{VERSION}\n'
                 f'Copyright (C) 2026 {AUTHOR}\n\n'
                 f'本程式為自由軟體，依 {LICENSE_NAME}（GNU Affero 通用公共授權條款第 3 版或更新版本）'
                 '釋出；您可以依該授權條款重新散布或修改本程式。\n\n'
                 '本程式不提供任何擔保，亦不含適售性或特定用途適用性之默示擔保。'
                 '詳見「授權全文」分頁。\n\n'
                 '取得本程式時，您有權一併取得對應的完整原始碼。散布者應在提供本 EXE 的同一位置'
                 '一併提供下列檔案：\n'
                 f'・PDF-to-JPG-{VERSION}-source.zip：本程式原始碼、資源、授權檔、建置腳本與鎖定版本清單\n'
                 '・pymupdf-2.0.tar.gz：PyMuPDF 2.0 官方原始碼\n'
                 '・mupdf-1.28.5-source.tar.gz：MuPDF 1.28.5 官方原始碼（含 thirdparty）\n'
                 '・SHA256SUMS.txt：上列檔案與 EXE 的 SHA-256\n'
                 '若未一併取得，請向提供 EXE 給您的散布者索取。\n\n'
                 '本程式內含 PyMuPDF / MuPDF（AGPL-3.0）、Pillow、CustomTkinter（含 Roboto 字型）、'
                 'darkdetect、NumPy、packaging、psutil、PyYAML、Python、Tcl/Tk 與 '
                 'PyInstaller bootloader，清單見「第三方元件」分頁，'
                 '各元件授權全文附於該分頁下方及原始碼包的 licenses 資料夾。')
        for name, text in (('關於', about),
                           ('授權全文', self.read_bundled('LICENSE')),
                           ('第三方元件', self.read_third_party())):
            tab = tabs.add(name)
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1)
            box = ctk.CTkTextbox(tab, font=(self.font if name != '授權全文' else 'Consolas', 12),
                                 wrap='word')
            box.grid(row=0, column=0, sticky='nsew')
            box.insert('1.0', text)
            box.configure(state='disabled')
        ctk.CTkButton(window, text='關閉', command=window.destroy, width=100,
                      font=(self.font, 14)).grid(row=1, column=0, sticky='e', padx=16, pady=12)
        window.after(50, window.focus)

    @staticmethod
    def read_bundled(name):
        try:
            return (BASE / name).read_text(encoding='utf8')
        except OSError as exc:
            return f'找不到 {name}：{exc}\n授權為 {LICENSE_NAME}，全文見 https://www.gnu.org/licenses/agpl-3.0.html'

    @classmethod
    def read_third_party(cls):
        parts = [cls.read_bundled('THIRD-PARTY-NOTICES.md')]
        root = BASE / 'licenses'
        files = sorted(p for p in root.rglob('*') if p.is_file()) if root.is_dir() else []
        if not files:
            parts.append(f'找不到隨附的授權全文資料夾：{root}')
        for path in files:
            rel = path.relative_to(root).as_posix()
            try:
                text = path.read_text(encoding='utf8', errors='replace')
            except OSError as exc:
                text = f'無法讀取：{exc}'
            parts.append(f'{"=" * 72}\nlicenses/{rel}\n{"=" * 72}\n{text}')
        return '\n\n'.join(parts)

    def open_output(self):
        try:
            # Follow the current entry so a newly chosen folder opens, not the previous run's.
            output = Path(self.output_var.get().strip()).expanduser().resolve()
            if not output.is_dir():
                raise ValueError('輸出資料夾尚未建立，請先轉換或選擇現有資料夾。')
            os.startfile(str(output))
        except Exception as exc:
            messagebox.showerror('無法開啟目錄', str(exc), parent=self)


def main():
    ctk.set_default_color_theme('blue')
    ctk.set_appearance_mode('System')
    app = App()
    if len(sys.argv) == 3 and sys.argv[1] == '--smoke-test':
        from smoke_test import attach_smoke_test
        attach_smoke_test(app, Path(sys.argv[2]))
    app.mainloop()


if __name__ == '__main__':
    main()
