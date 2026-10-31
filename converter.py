# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Kaido-MSVC
from __future__ import annotations

import math
import re
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import pymupdf
from PIL import Image

DPI_CHOICES = (150, 200, 300, 600)
MAX_PIXELS = 80_000_000


@dataclass(frozen=True)
class Settings:
    output: Path
    dpi: int = 200
    quality: int = 92

    def validate(self):
        if self.dpi not in DPI_CHOICES:
            raise ValueError('DPI 必須為 150、200、300 或 600。')
        if not 1 <= self.quality <= 100:
            raise ValueError('JPG 品質必須為 1–100。')


@dataclass
class Result:
    saved: int = 0
    completed: int = 0
    failed: int = 0
    cancelled: bool = False
    errors: list[str] = field(default_factory=list)
    folders: list[str] = field(default_factory=list)


def safe_stem(path: Path) -> str:
    # Truncate before stripping so the name never ends with a space or dot,
    # which Windows silently removes from folder and file names.
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', path.stem)[:80].strip(' .')
    if not name or re.fullmatch(r'(?i)(CON|PRN|AUX|NUL|COM[0-9]|LPT[0-9])', name):
        name = '_' + (name or 'PDF')
    return name


def new_folder(parent: Path, name: str) -> Path:
    for index in range(1, 100_001):
        candidate = parent / (name if index == 1 else f'{name} ({index})')
        try:
            candidate.mkdir()
            return candidate
        except FileExistsError:
            pass
    raise OSError('同名輸出資料夾過多，請更換輸出目錄。')


def save_page(page, target: Path, settings: Settings, cancel: threading.Event) -> bool:
    rect = page.rect
    width = math.ceil(rect.width * settings.dpi / 72)
    height = math.ceil(rect.height * settings.dpi / 72)
    if width <= 0 or height <= 0:
        raise ValueError('頁面尺寸無效。')
    if width * height > MAX_PIXELS:
        raise ValueError('頁面尺寸過大（超過 8,000 萬像素），請降低 DPI。')
    pixmap = page.get_pixmap(dpi=settings.dpi, colorspace=pymupdf.csRGB, alpha=False)
    if cancel.is_set():
        return False
    # Pillow explicitly embeds DPI and writes through Python's Unicode path support.
    with Image.frombytes('RGB', (pixmap.width, pixmap.height), pixmap.samples) as image:
        del pixmap
        if cancel.is_set():
            return False
        created = False
        try:
            with target.open('xb') as stream:
                created = True
                image.save(stream, format='JPEG', quality=settings.quality,
                           dpi=(settings.dpi, settings.dpi), optimize=True)
        except BaseException:
            if created:
                target.unlink(missing_ok=True)
            raise
    return True


def convert_batch(paths, settings: Settings, cancel: threading.Event,
                  emit: Callable[[dict], None] = lambda event: None,
                  password: Callable[[Path], str | None] = lambda path: None) -> Result:
    settings.validate()
    result = Result()
    settings.output.mkdir(parents=True, exist_ok=True)
    paths = list(dict.fromkeys(Path(p).resolve() for p in paths))
    for file_index, source in enumerate(paths):
        if cancel.is_set():
            break
        emit(dict(type='file', name=str(source), index=file_index + 1, total=len(paths)))
        folder = None
        try:
            if source.suffix.lower() != '.pdf':
                raise ValueError('僅接受 PDF 檔案。')
            with pymupdf.open(str(source)) as document:
                if not document.is_pdf:
                    raise ValueError('檔案內容不是 PDF。')
                if document.needs_pass:
                    secret = password(source)
                    if cancel.is_set():
                        break
                    if secret is None:
                        raise ValueError('已略過需要密碼的 PDF。')
                    authenticated = document.authenticate(secret)
                    secret = None
                    if not authenticated:
                        raise ValueError('PDF 密碼不正確，已略過此檔案。')
                if not document.page_count:
                    raise ValueError('PDF 沒有頁面。')
                folder = new_folder(settings.output, safe_stem(source))
                result.folders.append(str(folder))
                file_errors = 0
                page_count = document.page_count
                for page_index in range(page_count):
                    if cancel.is_set():
                        break
                    emit(dict(type='progress', file=file_index, files=len(paths),
                              page=page_index, pages=page_count, name=source.name))
                    try:
                        target = folder / f'{safe_stem(source)}_p{page_index + 1:04d}.jpg'
                        if save_page(document[page_index], target, settings, cancel):
                            result.saved += 1
                        else:
                            break
                    except Exception as exc:
                        file_errors += 1
                        message = f'{source.name} / 第 {page_index + 1} 頁：{exc}'
                        result.errors.append(message)
                        emit(dict(type='error', message=message))
                    emit(dict(type='progress', file=file_index, files=len(paths),
                              page=page_index + 1, pages=page_count, name=source.name))
                if not cancel.is_set():
                    if file_errors:
                        result.failed += 1
                    else:
                        result.completed += 1
        except Exception as exc:
            result.failed += 1
            message = f'{source.name}：{exc}'
            result.errors.append(message)
            emit(dict(type='error', message=message))
        finally:
            if folder is not None:
                try:
                    folder.rmdir()  # Only remove an empty directory created by this run.
                    result.folders.remove(str(folder))
                except OSError:
                    pass
        if not cancel.is_set():
            emit(dict(type='file_done', done=file_index + 1, total=len(paths)))
    result.cancelled = cancel.is_set()
    return result
