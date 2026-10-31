# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Kaido-MSVC
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

import pymupdf
from PIL import Image

from converter import Settings, convert_batch, save_page

ROOT = Path(__file__).resolve().parents[1]


def pdf(path, pages=2, encrypted=False, rotated=False, size=(144, 72)):
    path.parent.mkdir(parents=True, exist_ok=True)
    with pymupdf.open() as doc:
        for index in range(pages):
            page = doc.new_page(width=size[0], height=size[1])
            page.draw_rect(pymupdf.Rect(5, 5, 40, 40), color=(1, 0, 0), fill=(1, 0, 0))
            page.insert_text((45, 35), f'Page {index + 1}', fontsize=10)
            if rotated:
                page.set_rotation(90)
        kwargs = dict(encryption=pymupdf.PDF_ENCRYPT_AES_256,
                      owner_pw='owner-secret', user_pw='test-secret') if encrypted else {}
        doc.save(str(path), **kwargs)
    return path


class ConversionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / 'work', prefix='test-')
        self.root = Path(self.temp.name)
        self.out = self.root / '輸出 日本語'
        self.cancel = threading.Event()

    def tearDown(self):
        self.temp.cleanup()

    def convert(self, paths, dpi=200, quality=92, **kwargs):
        return convert_batch(paths, Settings(self.out, dpi, quality), self.cancel, **kwargs)

    def test_all_dpi_unicode_rotation_rgb_and_metadata(self):
        source = pdf(self.root / '中文 日本語' / '測試.PDF', rotated=True)
        for dpi in (150, 200, 300, 600):
            with self.subTest(dpi=dpi):
                result = self.convert([source], dpi)
                self.assertEqual((result.saved, result.completed, result.failed), (2, 1, 0))
                files = sorted(Path(result.folders[0]).glob('*.jpg'))
                self.assertEqual(len(files), 2)
                with Image.open(files[0]) as image:
                    self.assertEqual(image.size, (dpi, dpi * 2))
                    self.assertEqual(image.mode, 'RGB')
                    self.assertEqual(image.info['dpi'], (dpi, dpi))
                    self.assertGreater(min(image.getpixel((5, 5))), 240)
                    self.assertTrue(any(lo < 200 for lo, hi in image.getextrema()))
                    image.load()

    def test_same_names_repeat_runs_and_duplicate_input(self):
        a = pdf(self.root / 'a' / '同名.pdf', pages=1)
        b = pdf(self.root / 'b' / '同名.pdf', pages=1)
        first = self.convert([a, a, b])
        self.assertEqual(first.saved, 2)
        original = {p: p.read_bytes() for p in self.out.rglob('*.jpg')}
        second = self.convert([a, b])
        self.assertEqual(second.saved, 2)
        self.assertEqual(len(list(self.out.glob('*'))), 4)
        for path, content in original.items():
            self.assertEqual(path.read_bytes(), content)

    def test_encryption_correct_wrong_and_skipped(self):
        encrypted = pdf(self.root / '有密碼.pdf', pages=1, encrypted=True)
        for secret, saved in [('test-secret', 1), ('wrong', 0), (None, 0)]:
            with self.subTest(secret=secret):
                result = self.convert([encrypted], password=lambda p: secret)
                self.assertEqual(result.saved, saved)
                self.assertEqual(result.failed, 0 if saved else 1)
                self.assertNotIn('test-secret', '\n'.join(result.errors))

    def test_corrupt_missing_and_non_pdf_continue_batch(self):
        bad = self.root / '損壞.pdf'
        bad.write_bytes(b'%PDF-broken')
        disguised = self.root / 'fake.pdf'
        Image.new('RGB', (10, 10)).save(disguised, format='PNG')
        good = pdf(self.root / '正常.pdf', pages=1)
        result = self.convert([bad, self.root / 'missing.pdf', disguised, good])
        self.assertEqual((result.saved, result.failed, result.completed), (1, 3, 1))

    def test_cancel_before_and_between_pages_preserves_completed(self):
        source = pdf(self.root / 'cancel.pdf', pages=5)
        self.cancel.set()
        result = self.convert([source])
        self.assertTrue(result.cancelled)
        self.assertEqual(result.saved, 0)
        self.cancel.clear()
        events = []
        def emit(event):
            events.append(event)
            if event['type'] == 'progress' and event['page'] == 1:
                self.cancel.set()
        result = self.convert([source], emit=emit)
        self.assertTrue(result.cancelled)
        self.assertEqual(result.saved, 1)
        self.assertEqual(len(list(self.out.rglob('*.jpg'))), 1)
        self.assertEqual(result.completed, 0)
        self.assertFalse(any(e['type'] == 'file_done' for e in events))

    def test_no_overwrite_even_direct_collision(self):
        source = pdf(self.root / 'source.pdf', pages=1)
        target = self.root / 'exists.jpg'
        target.write_bytes(b'original')
        with pymupdf.open(source) as doc:
            with self.assertRaises(FileExistsError):
                save_page(doc[0], target, Settings(self.out), self.cancel)
        self.assertEqual(target.read_bytes(), b'original')

    def test_encoding_write_failure_removes_partial_image(self):
        source = pdf(self.root / 'source.pdf', pages=1)
        def fail(image, stream, **kwargs):
            stream.write(b'partial')
            raise OSError('simulated disk full')
        with patch('PIL.Image.Image.save', fail):
            result = self.convert([source])
        self.assertEqual(result.failed, 1)
        self.assertEqual(result.saved, 0)
        self.assertEqual(list(self.out.rglob('*.jpg')), [])
        self.assertEqual(list(self.out.iterdir()), [])

    def test_page_error_continues_later_pages_and_files(self):
        a = pdf(self.root / 'first.pdf', pages=3)
        b = pdf(self.root / 'second.pdf', pages=1)
        original = save_page
        calls = 0
        def fail_one(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError('simulated page error')
            return original(*args, **kwargs)
        with patch('converter.save_page', fail_one):
            result = self.convert([a, b])
        self.assertEqual((result.saved, result.completed, result.failed), (3, 1, 1))

    def test_safe_stem_never_ends_with_space_or_dot(self):
        from converter import safe_stem
        name = safe_stem(Path('a' * 79 + ' tail.pdf'))
        self.assertEqual(name, 'a' * 79)
        self.assertEqual(safe_stem(Path('CON.pdf')), '_CON')
        self.assertEqual(safe_stem(Path('... .pdf')), '_PDF')

    def test_output_is_file_and_invalid_settings(self):
        source = pdf(self.root / 'source.pdf', pages=1)
        self.out.write_text('not a directory', encoding='utf8')
        with self.assertRaises(FileExistsError):
            self.convert([source])
        for dpi, quality in [(72, 92), (200, 0), (200, 101)]:
            with self.assertRaises(ValueError):
                Settings(self.out, dpi, quality).validate()

    def test_large_page_guard_and_quality_changes_encoding(self):
        huge = pdf(self.root / 'huge.pdf', pages=1, size=(14400, 14400))
        result = self.convert([huge], dpi=600)
        self.assertEqual(result.failed, 1)
        self.assertIn('8,000', result.errors[0])
        source = pdf(self.root / 'quality.pdf', pages=1)
        low = self.convert([source], quality=15)
        high = self.convert([source], quality=98)
        with Image.open(next(Path(low.folders[0]).glob('*.jpg'))) as a, \
             Image.open(next(Path(high.folders[0]).glob('*.jpg'))) as b:
            self.assertNotEqual(a.quantization, b.quantization)


if __name__ == '__main__':
    unittest.main(verbosity=2)
