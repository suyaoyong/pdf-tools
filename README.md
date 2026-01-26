# PDF Toolbox Qt

Offline local PDF toolbox (PySide6 + pikepdf + PyMuPDF + Pillow).
离线本地 PDF 工具箱（PySide6 + pikepdf + PyMuPDF + Pillow）。

## Features (Phase 1) / 功能（Phase 1）
- Merge, split/extract, delete pages, rotate pages, reorder pages
- Basic compression, image re-encode compression
- PDF → Images, Images → PDF, PPT → PDF
- Batch processing, progress display, cancelable
- 3 built-in presets

## Phase 2 (In Progress) / Phase 2（进行中）
- Office conversion (WPS first, LibreOffice fallback) / Office 互转（WPS 优先，LibreOffice 兜底）
- OCR (quality first) / OCR（质量优先）
- Watermark (text/image) / 水印（文字/图片）

## Install & Run / 安装与运行

```bash
# Recommended: use a virtual environment / 建议使用虚拟环境
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# Run / 运行
python -m pdf_toolbox.app
# Or / 或
pdf-toolbox-qt
```

## Office Conversion Notes (WPS First) / Office 互转说明（WPS 优先）
- Default engine: WPS COM (requires WPS + pywin32)
- If WPS is unavailable, use LibreOffice (ensure `soffice` is available)
- Fully offline, no cloud services

## PPT to PDF Notes / PPT 转 PDF 说明
- Requires Microsoft PowerPoint or WPS Presentation (COM automation export)
- If no PPT engine is detected, an error will be shown

## Packaging (Windows) / 打包（Windows）

```bash
# Option 1: script / 方式1：直接使用脚本
powershell -ExecutionPolicy Bypass -File .\scripts\build_win.ps1

# Option 2: PyInstaller / 方式2：手动执行 PyInstaller
pip install pyinstaller
pyinstaller --noconsole --name pdf-toolbox-qt --add-data "assets;assets" -m pdf_toolbox.app
```

> Note: PySide6 packaging may require extra Qt plugins. If you see a black window or missing DLLs, follow PyInstaller and Qt docs.
> 说明：PySide6 打包可能需要额外的 Qt 插件收集，若遇到启动黑屏或缺 DLL，请参考 PyInstaller 与 Qt 的官方说明进行补齐。

## Structure / 目录结构

```
pdf-toolbox-qt/
  assets/
  scripts/
  src/pdf_toolbox/
    app.py
    ui/
    core/
    services/
  tests/
```

## FAQ / 常见问题
- **Encrypted PDF can't be processed**: enter the password or decrypt elsewhere first.
- **Output failed**: check output folder permissions or whether the file is in use.
- **Large files are slow**: try basic compression or reduce DPI first.

## Development Notes / 开发说明
- UI handles interaction/presentation only; business logic is in `services/`.
- Job queue: `core/job_queue.py` with progress and cancellation.
- `core/range_parser.py` parses page ranges and has unit tests.
