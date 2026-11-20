# PDF to JPG v1.0.1

作者：Kaido-MSVC　授權：AGPL-3.0-or-later

自用 Windows 桌面程式。所有轉換都在本機完成。

## 直接使用

雙擊 `dist\PDF-to-JPG.exe`。

1. 按「加入 PDF」，選擇一份或多份 PDF。支援含中文或日文的檔名與路徑。
2. 選擇輸出目錄、150 / 200 / 300 / 600 DPI，以及 1–100 的 JPG 品質。
3. 按「開始轉換」。需要開啟密碼的 PDF 會逐檔詢問，密碼只用於本次開啟，不儲存、不記錄。
4. 完成後按「開啟輸出目錄」。

預設為 200 DPI、品質 92。一般文件可用 200 或 300 DPI；600 DPI 會使用更多時間、記憶體及磁碟空間。右上角可切換系統、淺色或深色外觀。

## 輸出與取消

- 每份 PDF 各建一個資料夾，逐頁命名，例如 `文件\文件_p0001.jpg`。
- 已有同名資料夾時，建立 `文件 (2)`、`文件 (3)`，不覆寫既有檔案。
- 相同來源重複加入時自動去重；不同資料夾的同名 PDF 仍各自處理。
- 「取消」在目前頁面處理結束後停止；已完成的 JPG 保留。關閉視窗時也會先等待目前工作結束。
- 進度條按各份檔案的頁面完成比例計算，頁數顯示目前檔案的進度。
- 密碼錯誤或在密碼視窗按取消，略過該 PDF，其他檔案繼續。需要重試時重新執行該檔案。
- 損壞、遺失、偽裝成 PDF 或無法讀取的檔案會顯示錯誤。單頁失敗會繼續後續頁面及其他檔案。
- 輸出目錄無法建立或寫入時會顯示錯誤。寫入失敗會移除該次建立的不完整 JPG。
- 單頁估算超過 8,000 萬像素時略過並提示降低 DPI。此上限針對輸出像素數。PDF 開啟、內嵌資源解碼、原生渲染及 JPG 編碼仍會各自使用時間和記憶體。
- JPG 使用 RGB、不透明背景，並寫入所選 DPI。

## 單一 EXE

執行時只需 `dist\PDF-to-JPG.exe`，不需旁附 Python、字型、主題或圖示。分享給他人時仍有授權義務，須在同一位置一併提供原始碼檔案（見下方「分享給他人」）。需要 Windows 10 或 11 x64（使用系統內建的 Universal CRT，EXE 不另附）。首次啟動可能需要數秒；PyInstaller 會先將內含資源解壓到 Windows 暫存目錄，正常離開時清理。EXE 未加數位簽章。

預設輸出資料夾在 EXE 旁的 `JPG輸出`；也可以改選其他可寫入的位置。EXE 圖示、視窗圖示與版本資訊均已內嵌。

## 開發與重建

專案使用自己的 `.venv`：Python 3.13.17 x64、CustomTkinter 6.0.0、PyMuPDF 2.1（MuPDF 1.28.6、Brotli 1.2.1）、Pillow 13.0.0、PyInstaller 6.22.3、pefile 2024.8.26。

首次建立（或重建）環境：

```powershell
py -3.13 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
```

日常在本專案 PowerShell 執行：

```powershell
.venv\Scripts\python.exe app.py
.\build.ps1
.venv\Scripts\python.exe verify.py
```

`build.ps1` 預設使用 `.venv`。從 Git 建置時，工作樹須維持乾淨。腳本核對 Python 與鎖定套件版本，執行單元測試，使用每次新建的 PyInstaller 工作目錄與快取，產出 EXE 及記錄 Git commit 與 EXE SHA-256 的 `BUILD-INFO.json`。原始碼 ZIP 解壓後也可重建 EXE，此時建置紀錄的 commit 欄位為空。圖示取自專案資源。建置需要 Visual Studio 2026（含「使用 C++ 的桌面開發」工作負載），`MSVCP140.dll` 取自 `VC\Redist\MSVC\14.52.37025\x64\Microsoft.VC145.CRT`，目錄版本與 SHA-256 固定在 `PDF-to-JPG.spec`。建置工作目錄與單元測試紀錄存於 `work`，成品預設在 `dist`。

`requirements.txt` 記錄直接相依套件，`requirements-lock.txt` 鎖定完整環境。PyMuPDF 2.1 連帶安裝的 onnxruntime、layout 與 LLM 套件會在封裝時排除。

`verify.py` 會建立獨立測試資料夾，執行核心與 GUI 測試，將 EXE 複製到含中文、日文的路徑，以不含 Python 的子程序 PATH 啟動，再核對 EXE 的 x64 架構、圖示、版本資源及封裝內的 PDF 原生函式庫 SHA-256。GUI 測試會轉換 Brotli 壓縮頁面，並記錄 Windows 實際載入的 MuPDF DLL 雜湊。報告與截圖存於 `work\verify-日期時間`。可用 `build.ps1 -PythonPath ... -OutputDirectory ...` 和 `verify.py --exe ... --unit-test-log ...` 驗證獨立建置，也可沿用該次建置的單元測試紀錄。

## 專案檔案

