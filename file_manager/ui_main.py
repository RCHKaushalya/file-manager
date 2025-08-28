from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QToolBar, QAction, QFileSystemModel, QTreeView, QListView
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My File Manager")
        self.setGeometry(100, 100, 1000, 600)

        self._create_toolbar()
        self._create_main_layout()
        self._connect_signals()

    def _create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        open_action = QAction("Open", self)
        delete_action = QAction("Delete", self)
        rename_action = QAction("Rename", self)

        toolbar.addAction(open_action)
        toolbar.addAction(delete_action)
        toolbar.addAction(rename_action)
    
    def _create_main_layout(self):
        central_widget = QWidget()
        layout = QHBoxLayout()

        # Folder tree
        self.folder_model = QFileSystemModel()
        self.folder_model.setRootPath('')

        self.folder_view = QTreeView()
        self.folder_view.setModel(self.folder_model)
        self.folder_view.setColumnWidth(0, 250)
        self.folder_view.setHeaderHidden(True)

        # File view
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath('')
        self.file_view = QListView()
        self.file_view.setModel(self.file_model)

        layout.addWidget(self.folder_view, 1)
        layout.addWidget(self.file_view, 2)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def _connect_signals(self):
        self.folder_view.clicked.connect(self.on_folder_clicked)
    
    def on_folder_clicked(self, index):
        folder_path = self.folder_model.filePath(index)
        self.file_view.setRootIndex(self.file_model.index(folder_path))