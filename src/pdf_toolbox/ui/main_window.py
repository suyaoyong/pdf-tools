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
from pdf_toolbox.i18n import get_language, set_language, t
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
        self.setWindowTitle(t("window_title"))
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
        self._panel_buttons: list[QPushButton] = []

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
        self.home_btn = QPushButton(t("nav_home"))
        self.home_btn.clicked.connect(self._show_home)
        self.title_label = QLabel(t("nav_tools"))
        self.lang_btn = QPushButton()
        self.lang_btn.clicked.connect(self._toggle_language)
        self._set_lang_button_text()
        nav_layout.addWidget(self.home_btn)
        nav_layout.addWidget(self.title_label)
        nav_layout.addStretch(1)
        nav_layout.addWidget(self.lang_btn)

        top_layout.addLayout(nav_layout)
        top_layout.addWidget(self.stack)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.progress_list)

        root = QWidget()
        root.setLayout(main_layout)
        self.setCentralWidget(root)
        self._show_home()
        self._apply_language()

    def _init_menu(self) -> None:
        menubar = self.menuBar()
        self.help_menu = menubar.addMenu(t("menu_help"))
        self.about_action = self.help_menu.addAction(t("menu_about"))
        self.about_action.triggered.connect(self._show_about)

    def _show_about(self) -> None:
        box = QMessageBox(self)
        box.setWindowTitle(t("about_title"))
        box.setText(t("about_text"))
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
        self.home_title_label = QLabel(t("home_title"))
        self.home_title_label.setStyleSheet("font-size: 13px; font-weight: bold;")
        self.home_subtitle_label = QLabel(t("home_subtitle"))
        self.home_subtitle_label.setStyleSheet("color: #777777; font-size: 11px;")

        layout.addWidget(self.home_title_label)
        layout.addWidget(self.home_subtitle_label)

        grid = QGridLayout()
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(6)

        for panel in self._panels:
            btn = QPushButton(panel.title)
            btn.setMinimumHeight(36)
            btn.setIcon(_panel_icon(panel))
            btn.setIconSize(QSize(16, 16))
            btn.clicked.connect(lambda _, p=panel: self._open_panel(p))
            self._panel_buttons.append(btn)

        cols = 4
        for idx, btn in enumerate(self._panel_buttons):
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
        self.title_label.setText(t("nav_tools"))
        self.home_btn.setEnabled(False)

    def _submit(self, panel) -> None:
        try:
            spec = panel.build_spec()
            if not spec.inputs:
                raise ValidationError(t("err_no_input_files"))
            if not spec.output_dir:
                raise ValidationError(t("err_no_output_dir"))
        except Exception as exc:  # noqa: BLE001
            QMessageBox.warning(self, t("invalid_params_title"), str(exc))
            return

        job_id = self.queue.submit(spec)
        self.progress_list.add_job(job_id, panel.title, self.queue.cancel)

    def _on_progress(self, progress) -> None:
        self.progress_list.update_progress(progress)

    def _on_finished(self, job_id, result) -> None:
        self.progress_list.finish(job_id, result)
        if not result.success and not result.cancelled:
            QMessageBox.warning(self, t("task_failed_title"), result.error or t("unknown_error"))

    def _toggle_language(self) -> None:
        new_lang = "zh" if get_language() == "en" else "en"
        set_language(new_lang)
        self._set_lang_button_text()
        self._apply_language()

    def _set_lang_button_text(self) -> None:
        self.lang_btn.setText(t("lang_to_zh") if get_language() == "en" else t("lang_to_en"))

    def _apply_language(self) -> None:
        self.setWindowTitle(t("window_title"))
        self.home_btn.setText(t("nav_home"))
        self._set_lang_button_text()
        if self.stack.currentIndex() == 0:
            self.title_label.setText(t("nav_tools"))
        else:
            for panel, index in self._panel_index.items():
                if index == self.stack.currentIndex():
                    self.title_label.setText(panel.title)
                    break
        self.help_menu.setTitle(t("menu_help"))
        self.about_action.setText(t("menu_about"))
        self.home_title_label.setText(t("home_title"))
        self.home_subtitle_label.setText(t("home_subtitle"))
        for panel, btn in zip(self._panels, self._panel_buttons):
            btn.setText(panel.title)
        for panel in self._panels:
            panel.apply_language()
        self.progress_list.apply_language()


def _panel_icon(panel) -> QIcon:
    tool_id = getattr(panel, "tool_id", "")
    if tool_id == "merge":
        return QIcon.fromTheme("list-add")
    if tool_id == "split_extract":
        return QIcon.fromTheme("view-split-left-right")
    if tool_id in {"delete_rotate", "delete_pages", "rotate_pages"}:
        return QIcon.fromTheme("edit-delete")
    if tool_id == "reorder_pages":
        return QIcon.fromTheme("view-sort-ascending")
    if tool_id in {"compress", "compress_basic", "compress_images"}:
        return QIcon.fromTheme("folder-compressed")
    if tool_id == "pdf_to_images":
        return QIcon.fromTheme("image-x-generic")
    if tool_id == "images_to_pdf":
        return QIcon.fromTheme("x-office-document")
    if tool_id == "ppt_to_pdf":
        return QIcon.fromTheme("x-office-presentation")
    if tool_id == "ocr":
        return QIcon.fromTheme("insert-text")
    return QIcon.fromTheme("applications-graphics")
