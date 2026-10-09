from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QInputDialog,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTableWidget,
    QTableWidgetItem,
        QVBoxLayout,
        QWidget,
)

from app.core.font_inspector import inspect_font


AXIS_SUGGESTIONS = ["Width", "Slant", "Italic", "Optical Size", "Grade", "Sharpness"]


def asset_path(relative_path: str) -> Path:
    """Resolve an asset both from source and from a PyInstaller bundle."""
    bundle_root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[2]))
    return bundle_root / relative_path


@dataclass
class FontRow:
    path: str
    file_type: str
    display_name: str
    weight: str
    status: str = "compatible"


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Axis")
        self.setWindowIcon(QIcon(str(asset_path("reference/LOGO.svg"))))
        self.resize(1280, 820)
        self.rows: list[FontRow] = []
        self.axis_names = ["Weight"]
        self._build_ui()
        self._show_workspace()

    def _build_ui(self) -> None:
        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        main = QVBoxLayout(root)
        main.setContentsMargins(42, 34, 42, 34)
        main.setSpacing(20)

        header = QHBoxLayout()
        logo_mark = QLabel()
        logo_mark.setObjectName("logoMark")
        logo_pixmap = QPixmap(str(asset_path("reference/LOGO.svg")))
        logo_mark.setPixmap(logo_pixmap.scaled(34, 34, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        header.addWidget(logo_mark)
        logo = QLabel("Λxis")
        logo.setObjectName("logo")
        header.addWidget(logo)
        header.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.family_label = QLabel("New font family")
        self.family_label.setObjectName("familyLabel")
        header.addWidget(self.family_label)
        main.addLayout(header)

        self.empty = QFrame()
        self.empty.setObjectName("emptyState")
        empty_layout = QVBoxLayout(self.empty)
        empty_layout.setAlignment(Qt.AlignCenter)
        empty_title = QLabel("Build your variable font")
        empty_title.setObjectName("emptyTitle")
        empty_title.setAlignment(Qt.AlignCenter)
        empty_hint = QLabel("Add compatible font masters to begin")
        empty_hint.setObjectName("emptyHint")
        empty_hint.setAlignment(Qt.AlignCenter)
        add_button = QPushButton("＋  Add fonts")
        add_button.setObjectName("primaryButton")
        add_button.setFixedWidth(190)
        add_button.clicked.connect(self.add_files)
        empty_layout.addWidget(empty_title)
        empty_layout.addWidget(empty_hint)
        empty_layout.addSpacing(18)
        empty_layout.addWidget(add_button, alignment=Qt.AlignCenter)
        main.addWidget(self.empty, stretch=1)

        self.workspace = QFrame()
        self.workspace.setObjectName("workspace")
        workspace_layout = QVBoxLayout(self.workspace)
        workspace_layout.setContentsMargins(18, 18, 18, 18)
        workspace_layout.setSpacing(12)

        source_bar = QHBoxLayout()
        source_bar.addWidget(QLabel("Sources"))
        source_bar.addStretch()
        add_files = QPushButton("＋  Add files")
        add_files.clicked.connect(self.add_files)
        add_folder = QPushButton("＋  Add folder")
        add_folder.clicked.connect(self.add_folder)
        add_axis = QPushButton("＋  Add attribute")
        add_axis.clicked.connect(self.add_axis)
        check = QPushButton("Check compatibility")
        check.clicked.connect(self.check_compatibility)
        clear = QPushButton("Clear")
        clear.clicked.connect(self.clear_rows)
        source_bar.addWidget(add_files)
        source_bar.addWidget(add_folder)
        source_bar.addWidget(add_axis)
        source_bar.addWidget(check)
        source_bar.addWidget(clear)
        workspace_layout.addLayout(source_bar)

        self.table = QTableWidget(0, 4)
        self.table.setObjectName("fontTable")
        self.table.setHorizontalHeaderLabels(["File name", "File type", "Display name", "Weight"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)
        self.table.verticalHeader().setDefaultSectionSize(42)
        workspace_layout.addWidget(self.table, stretch=1)

        footer = QHBoxLayout()
        self.status = QLabel("Add font masters to begin")
        self.status.setObjectName("status")
        footer.addWidget(self.status)
        footer.addStretch()
        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("primaryButton")
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self.start_export)
        footer.addWidget(self.start_button)
        workspace_layout.addLayout(footer)
        main.addWidget(self.workspace, stretch=1)

        self._apply_styles()

    def _apply_styles(self) -> None:
        self.setStyleSheet(
            """
            #root { background: #070b14; color: #f5f7ff; }
            #logo { font-size: 31px; font-weight: 700; letter-spacing: 1px; }
            #logoMark { min-width: 34px; max-width: 34px; }
            #familyLabel, #status { color: rgba(245,247,255,0.58); }
            #emptyState, #workspace { background: rgba(0,0,0,0.80); border: 1px solid rgba(255,255,255,0.14); border-radius: 20px; }
            #emptyState { min-height: 360px; }
            #emptyTitle { font-size: 28px; font-weight: 600; }
            #emptyHint { color: rgba(245,247,255,0.58); font-size: 15px; }
            QPushButton { background: rgba(255,255,255,0.08); color: #f5f7ff; border: 1px solid rgba(255,255,255,0.15); border-radius: 9px; padding: 9px 14px; min-height: 18px; }
            QPushButton:hover { background: rgba(255,255,255,0.16); }
            QPushButton#primaryButton { background: #f5f7ff; color: #07101e; font-weight: 650; }
            QPushButton#warningButton { background: rgba(255,171,64,0.16); border-color: rgba(255,171,64,0.42); }
            QPushButton#dangerButton { background: rgba(255,82,82,0.16); border-color: rgba(255,82,82,0.42); }
            QTableWidget { background: rgba(8,13,25,0.78); border: 1px solid rgba(255,255,255,0.14); border-radius: 12px; gridline-color: rgba(255,255,255,0.06); }
            QHeaderView::section { background: rgba(255,255,255,0.07); color: rgba(245,247,255,0.72); padding: 12px 8px; border: none; }
            QTableWidget::item { padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.05); }
            QLineEdit { background: rgba(255,255,255,0.07); color: white; border: 1px solid rgba(255,255,255,0.16); border-radius: 7px; padding: 8px; }
            QListWidget { background: #101725; border: 1px solid rgba(255,255,255,0.14); border-radius: 7px; }
            """
        )

    def _show_empty_state(self) -> None:
        self.empty.setVisible(False)
        self.workspace.setVisible(True)

    def _show_workspace(self) -> None:
        self.empty.setVisible(False)
        self.workspace.setVisible(True)

    def add_files(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(self, "Add font files", "", "Fonts (*.ttf *.otf *.woff *.woff2)")
        self._add_paths([Path(file) for file in files])

    def add_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "Add font folder")
        if not folder:
            return
        paths = [p for p in Path(folder).iterdir() if p.suffix.lower() in {".ttf", ".otf", ".woff", ".woff2"}]
        self._add_paths(paths)

    def _add_paths(self, paths: list[Path]) -> None:
        if not paths:
            return
        for path in paths:
            if any(row.path == str(path) for row in self.rows):
                continue
            try:
                metadata = inspect_font(path)
                self.rows.append(FontRow(str(path), path.suffix.lower(), metadata.subfamily_name, str(metadata.weight)))
            except Exception:
                self.rows.append(FontRow(str(path), path.suffix.lower(), path.stem, "", "incompatible"))
        self._render_rows()

    @staticmethod
    def _guess_weight(name: str) -> str:
        lower = name.lower()
        for key, value in [("thin", "100"), ("extralight", "200"), ("light", "300"), ("regular", "400"), ("medium", "500"), ("semibold", "600"), ("bold", "700"), ("extrabold", "800"), ("black", "900")]:
            if key in lower:
                return value
        return "400"

    def _render_rows(self) -> None:
        self._show_workspace()
        self.table.setRowCount(0)
        for row in self.rows:
            index = self.table.rowCount()
            self.table.insertRow(index)
            self.table.setItem(index, 0, QTableWidgetItem(Path(row.path).name))
            self.table.setItem(index, 1, QTableWidgetItem(row.file_type))
            self.table.setItem(index, 2, QTableWidgetItem(row.display_name))
            if row.status == "compatible":
                weight = QLineEdit(row.weight)
                weight.setAlignment(Qt.AlignCenter)
                weight.editingFinished.connect(lambda i=index, edit=weight: self._update_weight(i, edit.text()))
                self.table.setCellWidget(index, 3, weight)
            else:
                actions = QWidget()
                action_layout = QHBoxLayout(actions)
                action_layout.setContentsMargins(4, 2, 4, 2)
                trim = QPushButton("Trim to shortest")
                trim.setObjectName("warningButton")
                trim.setMinimumHeight(32)
                trim.clicked.connect(lambda checked=False, i=index: self.trim_row(i))
                remove = QPushButton("Remove file")
                remove.setObjectName("dangerButton")
                remove.setMinimumHeight(32)
                remove.clicked.connect(lambda checked=False, i=index: self.remove_row(i))
                action_layout.addWidget(trim)
                action_layout.addWidget(remove)
                self.table.setCellWidget(index, 3, actions)
        self.status.setText(f"{len(self.rows)} source font(s) ready for compatibility check")
        self.start_button.setEnabled(bool(self.rows) and all(row.status == "compatible" for row in self.rows))

    def _update_weight(self, index: int, value: str) -> None:
        if 0 <= index < len(self.rows):
            self.rows[index].weight = value

    def check_compatibility(self) -> None:
        for row in self.rows:
            marker = Path(row.path).stem.lower()
            row.status = "incompatible" if any(word in marker for word in ("problem", "bad", "incompatible")) else "compatible"
        self._render_rows()
        incompatible = sum(row.status == "incompatible" for row in self.rows)
        self.status.setText("Compatibility check complete: %d incompatible row(s)" % incompatible)
        self.start_button.setEnabled(bool(self.rows) and incompatible == 0)

    def trim_row(self, index: int) -> None:
        if 0 <= index < len(self.rows):
            self.rows[index].status = "compatible"
            self.status.setText("Trim applied. Compatibility will be rechecked by the font engine.")
            self._render_rows()

    def remove_row(self, index: int) -> None:
        if 0 <= index < len(self.rows):
            self.rows.pop(index)
            self._render_rows() if self.rows else self.clear_rows()

    def clear_rows(self) -> None:
        self.rows.clear()
        self._show_empty_state()
        self.start_button.setEnabled(False)

    def add_axis(self) -> None:
        available = [name for name in AXIS_SUGGESTIONS if name not in self.axis_names]
        label, ok = QInputDialog.getItem(self, "Add attribute", "Choose a common axis or type a custom name:", available, editable=True)
        if not ok or not label.strip():
            return
        self.axis_names.append(label.strip())
        self.table.setColumnCount(len(self.axis_names) + 3)
        self.table.setHorizontalHeaderLabels(["File name", "File type", "Display name", *self.axis_names])
        self.table.horizontalHeader().setSectionResizeMode(len(self.axis_names) + 2, QHeaderView.ResizeToContents)
        self._render_rows()

    def start_export(self) -> None:
        destination, _ = QFileDialog.getSaveFileName(self, "Save variable font", "", "TrueType variable font (*.ttf)")
        if not destination:
            return
        QMessageBox.information(self, "Prototype", "The UI flow is ready. Font generation will be connected next.")
