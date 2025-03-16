import re
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QTextEdit, QListWidget, QFileDialog, QMessageBox, QScrollArea)
from PySide6.QtGui import QFont
from brain import generate_file_content
from styles import light_stylesheet, dark_stylesheet

class KrakenBuilder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dark_mode = False
        self.setWindowTitle("pkgbuild.Kraken Builder")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set a default font for the entire application (this will be inherited by some widgets)
        default_font = QFont()
        default_font.setPointSize(16)
        self.setFont(default_font)
        
        self.init_ui()
    
    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # Top panel with utility buttons
        top_panel = self.build_top_panel()
        main_layout.addLayout(top_panel)
        
        # Content panel with left and right areas
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)
        
        left_widget = self.build_left_panel()
        content_layout.addWidget(left_widget)
        
        right_scroll = self.build_right_panel()
        content_layout.addWidget(right_scroll)
    
    def build_top_panel(self):
        top_panel = QHBoxLayout()
        btn_info = QPushButton("Info")
        btn_help = QPushButton("Help")
        self.btn_mode = QPushButton("Dark Mode")
        self.btn_mode.clicked.connect(self.toggle_dark_mode)
        
        top_panel.addWidget(btn_info)
        top_panel.addWidget(btn_help)
        top_panel.addStretch()
        top_panel.addWidget(self.btn_mode)
        return top_panel
    
    def build_left_panel(self):
        left_panel = QVBoxLayout()
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        left_widget.setFixedWidth(300)
        
        self.pkg_name = QLineEdit()
        self.pkg_name.setPlaceholderText("Enter package name")
        self.pkg_version = QLineEdit()
        self.pkg_version.setPlaceholderText("Enter package version")
        
        left_panel.addWidget(QLabel("Package Name:"))
        left_panel.addWidget(self.pkg_name)
        left_panel.addWidget(QLabel("Package Version:"))
        left_panel.addWidget(self.pkg_version)
        
        # Sources section
        self.source_list = QListWidget()
        self.source_input = QLineEdit()
        self.source_input.setPlaceholderText("Enter source URL")
        btn_add_source = QPushButton("Add Source")
        btn_add_source.clicked.connect(self.add_source)
        btn_remove_source = QPushButton("Remove Selected Source")
        btn_remove_source.clicked.connect(self.remove_selected_source)
        
        left_panel.addWidget(QLabel("Sources:"))
        left_panel.addWidget(self.source_list)
        left_panel.addWidget(self.source_input)
        left_panel.addWidget(btn_add_source)
        left_panel.addWidget(btn_remove_source)
        
        # Dependencies section
        self.dep_list = QListWidget()
        self.dep_input = QLineEdit()
        self.dep_input.setPlaceholderText("Enter dependency")
        btn_add_dep = QPushButton("Add Dependency")
        btn_add_dep.clicked.connect(self.add_dependency)
        btn_remove_dep = QPushButton("Remove Selected Dependency")
        btn_remove_dep.clicked.connect(self.remove_selected_dependency)
        
        left_panel.addWidget(QLabel("Dependencies:"))
        left_panel.addWidget(self.dep_list)
        left_panel.addWidget(self.dep_input)
        left_panel.addWidget(btn_add_dep)
        left_panel.addWidget(btn_remove_dep)
        
        # Generate button
        btn_generate = QPushButton("Generate PKGBUILD.kraken")
        btn_generate.clicked.connect(self.handle_generate)
        left_panel.addWidget(btn_generate)
        
        return left_widget
    
    def build_right_panel(self):
        right_scroll = QScrollArea()
        right_scroll.setWidgetResizable(True)
        right_content = QWidget()
        right_layout = QVBoxLayout(right_content)
        
        functions_order = ['prepare', 'build', 'test', 'install', 'preinstall', 'postinstall', 'remove']
        self.function_editors = {}
        default_cd = 'cd "${SOURCE_DIR}/${pkgname}/${pkgname}-${pkgver}" &&'
        for key in functions_order:
            label = QLabel(f"kraken_{key}()")
            label.setStyleSheet("font-weight: bold;")
            
            editor = QTextEdit()
            # Set the editor font size to 16
            font = QFont()
            font.setPointSize(16)
            editor.setFont(font)
            
            if key == "prepare":
                editor.setPlainText(
                    'tar -xvf "${SOURCE_DIR}/${pkgname}/${pkgname}-${pkgver}.tar.xz" -C "${SOURCE_DIR}/${pkgname}" &&\n'
                    'cd "${SOURCE_DIR}/${pkgname}/${pkgname}-${pkgver}" &&'
                )
            elif key in ['build', 'test', 'install', 'postinstall', 'remove']:
                editor.setPlainText(default_cd)
            elif key == "preinstall":
                editor.setPlainText('echo "nothing to do!"')
            editor.setMinimumHeight(100)
            editor.setStyleSheet("border: 1px solid #ccc; padding: 5px;")
            self.function_editors[key] = editor
            right_layout.addWidget(label)
            right_layout.addWidget(editor)
        
        right_layout.addStretch()
        right_scroll.setWidget(right_content)
        return right_scroll
    
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.setStyleSheet(dark_stylesheet())
            self.btn_mode.setText("Light Mode")
        else:
            self.setStyleSheet(light_stylesheet())
            self.btn_mode.setText("Dark Mode")
    
    def add_source(self):
        text = self.source_input.text().strip()
        if text:
            self.source_list.addItem(text)
            self.source_input.clear()
    
    def add_dependency(self):
        text = self.dep_input.text().strip()
        if text:
            self.dep_list.addItem(text)
            self.dep_input.clear()
    
    def remove_selected_source(self):
        row = self.source_list.currentRow()
        if row >= 0:
            self.source_list.takeItem(row)
    
    def remove_selected_dependency(self):
        row = self.dep_list.currentRow()
        if row >= 0:
            self.dep_list.takeItem(row)
    
    def handle_generate(self):
        deps = [self.dep_list.item(i).text() for i in range(self.dep_list.count())]
        sources = [self.source_list.item(i).text() for i in range(self.source_list.count())]
        md5sums = ["checksum_here" for _ in range(len(sources))]
        
        functions_order = ['prepare', 'build', 'test', 'install', 'preinstall', 'postinstall', 'remove']
        functions_dict = {}
        for key in functions_order:
            text = self.function_editors[key].toPlainText()
            functions_dict[key] = text
        
        content = generate_file_content(
            self.pkg_name.text(), self.pkg_version.text(),
            deps, sources, md5sums, functions_dict
        )
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "Kraken Files (*.kraken)")
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(content)
                QMessageBox.information(self, "Success", "File saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")