- `app.py`：繁體中文介面與背景工作協調，主執行緒處理所有視窗操作。
- `converter.py`：單執行緒逐頁渲染、密碼驗證、防覆寫與錯誤處理。
- `tests\test_converter.py`：轉換、輸入錯誤與輸出檔案保護的單元測試。
- `smoke_test.py`、`verify.py`：來源程式與封裝 EXE 的整合驗證。
- `make_icon.py`、`assets`：本專案繪製的圖示及多尺寸 ICO。
- `PDF-to-JPG.spec`、`version_info.txt`、`build.ps1`：單一 EXE 建置設定。
- `collect_licenses.py`、`licenses`：第三方授權全文，會內嵌於 EXE。Python 套件的授權由腳本從建置環境複製。MuPDF 1.28.6 的授權來源見 `licenses\MuPDF-1.28.6\PROVENANCE.md`。
- `make_source_zip.ps1`：產生對應原始碼包、驗證上游 AGPL 原始碼包並輸出 `SHA256SUMS.txt`。

封裝收集 CustomTkinter 的主題及字型、MuPDF DLL，排除本功能未使用的選用 layout / LLM 模組。驗證已在這台 Windows 11 x64 完成；尚未在另一台全新 Windows 或其他 Windows 版本測試。

## API 依據

已以本機 `inspect.signature`、實際呼叫及測試確認 API 相容性，並參考官方文件：

- [PyMuPDF Page.get_pixmap](https://pymupdf.readthedocs.io/en/latest/page.html#Page.get_pixmap)
- [PyInstaller 單檔與資料資源封裝](https://pyinstaller.org/en/stable/spec-files.html)

## 安全更新與限制

- v1.0.1 使用官方 PyMuPDF 2.1 Windows x64 wheel，其中的 MuPDF 1.28.6 內附 Brotli 1.2.1，修復 CVE-2026-111497。[PyMuPDF 2.1 發行說明](https://github.com/pymupdf/PyMuPDF/releases/tag/2.1) · [Brotli 1.2.1 安全公告](https://github.com/google/brotli/releases/tag/v1.2.1)
- MuPDF 1.28.6 仍含 CVE-2026-112036 的受影響簽章驗證程式。現有功能呼叫 PDF 開啟、密碼解鎖與頁面渲染，靜態檢查未找到連到該簽章驗證函式的路徑。待官方 PyMuPDF 的 Windows wheel 納入對應修補後，核對原始碼、DLL 與回歸結果再升級。[Artifex 修補提交](https://github.com/ArtifexSoftware/mupdf/commit/3984925b660afb8a781ddf504021e91be1bc671e)
- MuPDF 內含 FreeType 2.14.3。轉換可能解碼 PDF 內嵌的 CID 字型，仍有 CVE-2026-95512 所述的資源耗用風險，應隨上游安全更新一併追蹤。[FreeType 修補提交](https://gitlab.freedesktop.org/freetype/freetype/-/commit/f3ca71c9900fe860849b3163a6e2c1e765b291d9)
- 渲染仍在背景執行緒執行。程式會在目前的原生呼叫或 JPG 寫入返回後回應取消。像素上限與減少點陣圖複製可降低一般轉換的記憶體用量，對不受控輸入仍缺少程序級的時間、記憶體隔離。

## 分享給他人

EXE 內含 AGPL-3.0 的 PyMuPDF / MuPDF。轉發 EXE 時，不論分享對象多少，都必須讓收到的人能取得對應版本的完整原始碼：

1. 提交所有變更後執行 `.\build.ps1`，確保 EXE 由已提交的版本建置。
2. 執行 `.\make_source_zip.ps1`。腳本會以 `BUILD-INFO.json` 核對目前 Git commit 和 EXE 實際 SHA-256，再用該 commit 建立原始碼 ZIP。上游檔案以固定的 SHA-256 驗證，快取於 `work\upstream-sources`。可選用 `-OutputDirectory` 指向同一次建置的輸出資料夾。
   - `PDF-to-JPG-1.0.1-source.zip`：本程式原始碼、資源、授權、建置腳本及鎖定版本清單，ZIP 註解內有 commit。
   - `pymupdf-2.1.tar.gz`：PyMuPDF 2.1 官方 sdist。
   - `mupdf-1.28.6-source.tar.gz`：PyMuPDF 2.1 使用的 MuPDF 官方原始碼包，含 thirdparty。
   - `BUILD-INFO.json`：建置 commit 與 EXE 的 SHA-256。
   - `SHA256SUMS.txt`：EXE、建置紀錄與原始碼檔案的 SHA-256。
3. 將 EXE 與上列五個檔案放在同一個分享位置一併提供。

其他非 copyleft 第三方套件的原始碼可依 `requirements-lock.txt` 的版本由 PyPI 或 `THIRD-PARTY-NOTICES.md` 所列網址取得。

EXE 內含 Microsoft Visual C++ 執行階段檔案（`MSVCP140.dll` 等）。這些檔案是 Microsoft 的 Distributable Code，不適用 AGPL；收到 EXE 的人使用或轉發時須遵守 `THIRD-PARTY-NOTICES.md`「Microsoft Visual C++ 執行階段使用條款」，轉發時要連同該條款一併提供。依 Visual Studio 授權，散布者須為因散布本程式而對 Microsoft 提出的索賠負責（僅基於未修改之 Microsoft 檔案本身的索賠除外）。

## 授權

Copyright (C) 2026 Kaido-MSVC

本程式以 [GNU Affero General Public License v3.0 或更新版本](LICENSE) 釋出；此標示只適用於本專案自行撰寫的部分，第三方元件依各自授權。第三方元件清單見 [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md)，完整授權文字在 [licenses](licenses) 資料夾。`LICENSE`、第三方聲明與 `licenses` 均已內嵌於 EXE，可在程式右上角「關於」視窗的「授權全文」與「第三方元件」分頁檢視。
