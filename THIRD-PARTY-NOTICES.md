# 第三方元件授權聲明

PDF to JPG 由 Kaido-MSVC 以 GNU AGPL-3.0-or-later 釋出（見 `LICENSE`）。
本專案的授權標示只適用於 Kaido-MSVC 撰寫的部分，不改變下列第三方元件各自的授權。

單一 EXE 內含下列第三方元件。各元件完整的著作權聲明與授權全文，
已原樣收錄於 EXE 內及原始碼包的 `licenses\` 資料夾（由 `collect_licenses.py` 從建置環境複製）：

| 元件 | 版本 | 授權 | 完整授權文字 | 網址 |
|---|---|---|---|---|
| PyMuPDF / MuPDF | 2.0 / MuPDF 1.28.5 | GNU AGPL-3.0（或 Artifex 商業授權） | `licenses\PyMuPDF-2.0\COPYING`；AGPL 全文見 `LICENSE`；MuPDF 內建元件見下節 | https://github.com/pymupdf/PyMuPDF |
| Pillow | 13.0.0 | MIT-CMU（HPND）；內含函式庫另列於同檔 | `licenses\Pillow-13.0.0\LICENSE` | https://github.com/python-pillow/Pillow |
| CustomTkinter | 6.0.0 | MIT（套件附帶 LICENSE 為 MIT；套件資訊欄寫 CC0，以 LICENSE 檔為準） | `licenses\CustomTkinter-6.0.0\LICENSE` | https://github.com/TomSchimansky/CustomTkinter |
| Roboto 字型（隨 CustomTkinter） | 2.137 | Apache-2.0（字型內嵌授權資訊） | `licenses\Roboto\LICENSE-Apache-2.0.txt` | https://fonts.google.com/specimen/Roboto |
| darkdetect | 0.8.0 | BSD-3-Clause | `licenses\darkdetect-0.8.0\LICENSE` | https://github.com/albertosottile/darkdetect |
| NumPy（含 OpenBLAS 等內附元件） | 2.5.4 | BSD-3-Clause 等，見各檔 | `licenses\NumPy-2.5.4\` | https://github.com/numpy/numpy |
| packaging | 26.3 | Apache-2.0 或 BSD-2-Clause | `licenses\packaging-26.3\` | https://github.com/pypa/packaging |
| psutil | 7.2.2 | BSD-3-Clause | `licenses\psutil-7.2.2\LICENSE` | https://github.com/giampaolo/psutil |
| PyYAML | 6.0.3 | MIT | `licenses\PyYAML-6.0.3\LICENSE` | https://github.com/yaml/pyyaml |
| Python（含 OpenSSL、libffi、bzip2、zlib 等內附函式庫及 MSVC 執行階段條款） | 3.13.17 | PSF License 及檔內所列各授權 | `licenses\Python-3.13.17\LICENSE.txt` | https://www.python.org/ |
| Microsoft Visual C++ 執行階段（`VCRUNTIME140.dll`、`VCRUNTIME140_1.dll` 隨 Python；`MSVCP140.dll` 供 PyMuPDF 使用） | 14.x；`MSVCP140.dll` 為 14.51.36231 | Microsoft 專有軟體，屬 Microsoft Distributable Code，**不適用 AGPL**；接收者條款見下節 | 下節；`licenses\Python-3.13.17\LICENSE.txt` 的 “Additional Conditions for this Windows binary build” | https://learn.microsoft.com/cpp/windows/redistributing-visual-cpp-files |
| Tcl/Tk | 8.6 | Tcl/Tk License（BSD 類） | `licenses\Tcl-Tk-8.6\license.terms` | https://www.tcl-lang.org/ |
| PyInstaller bootloader | 6.22.3 | GPL-2.0-or-later，附 bootloader 例外 | `licenses\PyInstaller-6.22.3\COPYING.txt` | https://pyinstaller.org/ |

## MuPDF 1.28.5 內建元件

PyMuPDF 2.0 的 `mupdfcpp64.dll` 依 MuPDF 1.28.5 的 Windows 建置專案編入下列函式庫與資源。
授權全文由 MuPDF 1.28.5 官方原始碼及其固定的 submodule commit 原樣複製到
`licenses\MuPDF-1.28.5\`，來源網址與 SHA-256 見該資料夾的 `PROVENANCE.md`。
curl、freeglut、OpenSSL 未編入，故未列出。

| 元件 | 授權 | 完整授權文字（`licenses\MuPDF-1.28.5\` 下） |
|---|---|---|
| MuPDF（含 sRGB / sGray ICC 描述檔） | AGPL-3.0-or-later，Copyright (c) 2006-2026 Artifex Software, Inc. | `COPYING`、`README` |
| jbig2dec | AGPL-3.0-or-later | `thirdparty\jbig2dec\LICENSE`（全文同 `COPYING`） |
| extract | AGPL-3.0-or-later | 全文同 `COPYING` |
| FreeType 2.14.3 | FreeType License（FTL；FreeType 為 FTL / GPLv2 雙授權，本程式選用 FTL） | `thirdparty\freetype\LICENSE.TXT`、`FTL.TXT` |
| HarfBuzz | Old MIT | `thirdparty\harfbuzz\COPYING` |
| libjpeg（IJG） | IJG License | `thirdparty\libjpeg\README` |
| OpenJPEG | BSD-2-Clause | `thirdparty\openjpeg\LICENSE` |
| Little CMS（lcms2mt） | MIT | `thirdparty\lcms2\LICENSE` |
| zlib | zlib License | `thirdparty\zlib\LICENSE` |
| Brotli | MIT | `thirdparty\brotli\LICENSE` |
| MuJS | ISC | `thirdparty\mujs\COPYING` |
| Gumbo | Apache-2.0 | `thirdparty\gumbo-parser\COPYING` |
| cmark-gfm | BSD-2-Clause 等，見檔 | `thirdparty\cmark-gfm\COPYING` |
| Tesseract | Apache-2.0 | `thirdparty\tesseract\LICENSE` |
| Leptonica | BSD-2-Clause | `thirdparty\leptonica\leptonica-license.txt` |
| ZXing-C++ | Apache-2.0 | `thirdparty\zxing-cpp\LICENSE` |
| Zint | BSD-3-Clause | `thirdparty\zint\LICENSE` |
| URW Nimbus / Dingbats / Standard Symbols 字型 | SIL OFL-1.1 | `fonts\urw\OFL.txt` |
| Noto 字型 | SIL OFL-1.1 | `fonts\noto\COPYING` |
| Source Han Serif 1.001 | SIL OFL-1.1 | `fonts\han\LICENSE.txt` |
| Charis SIL（MuPDF 簡化版） | SIL OFL-1.1 | `fonts\sil\OFL.txt`、`README.txt` |
| Droid Sans Fallback | Apache-2.0 | `fonts\droid\NOTICE` |
| 斷字樣式（tex-hyphen CTAN-2025.06.02，48 種語言） | 各語言不同，見各檔 | `hyphen\license\hyph-*.info` |
| Adobe CMap 與 PDF 對應資源 | BSD-3-Clause，Copyright Adobe | `cmaps\` |

依各授權要求的聲明：

- Portions of this software are copyright © 1996-2026 The FreeType Project (https://freetype.org). All rights reserved.
- This software is based in part on the work of the Independent JPEG Group.

## Microsoft Visual C++ 執行階段使用條款

EXE 內含的 `MSVCP140.dll` 取自 Microsoft Visual Studio Community 2026（穩定通道）的
`VC\Redist\MSVC\14.51.36231\x64\Microsoft.VC145.CRT`，未經修改，依
Microsoft Software License Terms for Visual Studio Community 2026 第 5 節 “DISTRIBUTABLE CODE”
及其 Distributable List（https://aka.ms/vs/18/redistribution）隨本程式散布。
`VCRUNTIME140.dll`、`VCRUNTIME140_1.dll` 隨 Python 3.13 官方 Windows 版附帶，同屬 Microsoft Distributable Code。

這些檔案（下稱「Microsoft 執行階段檔案」）的著作權屬於 Microsoft Corporation，
不屬於本程式作者，也不在本程式 AGPL-3.0-or-later 授權範圍內；AGPL 賦予的修改與散布權利不及於這些檔案。
使用、複製或轉發本程式，即表示你同意下列條款：

1. Microsoft 執行階段檔案只能作為本程式的一部分使用，不得單獨抽出散布或用於其他用途。
2. 不得修改 Microsoft 執行階段檔案，也不得進行反向工程、解編譯或反組譯，但適用法律明確允許者不在此限。
3. Microsoft 執行階段檔案「依現狀」提供。Microsoft 不提供任何明示或默示擔保，
   對於因使用所生的任何損害不負責任，亦不提供技術支援。
4. 本程式並非由 Microsoft 製作或背書。
5. 若你轉發本程式，必須連同本檔案一起提供，並要求你的接收者同意本節條款。

English version: The Microsoft Visual C++ runtime files included in this program
(`MSVCP140.dll`, `VCRUNTIME140.dll`, `VCRUNTIME140_1.dll`) are Microsoft Distributable Code,
copyright Microsoft Corporation, and are not covered by this program's AGPL license.
By using, copying or redistributing this program you agree that: (1) you use them only as part of
this program; (2) you do not modify, reverse engineer, decompile or disassemble them, except to the
extent applicable law expressly permits; (3) they are provided "as is" without warranties or support
from Microsoft, and Microsoft is not liable for any damages; (4) this program is not made or endorsed
by Microsoft; and (5) if you redistribute this program, you include this notice and require your
recipients to agree to these terms.

## 原始碼

因 PyMuPDF 採 AGPL-3.0，本程式整體也以 AGPL-3.0-or-later 釋出。
散布者應在提供 EXE 的同一位置一併提供下列三個檔案（SHA-256 列於隨附的 `SHA256SUMS.txt`）：

| 檔案 | 內容 | 官方來源 |
|---|---|---|
| `PDF-to-JPG-1.0.0-source.zip` | 本程式原始碼、資源、授權檔、建置腳本與鎖定版本清單 | 本專案 |
| `pymupdf-2.0.tar.gz` | PyMuPDF 2.0 原始碼（官方 sdist，未修改） | https://pypi.org/project/pymupdf/2.0/#files |
| `mupdf-1.28.5-source.tar.gz` | MuPDF 1.28.5 及其 thirdparty 原始碼（官方原始碼包，未修改；PyMuPDF 2.0 建置時使用此檔） | https://github.com/ArtifexSoftware/mupdf-downloads/releases/tag/1.28.5 |

其他非 copyleft 第三方元件的原始碼可依 `requirements-lock.txt` 的版本由上表網址或 PyPI 取得。
