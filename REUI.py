import sys
import os
import re
import threading
import subprocess
import json
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QTextEdit, QTableWidget, QTableWidgetItem, QLabel, QHBoxLayout, QSplitter
)
from PySide6.QtCore import QTimer, Qt

# Matplotlib integration
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

EXE_NAME = "testproj.exe"  # adjust path if needed

# Regex map for parsing the human-readable output (fallback)
FIELD_REGEX = {
    "Games": re.compile(r"Games:\s*(\d+)"),
    "At Bats": re.compile(r"At Bats:\s*(\d+)"),
    "Runs": re.compile(r"Runs:\s*(\d+)"),
    "Hits": re.compile(r"Hits:\s*(\d+)"),
    "Total Bases": re.compile(r"Total Bases:\s*(\d+)"),
    "Doubles": re.compile(r"Doubles:\s*(\d+)"),
    "Triples": re.compile(r"Triples:\s*(\d+)"),
    "Home Runs": re.compile(r"Home Runs:\s*(\d+)"),
    "RBI": re.compile(r"Runs Batted In:\s*(\d+)"),
    "Walks": re.compile(r"Walks:\s*(\d+)"),
    "Intentional Walks": re.compile(r"Intentional Walks:\s*(\d+)"),
    "Strike Outs": re.compile(r"Strike Outs:\s*(\d+)"),
    "Stolen Bases": re.compile(r"Stolen Bases:\s*(\d+)"),
    "Caught Stealing": re.compile(r"Caught Stealing:\s*(\d+)"),
    "Plate Appearances": re.compile(r"Plate Appearances:\s*(\d+)"),
    "Extra Base Hits": re.compile(r"Extra Base Hits:\s*(\d+)"),
    "Hit by Pitch": re.compile(r"Hit by Pitch:\s*(\d+)"),
}


def parse_stats_text(text: str) -> dict:
    result = {}
    for name, rx in FIELD_REGEX.items():
        m = rx.search(text)
        if m:
            try:
                result[name] = int(m.group(1))
            except ValueError:
                try:
                    result[name] = float(m.group(1))
                except ValueError:
                    result[name] = m.group(1)
    # Derived
    if "Hits" in result and "At Bats" in result and result.get("At Bats", 0) > 0:
        result["AVG"] = round(result["Hits"] / result["At Bats"], 3)
    return result


def try_parse_json(text: str):
    try:
        return json.loads(text)
    except Exception:
        return None


class MainWindow(QWidget):
    def __init__(self, exe_path: Path):
        super().__init__()
        self.exe_path = exe_path
        self.setWindowTitle("C++ Baseball Stats Viewer")
        self.resize(1000, 700)

        layout = QVBoxLayout(self)

        hl = QHBoxLayout()
        self.run_btn = QPushButton("Run testproj.exe")
        self.run_btn.clicked.connect(self.run_exe)
        hl.addWidget(self.run_btn)

        self.json_btn = QPushButton("Run with --json")
        self.json_btn.clicked.connect(lambda: self.run_exe(json_mode=True))
        hl.addWidget(self.json_btn)

        self.status_label = QLabel("")
        hl.addWidget(self.status_label)
        hl.addStretch()
        layout.addLayout(hl)

        splitter = QSplitter(Qt.Vertical)

        # Top: raw output + parsed table
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)

        self.out_view = QTextEdit()
        self.out_view.setReadOnly(True)
        top_layout.addWidget(self.out_view, 2)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Field", "Value"])
        top_layout.addWidget(self.table, 1)

        splitter.addWidget(top_widget)

        # Bottom: matplotlib canvas for basic visualizations
        fig = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(fig)
        self.ax = fig.add_subplot(111)
        splitter.addWidget(self.canvas)

        layout.addWidget(splitter)

        # A small queue + timer to receive results from background thread
        self._result_queue = []
        self.timer = QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self._poll_queue)
        self.timer.start()

    def _poll_queue(self):
        if not self._result_queue:
            return
        raw, parsed = self._result_queue.pop(0)
        self.out_view.setPlainText(raw)
        self._fill_table(parsed)
        self._draw_chart(parsed)
        self.status_label.setText("Last run: OK")

    def _fill_table(self, parsed: dict):
        self.table.setRowCount(0)
        for k, v in sorted(parsed.items()):
            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(str(k)))
            self.table.setItem(r, 1, QTableWidgetItem(str(v)))

    def _draw_chart(self, parsed: dict):
        # Draw a small bar chart for AVG/OBP/SLG/OPS if present
        keys = ["AVG", "OBP", "SLG", "OPS"]
        values = []
        labels = []
        for k in keys:
            if k in parsed:
                labels.append(k)
                values.append(float(parsed[k]))
        self.ax.clear()
        if values:
            self.ax.bar(labels, values, color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"])  # sample colors
            self.ax.set_ylim(0, max(1.0, max(values) * 1.2))
            self.ax.set_ylabel("Value")
            self.ax.set_title("Key Rate Stats")
        else:
            self.ax.text(0.5, 0.5, "No rate stats to plot", ha="center", va="center")
        self.canvas.draw()

    def run_exe(self, json_mode: bool = False):
        self.run_btn.setEnabled(False)
        self.json_btn.setEnabled(False)
        self.status_label.setText("Running...")
        thread = threading.Thread(target=self._run_worker, args=(json_mode,), daemon=True)
        thread.start()

    def _run_worker(self, json_mode: bool):
        try:
            args = [str(self.exe_path)]
            if json_mode:
                args.append("--json")
            proc = subprocess.run(args, capture_output=True, text=True, timeout=10)
            raw = proc.stdout + ("\nERR:\n" + proc.stderr if proc.stderr else "")

            parsed = None
            # Prefer JSON if available
            if json_mode:
                parsed = try_parse_json(proc.stdout)
            if parsed is None:
                # try to find JSON anywhere in stdout
                parsed = try_parse_json(proc.stdout.strip())
            if parsed is None:
                # fall back to text parsing
                parsed = parse_stats_text(raw)

        except Exception as e:
            raw = f"Exception running exe: {e}"
            parsed = {}

        self._result_queue.append((raw, parsed))
        # Re-enable the buttons on the main thread via queue+timer
        self.run_btn.setEnabled(True)
        self.json_btn.setEnabled(True)


def find_exe():
    here = Path(__file__).resolve().parent
    cand = here / EXE_NAME
    if cand.exists():
        return cand
    cand = Path.cwd() / EXE_NAME
    if cand.exists():
        return cand
    fallback = Path(r"c:\Users\cjhar\Documents\Roman_Empire\testproj.exe")
    if fallback.exists():
        return fallback
    raise FileNotFoundError(f"{EXE_NAME} not found. Put it next to this script or update the path.")


if __name__ == "__main__":
    try:
        exe_path = find_exe()
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
    app = QApplication(sys.argv)
    w = MainWindow(exe_path)
    w.show()
    sys.exit(app.exec())
