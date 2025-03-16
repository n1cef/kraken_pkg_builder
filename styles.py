def light_stylesheet():
    return """
        QMainWindow { background-color: #f0f0f0; color: #000; }
        QLabel, QLineEdit, QListWidget, QTextEdit { background-color: #fff; color: #000; }
        QPushButton { background-color: #337ab7; color: #fff; border: 1px solid #2e6da4; padding: 5px; }
        QPushButton:hover { background-color: #286090; }
    """

def dark_stylesheet():
    return """
        QMainWindow { background-color: #2b2b2b; color: #e0e0e0; }
        QLabel, QLineEdit, QListWidget, QTextEdit { background-color: #3c3f41; color: #e0e0e0; }
        QPushButton { background-color: #3c3f41; color: #e0e0e0; border: 1px solid #555; padding: 5px; }
        QPushButton:hover { background-color: #555; }
    """

