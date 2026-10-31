# PDF to JPG v1.0

作者：Kaido-MSVC　授權：AGPL-3.0-or-later

自用 Windows 桌面程式。所有轉換都在本機完成。

## 直接使用

雙擊 `D:\projects\PDF to JPG\dist\PDF-to-JPG.exe`。

1. 按「加入 PDF」，選擇一份或多份 PDF。支援中文、日文檔名與路徑。
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
- 單頁超過 8,000 萬像素時略過並提示降低 DPI，以避免極大頁面耗盡記憶體。
- JPG 使用 RGB、不透明背景，並寫入所選 DPI。

## 單一 EXE

只需攜帶 `dist\PDF-to-JPG.exe`，不需旁附 Python、字型、主題或圖示。首次啟動可能需要數秒；PyInstaller 會先將內含資源解壓到 Windows 暫存目錄，正常離開時清理。EXE 未加數位簽章。

預設輸出資料夾在 EXE 旁的 `JPG輸出`；也可以改選其他可寫入的位置。EXE 圖示、視窗圖示與版本資訊均已內嵌。

## 開發與重建

專案使用自己的 `.venv`：Python 3.13.17、CustomTkinter 6.0.0、PyMuPDF 2.0、Pillow 13.0.0、PyInstaller 6.22.3、pefile 2024.8.26。

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

`build.ps1` 固定使用 `.venv`，先核對版本、執行測試，再建立單一 EXE。快取與中間檔保存在 `work`，成品在 `dist`。`requirements.txt` 記錄直接相依套件，`requirements-lock.txt` 為完整鎖定版本（含 PyMuPDF 2.0 連帶安裝的 onnxruntime 等，封裝時已排除）；建置程式不會自動安裝套件。

`verify.py` 會建立獨立測試資料夾，執行核心與實際 GUI 測試，將 EXE 複製到中文日文路徑，使用不含 Python 的子程序 PATH 啟動它，並檢查 EXE 圖示及版本資源。報告與深淺色截圖存於 `work\verify-日期時間`。

## 專案檔案

- `app.py`：繁體中文介面與背景工作協調，主執行緒處理所有視窗操作。
- `converter.py`：單執行緒逐頁渲染、密碼驗證、防覆寫與錯誤處理。
- `tests\test_converter.py`：11 組針對性測試。
- `smoke_test.py`、`verify.py`：來源程式與封裝 EXE 的整合驗證。
- `make_icon.py`、`assets`：本專案繪製的圖示及多尺寸 ICO。
- `PDF-to-JPG.spec`、`version_info.txt`、`build.ps1`：單一 EXE 建置設定。

封裝收集 CustomTkinter 的主題及字型、MuPDF DLL，排除本功能未使用的選用 layout / LLM 模組。驗證已在這台 Windows 11 x64 完成；尚未在另一台全新 Windows 或其他 Windows 版本測試。

## API 依據

已以本機 `inspect.signature`、實際呼叫及測試確認 API 相容性，並參考官方文件：

- [PyMuPDF Page.get_pixmap](https://pymupdf.readthedocs.io/en/latest/page.html#Page.get_pixmap)
- [PyInstaller 單檔與資料資源封裝](https://pyinstaller.org/en/stable/spec-files.html)

## 授權

Copyright (C) 2026 Kaido-MSVC

本程式以 [GNU Affero General Public License v3.0 或更新版本](LICENSE) 釋出。因內含 PyMuPDF（AGPL-3.0），轉發 EXE 時應一併提供或註明原始碼取得方式。第三方元件授權見 [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md)；兩份檔案也已內嵌於 EXE。
