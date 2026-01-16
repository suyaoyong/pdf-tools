# PDF Toolbox Qt

离线本地 PDF 工具箱（PySide6 + pikepdf + PyMuPDF + Pillow）。

## 功能（Phase 1）
- 合并、拆分/提取、删除页、旋转页、重排页
- 基础压缩、图片重编码压缩
- PDF -> 图片、图片 -> PDF、PPT -> PDF
- 批处理、进度显示、可取消
- 3 个内置 Preset

## Phase 2（进行中）
- Office 互转（WPS 优先，LibreOffice 兜底）
- OCR（PaddleOCR，质量优先）
- 水印（文字/图片）

## 安装与运行

```bash
# 建议使用虚拟环境
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# 运行
python -m pdf_toolbox.app
# 或
pdf-toolbox-qt
```

## Office 互转说明（WPS 优先）
- 默认使用 WPS COM 引擎（需要安装 WPS + pywin32）
- 若 WPS 不可用，可选择 LibreOffice 引擎（需安装 LibreOffice 并确保 `soffice` 可用）
- 全程离线，不使用云服务

## PPT 转 PDF 说明
- 需要安装 Microsoft PowerPoint 或 WPS 演示（通过 COM 自动化导出 PDF）
- 若未检测到 PPT 引擎会提示错误

## 打包（Windows）

```bash
# 方式1：直接使用脚本
powershell -ExecutionPolicy Bypass -File .\scripts\build_win.ps1

# 方式2：手动执行 PyInstaller
pip install pyinstaller
pyinstaller --noconsole --name pdf-toolbox-qt --add-data "assets;assets" -m pdf_toolbox.app
```

> 说明：PySide6 打包可能需要额外的 Qt 插件收集，若遇到启动黑屏或缺 DLL，请参考 PyInstaller 与 Qt 的官方说明进行补齐。

## 目录结构

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

## 常见问题

- **加密 PDF 无法处理**：请输入密码后重试，或先在其他工具解除加密。
- **输出失败**：请检查输出目录权限或是否被占用。
- **大文件处理较慢**：建议先使用基础压缩或降 DPI。

## 开发说明

- UI 仅负责交互与展示，业务逻辑在 `services/`。
- 任务队列位于 `core/job_queue.py`，支持进度与取消。
- `core/range_parser.py` 负责页码范围解析并有单元测试。
