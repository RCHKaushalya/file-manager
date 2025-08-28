from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QToolBar, QAction, QFileSystemModel, QTreeView, QListView, QTextEdit
)
from PyQt5.QtCore import Qt
import shutil

class FolderTreeView(QTreeView):
    def dropEvent(self, event):
        source_index = self.model().index(event.source().currentIndex().row(), 0)
        source_path = self.model().filePath(source_index)

        target_index = self.indexAt(event.pos())
        target_path = self.model().filePath(target_index)

        if source_path and target_path:
            try:
                shutil.move(source_path, target_path)
            except Exception as e:
                print(f"Error moving file: {e}")

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

        self.folder_view = FolderTreeView()
        self.folder_view.setModel(self.folder_model)
        self.folder_view.setRootIndex(self.folder_model.index(''))
        self.folder_view.setColumnWidth(0, 250)
        self.folder_view.setHeaderHidden(True)
        self.folder_view.setAcceptDrops(True)  
        self.folder_view.setDragDropMode(self.folder_view.DropOnly)

        # File view
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath('')

        self.file_view = QListView()
        self.file_view.setModel(self.file_model)
        self.file_view.setDragEnabled(True)
        self.file_view.setSelectionMode(self.file_view.SingleSelection)

        # Metadata preview
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setMinimumWidth(300)

        layout.addWidget(self.folder_view, 1)
        layout.addWidget(self.file_view, 2)
        layout.addWidget(self.preview, 1)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def _connect_signals(self):
        self.folder_view.clicked.connect(self.on_folder_clicked)
        self.file_view.clicked.connect(self.on_file_clicked)
    
    def on_folder_clicked(self, index):
        folder_path = self.folder_model.filePath(index)
        self.file_view.setRootIndex(self.file_model.index(folder_path))
    
    def on_file_clicked(self, index):
        file_path = self.file_model.filePath(index)
        file_info = self.file_model.fileInfo(index)

        name = file_info.fileName()
        size = file_info.size()
        last_modified = file_info.lastModified().toString('yyyy-MM-dd hh:mm:ss')
        file_type = 'Folder' if file_info.isDir() else 'File'

        preview_text = (
            f"Name: {name}\n"
            f"Type: {file_type}\n"
            f"Size: {size} bytes\n"
            f"Last Modified: {last_modified}\n"
            f"Path: {file_path}\n"
        )

        self.preview.setText(preview_text)