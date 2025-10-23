import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import threading
from voice import list_voices
from cli import run_cli

class SynthWorker(threading.Thread):
    def __init__(self, args, callback):
        super().__init__()
        self.args = args
        self.callback = callback

    def run(self):
        try:
            run_cli(self.args)
            self.callback("Synthesis completed")
        except Exception as e:
            self.callback(f"Error: {e}")

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Offline TTS")
        self.geometry("800x600")

        # High contrast theme
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12), padding=10)
        style.configure('TLabel', font=('Arial', 12))
        style.configure('TEntry', font=('Arial', 12))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Keyboard navigation
        self.bind('<Control-s>', lambda e: self.on_synth())
        self.bind('<Control-i>', lambda e: self.on_import_voice())

        self.create_home_tab()
        self.create_voice_tab()
        self.create_queue_tab()
        self.create_settings_tab()
        self.create_about_tab()

    def create_home_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Home")

        ttk.Label(frame, text="Text:").pack(anchor=tk.W, padx=10, pady=5)
        self.text_edit = tk.Text(frame, height=10)
        self.text_edit.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        ttk.Label(frame, text="Voice:").pack(anchor=tk.W, padx=10, pady=5)
        self.voice_combo = ttk.Combobox(frame)
        voices = list_voices()
        self.voice_combo['values'] = [v.name for v in voices]
        if voices:
            self.voice_combo.current(0)
        self.voice_combo.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(frame, text="Output:").pack(anchor=tk.W, padx=10, pady=5)
        self.output_edit = ttk.Entry(frame)
        self.output_edit.insert(0, "output.mp3")
        self.output_edit.pack(fill=tk.X, padx=10, pady=5)

        self.synth_button = ttk.Button(frame, text="Synthesize", command=self.on_synth)
        self.synth_button.pack(pady=10)
        self.synth_button.focus_set()  # Initial focus

    def create_voice_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Voice Manager")

        self.voice_list = tk.Listbox(frame)
        self.voice_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.update_voice_list()

        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(button_frame, text="Import Voice", command=self.on_import_voice).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Preview", command=self.on_preview_voice).pack(side=tk.LEFT, padx=5)

    def create_queue_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Render Queue")

        self.queue_list = tk.Listbox(frame)
        self.queue_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(button_frame, text="Add to Queue", command=self.on_add_to_queue).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Start Render", command=self.on_start_render).pack(side=tk.LEFT, padx=5)

        self.progress_bar = ttk.Progressbar(frame, mode='determinate')
        self.progress_bar.pack(fill=tk.X, padx=10, pady=5)

    def create_settings_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Settings")
        ttk.Label(frame, text="Settings placeholder").pack(pady=20)

    def create_about_tab(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="About")
        ttk.Label(frame, text="Offline TTS v1.0.0").pack(pady=20)

    def on_synth(self):
        text = self.text_edit.get("1.0", tk.END).strip()
        voice = self.voice_combo.get()
        output = self.output_edit.get()
        if not text or not voice:
            messagebox.showerror("Error", "Text and voice are required")
            return
        args = ['synth', '--text', text, '--voice', voice, '--out', output]
        self.synth_button.config(state=tk.DISABLED)
        worker = SynthWorker(args, self.on_synth_finished)
        worker.start()

    def on_synth_finished(self, message):
        self.synth_button.config(state=tk.NORMAL)
        messagebox.showinfo("Result", message)

    def on_import_voice(self):
        file_path = filedialog.askopenfilename(title="Select Embedding File")
        if file_path:
            name = simpledialog.askstring("Voice Name", "Enter voice name:")
            if name:
                args = ['import-voice', file_path, '--name', name]
                run_cli(args)
                self.update_voice_list()

    def on_preview_voice(self):
        selection = self.voice_list.curselection()
        if selection:
            voice = self.voice_list.get(selection[0]).split()[0]
            args = ['preview-voice', voice]
            run_cli(args)

    def on_add_to_queue(self):
        file_path = filedialog.askopenfilename(title="Select Text File")
        if file_path:
            self.queue_list.insert(tk.END, file_path)

    def on_start_render(self):
        self.progress_bar['value'] = 0
        total = self.queue_list.size()
        for i in range(total):
            file_path = self.queue_list.get(i)
            output_path = file_path.replace('.txt', '.mp3')
            args = ['synth-file', file_path, '--out', output_path]
            run_cli(args)
            self.progress_bar['value'] = (i + 1) / total * 100
        messagebox.showinfo("Render", "Batch rendering completed")

    def update_voice_list(self):
        self.voice_list.delete(0, tk.END)
        voices = list_voices()
        for v in voices:
            self.voice_list.insert(tk.END, f"{v.name} ({v.gender}, {v.locale})")

def gui_main():
    app = MainWindow()
    app.mainloop()