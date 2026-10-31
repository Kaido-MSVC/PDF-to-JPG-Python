# 第三方元件授權聲明

PDF to JPG 由 Kaido-MSVC 以 GNU AGPL-3.0-or-later 釋出（見 `LICENSE`）。
本專案的授權標示只適用於 Kaido-MSVC 撰寫的部分，不改變下列第三方元件各自的授權。

單一 EXE 內含下列第三方元件。各元件完整的著作權聲明與授權全文，
已原樣收錄於 EXE 內及原始碼包的 `licenses\` 資料夾（由 `collect_licenses.py` 從建置環境複製）：

| 元件 | 版本 | 授權 | 完整授權文字 | 網址 |
|---|---|---|---|---|
| PyMuPDF / MuPDF | 2.0 / MuPDF 1.28.5 | GNU AGPL-3.0（或 Artifex 商業授權） | `licenses\PyMuPDF-2.0\COPYING`；AGPL 全文見 `LICENSE` | https://github.com/pymupdf/PyMuPDF |
| Pillow | 13.0.0 | MIT-CMU（HPND）；內含函式庫另列於同檔 | `licenses\Pillow-13.0.0\LICENSE` | https://github.com/python-pillow/Pillow |
| CustomTkinter | 6.0.0 | MIT（套件附帶 LICENSE 為 MIT；套件資訊欄寫 CC0，以 LICENSE 檔為準） | `licenses\CustomTkinter-6.0.0\LICENSE` | https://github.com/TomSchimansky/CustomTkinter |
| Roboto 字型（隨 CustomTkinter） | 2.137 | Apache-2.0（字型內嵌授權資訊） | `licenses\Roboto\LICENSE-Apache-2.0.txt` | https://fonts.google.com/specimen/Roboto |
| darkdetect | 0.8.0 | BSD-3-Clause | `licenses\darkdetect-0.8.0\LICENSE` | https://github.com/albertosottile/darkdetect |
| NumPy（含 OpenBLAS 等內附元件） | 2.5.4 | BSD-3-Clause 等，見各檔 | `licenses\NumPy-2.5.4\` | https://github.com/numpy/numpy |
| packaging | 26.3 | Apache-2.0 或 BSD-2-Clause | `licenses\packaging-26.3\` | https://github.com/pypa/packaging |
| psutil | 7.2.2 | BSD-3-Clause | `licenses\psutil-7.2.2\LICENSE` | https://github.com/giampaolo/psutil |
| PyYAML | 6.0.3 | MIT | `licenses\PyYAML-6.0.3\LICENSE` | https://github.com/yaml/pyyaml |
| Python（含 OpenSSL、libffi、bzip2、zlib 等內附函式庫及 MSVC 執行階段條款） | 3.13.17 | PSF License 及檔內所列各授權 | `licenses\Python-3.13.17\LICENSE.txt` | https://www.python.org/ |
| Tcl/Tk | 8.6 | Tcl/Tk License（BSD 類） | `licenses\Tcl-Tk-8.6\license.terms` | https://www.tcl-lang.org/ |
| PyInstaller bootloader | 6.22.3 | GPL-2.0-or-later，附 bootloader 例外 | `licenses\PyInstaller-6.22.3\COPYING.txt` | https://pyinstaller.org/ |

MuPDF 本身另內建多個第三方函式庫（字型、影像解碼等），其清單與授權全文位於 MuPDF 上游原始碼的
`thirdparty\` 目錄及 `COPYING`；PyMuPDF 2.0 的安裝套件未附這些檔案。取得方式：
https://github.com/ArtifexSoftware/mupdf （標籤 1.28.5）。

## 原始碼

因 PyMuPDF 採 AGPL-3.0，本程式整體也以 AGPL-3.0-or-later 釋出。
對應版本的完整原始碼包為 `PDF-to-JPG-1.0.0-source.zip`（程式、資源、授權檔、建置腳本與鎖定版本清單），
散布者應在提供 EXE 的同一位置一併提供。上表第三方元件的原始碼可由各網址取得對應版本。
