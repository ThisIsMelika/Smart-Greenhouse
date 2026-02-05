import json
import os
import sqlite3
from dataclasses import dataclass
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# --- Constants & Settings ---
PROJECT_TITLE = "سیستم مانیتورینگ گلخانه هوشمند"
GROUP_MEMBERS = ["Melika Bagheri"]
OUTPUT_FILE = "environment_records.jsonl"
DB_FILE = "greenhouse.db"

# Colors for Greenhouse Theme
COLOR_PRIMARY = "#2e7d32"   # Dark Green
COLOR_ACCENT = "#4caf50"    # Fresh Green
COLOR_BG = "#f1f8e9"        # Light Greenish Background
COLOR_TEXT = "#1b5e20"      # Dark Forest Text

SENSOR_UNITS = {
    "temperature": "°C",
    "humidity": "%",
    "co2": "ppm",
    "light": "lux",
}
SENSOR_TYPES = list(SENSOR_UNITS.keys())


@dataclass
class SensorReading:
    greenhouse_id: str
    greenhouse_name: str
    zone_id: str
    zone_name: str
    sensor_id: str
    sensor_type: str
    unit: str
    value: float
    timestamp: str
    threshold_min: float
    threshold_max: float


class Repository:
    def __init__(self, jsonl_path: str, sqlite_path: str):
        self.jsonl_path = jsonl_path
        self.sqlite_path = sqlite_path
        self._init_db_once()

    def _init_db_once(self) -> None:
        with sqlite3.connect(self.sqlite_path) as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS sensor_readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    greenhouse_id TEXT,
                    greenhouse_name TEXT,
                    zone_id TEXT,
                    zone_name TEXT,
                    sensor_id TEXT,
                    sensor_type TEXT,
                    unit TEXT,
                    value REAL,
                    timestamp TEXT,
                    threshold_min REAL,
                    threshold_max REAL
                )
            """)

    def save_to_file(self, reading: SensorReading) -> None:
        with open(self.jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(reading.__dict__, ensure_ascii=False) + "\n")

    def save_to_db(self, reading: SensorReading) -> None:
        with sqlite3.connect(self.sqlite_path) as con:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO sensor_readings (
                    greenhouse_id, greenhouse_name, zone_id, zone_name,
                    sensor_id, sensor_type, unit, value, timestamp,
                    threshold_min, threshold_max
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                reading.greenhouse_id,
                reading.greenhouse_name,
                reading.zone_id,
                reading.zone_name,
                reading.sensor_id,
                reading.sensor_type,
                reading.unit,
                reading.value,
                reading.timestamp,
                reading.threshold_min,
                reading.threshold_max
            ))
            con.commit()

    def fetch_latest(self, limit: int = 15):
        if not os.path.exists(self.sqlite_path):
            return []
        with sqlite3.connect(self.sqlite_path) as con:
            cur = con.cursor()
            cur.execute("""
                SELECT greenhouse_name, zone_name, sensor_id, sensor_type,
                       value, unit, timestamp
                FROM sensor_readings
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
            return cur.fetchall()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Greenhouse Monitor")
        self.geometry("1000x650")
        self.configure(bg=COLOR_BG)

        self.repo = Repository(OUTPUT_FILE, DB_FILE)
        self._init_vars()
        self._apply_style()
        self._build_ui()
        self._refresh_table()

    def _init_vars(self):
        self.vars = {
            "gh_id": tk.StringVar(),
            "gh_name": tk.StringVar(),
            "z_id": tk.StringVar(),
            "z_name": tk.StringVar(),
            "s_id": tk.StringVar(),
            "s_type": tk.StringVar(value="temperature"),
            "unit": tk.StringVar(value="°C"),
            "val": tk.StringVar(),
            "min": tk.StringVar(),
            "max": tk.StringVar(),
            "db_flag": tk.BooleanVar(value=True)
        }
        self.vars["s_type"].trace_add("write", self._auto_unit)

    def _auto_unit(self, *args):
        t = self.vars["s_type"].get()
        self.vars["unit"].set(SENSOR_UNITS.get(t, ""))

    def _now_str(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _apply_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background=COLOR_BG)
        style.configure("TLabelframe", background=COLOR_BG, bordercolor=COLOR_PRIMARY)
        style.configure("TLabelframe.Label", background=COLOR_BG, foreground=COLOR_PRIMARY, font=("Segoe UI", 10, "bold"))

        style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), foreground=COLOR_PRIMARY, background=COLOR_BG)
        style.configure("TLabel", background=COLOR_BG, foreground="#333", font=("Segoe UI", 9))

        style.configure("Accent.TButton", font=("Segoe UI", 9, "bold"), background=COLOR_PRIMARY, foreground="white")
        style.map("Accent.TButton", background=[('active', COLOR_ACCENT)])

        style.configure("Treeview", rowheight=25, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#e0e0e0")

    def _build_ui(self):
        container = ttk.Frame(self, padding=20)
        container.pack(fill="both", expand=True)

        # Header
        header = ttk.Frame(container)
        header.pack(fill="x", pady=(0, 20))
        ttk.Label(header, text="🌿 " + PROJECT_TITLE, style="Header.TLabel").pack(side="left")
        ttk.Label(header, text=f"اپراتور: {', '.join(GROUP_MEMBERS)}", foreground="#666").pack(side="right", pady=10)

        # Main Layout
        main_content = ttk.Frame(container)
        main_content.pack(fill="both", expand=True)

        # Form Section
        form_frame = ttk.Labelframe(main_content, text=" ورودی اطلاعات سنسور ", padding=15)
        form_frame.pack(side="left", fill="y", padx=(0, 15))

        grid_params = {'padx': 5, 'pady': 5, 'sticky': 'w'}

        fields = [
            ("شناسه گلخانه:", self.vars["gh_id"]),
            ("نام گلخانه:", self.vars["gh_name"]),
            ("شناسه ناحیه:", self.vars["z_id"]),
            ("نام ناحیه:", self.vars["z_name"]),
            ("شناسه سنسور:", self.vars["s_id"]),
        ]

        for i, (txt, var) in enumerate(fields):
            ttk.Label(form_frame, text=txt).grid(row=i, column=0, **grid_params)
            ttk.Entry(form_frame, textvariable=var, width=25).grid(row=i, column=1, pady=5)

        ttk.Label(form_frame, text="نوع سنسور:").grid(row=5, column=0, **grid_params)
        ttk.Combobox(form_frame, textvariable=self.vars["s_type"], values=SENSOR_TYPES, state="readonly", width=23).grid(row=5, column=1)

        ttk.Label(form_frame, text="مقدار عددی:").grid(row=6, column=0, **grid_params)
        ttk.Entry(form_frame, textvariable=self.vars["val"], width=25).grid(row=6, column=1)

        # Thresholds
        thresh_frame = ttk.Frame(form_frame)
        thresh_frame.grid(row=7, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Label(thresh_frame, text="بازه مجاز: از").pack(side="left")
        ttk.Entry(thresh_frame, textvariable=self.vars["min"], width=7).pack(side="left", padx=5)
        ttk.Label(thresh_frame, text="تا").pack(side="left")
        ttk.Entry(thresh_frame, textvariable=self.vars["max"], width=7).pack(side="left", padx=5)

        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=9, column=0, columnspan=2, pady=20, sticky="ew")
        ttk.Button(btn_frame, text="ثبت داده", style="Accent.TButton", command=self.on_save).pack(fill="x", pady=2)
        ttk.Button(btn_frame, text="پاک کردن فرم", command=self.on_clear).pack(fill="x", pady=2)

        ttk.Checkbutton(form_frame, text="ذخیره در دیتابیس (SQLite)", variable=self.vars["db_flag"]).grid(row=10, column=0, columnspan=2, pady=10)

        # Table Section
        table_frame = ttk.Labelframe(main_content, text=" آخرین وضعیت سنسورها ", padding=10)
        table_frame.pack(side="right", fill="both", expand=True)

        cols = ("gh_name", "zone_name", "sid", "type", "val", "unit", "time")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")

        headings = ["نام گلخانه", "نام ناحیه", "سنسور", "نوع", "مقدار", "واحد", "زمان ثبت"]
        for col, head in zip(cols, headings):
            self.tree.heading(col, text=head)
            self.tree.column(col, width=110, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # Status Bar
        self.status_bar = ttk.Label(self, text="آماده به کار", relief="sunken", anchor="w", padding=5)
        self.status_bar.pack(side="bottom", fill="x")

    def on_save(self):
        try:
            # Basic validation
            required = ["gh_id", "gh_name", "z_id", "z_name", "s_id", "val", "min", "max"]
            for key in required:
                if not self.vars[key].get().strip():
                    raise ValueError(f"فیلد {key} نمی‌تواند خالی باشد")

            val = float(self.vars["val"].get())
            t_min = float(self.vars["min"].get())
            t_max = float(self.vars["max"].get())

            reading = SensorReading(
                greenhouse_id=self.vars["gh_id"].get(),
                greenhouse_name=self.vars["gh_name"].get(),
                zone_id=self.vars["z_id"].get(),
                zone_name=self.vars["z_name"].get(),
                sensor_id=self.vars["s_id"].get(),
                sensor_type=self.vars["s_type"].get(),
                unit=self.vars["unit"].get(),
                value=val,
                timestamp=self._now_str(),
                threshold_min=t_min,
                threshold_max=t_max
            )

            self.repo.save_to_file(reading)
            if self.vars["db_flag"].get():
                self.repo.save_to_db(reading)

            if not (t_min <= val <= t_max):
                messagebox.showwarning("هشدار بحرانی", f"مقدار سنسور ({val}) خارج از بازه مجاز است!")

            self._refresh_table()
            self.status_bar.config(text=f"آخرین ثبت موفق: {reading.timestamp}")

        except ValueError as e:
            messagebox.showerror("خطا", str(e) or "لطفاً مقادیر عددی را به درستی وارد کنید.")

    def on_clear(self):
        for key in ["gh_id", "gh_name", "z_id", "z_name", "s_id", "val", "min", "max"]:
            self.vars[key].set("")
        self.vars["s_type"].set("temperature")

    def _refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in self.repo.fetch_latest():
            self.tree.insert("", "end", values=row)


if __name__ == "__main__":
    app = App()
    app.mainloop()