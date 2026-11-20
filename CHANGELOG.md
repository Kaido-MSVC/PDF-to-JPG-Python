# 版本紀錄

## v1.0.1

### 安全性

- 升級至 PyMuPDF 2.1，內含 MuPDF 1.28.6 與 Brotli 1.2.1，修復 CVE-2026-111497。
- 建置紀錄新增 Git commit 與 EXE SHA-256。封裝時核對兩者，再從對應 commit 建立原始碼 ZIP。

### 修正

- 批次轉換遇到個別路徑解析或讀取錯誤時，回報該檔案並繼續處理其餘 PDF。
- 移除渲染轉交 JPG 編碼時的一份 RGB 資料複本，降低大頁面的峰值記憶體用量。
- 更新套件鎖定、第三方元件聲明，以及 Windows 發行檔內附的授權資料。

### 已知限制

- 單頁輸出上限為 8,000 萬像素。取消會在目前的原生呼叫或 JPG 寫入返回後生效。內嵌 CID 字型仍可能使轉換卡住或耗用大量記憶體。 [FreeType CVE-2026-95512](https://access.redhat.com/security/cve/cve-2026-95512)
- MuPDF 1.28.6 仍待納入 CVE-2026-112036 的簽章驗證修補。PDF-to-JPG 的開檔與逐頁渲染流程透過靜態檢查未找到通往受影響函式的呼叫路徑。 [Artifex 修補提交](https://github.com/ArtifexSoftware/mupdf/commit/3984925b660afb8a781ddf504021e91be1bc671e)

## v1.0.0

- 首次發布 Windows x64 可攜版，提供單檔與批次 PDF 逐頁轉 JPG、DPI 與品質設定、密碼輸入及取消功能。 [v1.0.0 發行紀錄](https://github.com/Kaido-MSVC/PDF-to-JPG-Python/releases/tag/v1.0.0)
