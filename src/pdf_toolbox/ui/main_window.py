from __future__ import annotations

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from pdf_toolbox.core.job_queue import JobQueue
from pdf_toolbox.config import BASE_DIR
from pdf_toolbox.ui.tools_panels.compress_panel import CompressPanel
from pdf_toolbox.ui.tools_panels.convert_panels import ImagesToPdfPanel, PdfToImagesPanel, PptToPdfPanel
from pdf_toolbox.ui.tools_panels.delete_rotate_panel import DeleteRotatePanel
from pdf_toolbox.ui.tools_panels.merge_panel import MergePanel
from pdf_toolbox.ui.tools_panels.ocr_panel import OcrPanel
from pdf_toolbox.ui.tools_panels.reorder_panel import ReorderPanel
from pdf_toolbox.ui.tools_panels.split_panel import SplitPanel
from pdf_toolbox.ui.widgets.progress_list import ProgressList
from pdf_toolbox.services.io.validators import ValidationError


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PDF 工具箱")
        self.resize(740, 480)

        self._init_menu()

        self.queue = JobQueue()
        self.queue.progress.connect(self._on_progress)
        self.queue.finished.connect(self._on_finished)

        self.stack = QStackedWidget()
        self.progress_list = ProgressList()

        self._panels = [
            MergePanel(),
            SplitPanel(),
            DeleteRotatePanel(),
            ReorderPanel(),
            CompressPanel(),
            PdfToImagesPanel(),
            ImagesToPdfPanel(),
            PptToPdfPanel(),
            OcrPanel(),
        ]
        self._panel_index: dict[object, int] = {}

        self.home_page = self._build_home()
        self.stack.addWidget(self.home_page)

        for panel in self._panels:
            self.stack.addWidget(panel)
            self._panel_index[panel] = self.stack.indexOf(panel)
            panel.run_btn.clicked.connect(lambda _, p=panel: self._submit(p))

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(6)
        top_layout = QVBoxLayout()
        top_layout.setSpacing(6)
        nav_layout = QHBoxLayout()
        self.home_btn = QPushButton("返回首页")
        self.home_btn.clicked.connect(self._show_home)
        self.title_label = QLabel("功能中心")
        nav_layout.addWidget(self.home_btn)
        nav_layout.addWidget(self.title_label)
        nav_layout.addStretch(1)

        top_layout.addLayout(nav_layout)
        top_layout.addWidget(self.stack)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.progress_list)

        root = QWidget()
        root.setLayout(main_layout)
        self.setCentralWidget(root)
        self._show_home()

    def _init_menu(self) -> None:
        menubar = self.menuBar()
        help_menu = menubar.addMenu("帮助")
        about_action = help_menu.addAction("关于")
        about_action.triggered.connect(self._show_about)

    def _show_about(self) -> None:
        box = QMessageBox(self)
        box.setWindowTitle("关于 PDF Toolbox Qt")
        box.setText(
            "PDF Toolbox Qt\n"
            "离线本地 PDF 工具箱（PySide6 + pikepdf + PyMuPDF + Pillow）。\n"
            "支持合并、拆分、删除/旋转/重排、压缩、PDF/图片互转、PPT 转 PDF、OCR。\n"
            "软件免费使用。\n"
            "版本：0.1.0\n"
            "作者：苏耀勇\n"
            "了解新工具、问题反馈、扫码关注公众号。"
        )
        qr_path = BASE_DIR / "qrcode_wetchat.png"
        if qr_path.exists():
            pixmap = QPixmap(str(qr_path)).scaled(
                QSize(140, 140), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            box.setIconPixmap(pixmap)
        box.exec()

    def _build_home(self) -> QWidget:
        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignTop)
        title = QLabel("功能中心")
        title.setStyleSheet("font-size: 13px; font-weight: bold;")
        subtitle = QLabel("离线本地 PDF 工具箱：选择下方功能开始处理文件。")
        subtitle.setStyleSheet("color: #777777; font-size: 11px;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        grid = QGridLayout()
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(6)

        buttons = []
        for panel in self._panels:
            btn = QPushButton(panel.title)
            btn.setMinimumHeight(36)
            btn.setIcon(_panel_icon(panel))
            btn.setIconSize(QSize(16, 16))
            btn.clicked.connect(lambda _, p=panel: self._open_panel(p))
            buttons.append(btn)

        cols = 4
        for idx, btn in enumerate(buttons):
            row = idx // cols
            col = idx % cols
            grid.addWidget(btn, row, col)

        layout.addLayout(grid)
        layout.addSpacing(4)
        return root

    def _open_panel(self, panel) -> None:
        index = self._panel_index.get(panel)
        if index is None:
            return
        self.stack.setCurrentIndex(index)
        self.title_label.setText(panel.title)
        self.home_btn.setEnabled(True)

    def _show_home(self) -> None:
        self.stack.setCurrentIndex(0)
        self.title_label.setText("功能中心")
        self.home_btn.setEnabled(False)

    def _submit(self, panel) -> None:
        try:
            spec = panel.build_spec()
            if not spec.inputs:
                raise ValidationError("未选择输入文件")
            if not spec.output_dir:
                raise ValidationError("未选择输出目录")
        except Exception as exc:  # noqa: BLE001
            QMessageBox.warning(self, "参数错误", str(exc))
            return

        job_id = self.queue.submit(spec)
        self.progress_list.add_job(job_id, panel.title, self.queue.cancel)

    def _on_progress(self, progress) -> None:
        self.progress_list.update_progress(progress)

    def _on_finished(self, job_id, result) -> None:
        self.progress_list.finish(job_id, result)
        if not result.success and not result.cancelled:
            QMessageBox.warning(self, "任务失败", result.error or "未知错误")


def _panel_icon(panel) -> QIcon:
    title = getattr(panel, "title", "")
    if "合并" in title:
        return QIcon.fromTheme("list-add")
    if "拆分" in title or "提取" in title:
        return QIcon.fromTheme("view-split-left-right")
    if "删除" in title or "旋转" in title:
        return QIcon.fromTheme("edit-delete")
    if "重排" in title:
        return QIcon.fromTheme("view-sort-ascending")
    if "压缩" in title:
        return QIcon.fromTheme("folder-compressed")
    if "PDF -> 图片" in title:
        return QIcon.fromTheme("image-x-generic")
    if "图片 -> PDF" in title:
        return QIcon.fromTheme("x-office-document")
    if "PPT -> PDF" in title:
        return QIcon.fromTheme("x-office-presentation")
    if "OCR" in title or "识别" in title:
        return QIcon.fromTheme("insert-text")
    return QIcon.fromTheme("applications-graphics")
