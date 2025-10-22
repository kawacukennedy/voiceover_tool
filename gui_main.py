import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QComboBox, QLineEdit, QLabel, QWidget, QTabWidget, QListWidget, QProgressBar, QFileDialog, QMessageBox, QInputDialog
from PyQt6.QtCore import QThread, pyqtSignal
from voice import list_voices
from cli import run_cli

class SynthWorker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, args):
        super().__init__()
        self.args = args

    def run(self):
        try:
            run_cli(self.args)
            self.finished.emit("Synthesis completed")
        except Exception as e:
            self.finished.emit(f"Error: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Offline TTS")
        self.setGeometry(100, 100, 800, 600)

        tabs = QTabWidget()
        self.setCentralWidget(tabs)

        # Home tab
        home_tab = QWidget()
        layout = QVBoxLayout(home_tab)
        layout.addWidget(QLabel("Text:"))
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)
        layout.addWidget(QLabel("Voice:"))
        self.voice_combo = QComboBox()
        voices = list_voices()
        for v in voices:
            self.voice_combo.addItem(v.name)
        layout.addWidget(self.voice_combo)
        layout.addWidget(QLabel("Output:"))
        self.output_edit = QLineEdit("output.mp3")
        layout.addWidget(self.output_edit)
        self.synth_button = QPushButton("Synthesize")
        self.synth_button.clicked.connect(self.on_synth)
        layout.addWidget(self.synth_button)
        tabs.addTab(home_tab, "Home")

        # Voice Manager tab
        voice_tab = QWidget()
        layout = QVBoxLayout(voice_tab)
        self.voice_list = QListWidget()
        self.update_voice_list()
        layout.addWidget(self.voice_list)
        import_button = QPushButton("Import Voice")
        import_button.clicked.connect(self.on_import_voice)
        layout.addWidget(import_button)
        preview_button = QPushButton("Preview")
        preview_button.clicked.connect(self.on_preview_voice)
        layout.addWidget(preview_button)
        tabs.addTab(voice_tab, "Voice Manager")

        # Render Queue tab
        render_tab = QWidget()
        layout = QVBoxLayout(render_tab)
        self.queue_list = QListWidget()
        layout.addWidget(self.queue_list)
        add_button = QPushButton("Add to Queue")
        add_button.clicked.connect(self.on_add_to_queue)
        layout.addWidget(add_button)
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        start_button = QPushButton("Start Render")
        start_button.clicked.connect(self.on_start_render)
        layout.addWidget(start_button)
        tabs.addTab(render_tab, "Render Queue")

        # Settings tab
        settings_tab = QWidget()
        layout = QVBoxLayout(settings_tab)
        layout.addWidget(QLabel("Settings placeholder"))
        tabs.addTab(settings_tab, "Settings")

        # About tab
        about_tab = QWidget()
        layout = QVBoxLayout(about_tab)
        layout.addWidget(QLabel("Offline TTS v1.0.0"))
        tabs.addTab(about_tab, "About")

    def on_synth(self):
        text = self.text_edit.toPlainText()
        voice = self.voice_combo.currentText()
        output = self.output_edit.text()
        args = ['synth', '--text', text, '--voice', voice, '--out', output]
        self.worker = SynthWorker(args)
        self.worker.finished.connect(self.on_synth_finished)
        self.worker.start()
        self.synth_button.setEnabled(False)

    def on_synth_finished(self, message):
        self.synth_button.setEnabled(True)
        QMessageBox.information(self, "Result", message)

    def on_import_voice(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Embedding File")
        if file_path:
            name, ok = QInputDialog.getText(self, "Voice Name", "Enter voice name:")
            if ok and name:
                args = ['import-voice', file_path, '--name', name]
                run_cli(args)
                self.update_voice_list()

    def on_preview_voice(self):
        current = self.voice_list.currentItem()
        if current:
            voice = current.text().split()[0]
            args = ['preview-voice', voice]
            run_cli(args)

    def on_add_to_queue(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Text File")
        if file_path:
            self.queue_list.addItem(file_path)

    def on_start_render(self):
        # Placeholder for batch processing
        QMessageBox.information(self, "Render", "Batch rendering not fully implemented in GUI yet")

    def update_voice_list(self):
        self.voice_list.clear()
        voices = list_voices()
        for v in voices:
            self.voice_list.addItem(f"{v.name} ({v.gender}, {v.locale})")

def gui_main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())