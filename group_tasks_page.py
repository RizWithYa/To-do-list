import customtkinter as ctk
from datetime import date, timedelta

class GroupTasksPage(ctk.CTkFrame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, fg_color="transparent")
        self.app = app_instance

        # --- FONT ---
        self.page_title_font = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        self.main_header_font = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        self.date_header_font = ctk.CTkFont(family="Segoe UI", size=12, weight="bold")

        # --- KONTEN HALAMAN ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=20, anchor="n")
        
        # Tombol kembali
        back_button = ctk.CTkButton(self.header_frame, text="< Kembali", width=100, command=lambda: self.app._navigate_to(self.app.college_page_frame, None))
        back_button.pack(side="left")

        self.group_title_label = ctk.CTkLabel(self.header_frame, text="", font=self.page_title_font)
        self.group_title_label.pack(side="left", padx=20)
        
        # frame scrollable untuk daftar tugas grup
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_frame.pack(fill="both", expand=True)

        # di dalam scrollable_frame, buat container tasks
        self.tasks_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.tasks_frame.pack(fill="both", expand=True)
        
    def render_tasks_for_group(self, group_name):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        tasks = self.app.college_tasks.get(group_name, [])

        if not tasks:
            # buat placeholder baru setiap kali kosong
            placeholder_label = ctk.CTkLabel(
                self.tasks_frame,
                text="Belum ada tugas di grup ini.\nKlik '+' untuk menambahkan.",
                font=self.app.default_font,
                text_color="gray"
            )
            placeholder_label.pack(expand=True, pady=50)
            return

        # kalau ada tugas → render task
        incomplete_tasks = sorted([t for t in tasks if not t['is_checked']], key=lambda x: x['deadline'])
        completed_tasks = sorted([t for t in tasks if t['is_checked']], key=lambda x: x['deadline'], reverse=True)

        if incomplete_tasks:
            ctk.CTkLabel(self.tasks_frame, text="Tasks to do", font=self.app.main_header_font, anchor="w").pack(fill="x", padx=5, pady=(5,10))
            last_date_obj = None
            for task_info in incomplete_tasks:
                date_obj = task_info['deadline'].date()
                if date_obj != last_date_obj:
                    formatted_date = self.app._format_date_header(date_obj)
                    ctk.CTkLabel(self.tasks_frame, text=formatted_date, font=self.app.date_header_font, text_color="gray").pack(fill="x", padx=5, pady=(15, 5), anchor="w")
                    last_date_obj = date_obj
                self.app._create_task_widget(self.tasks_frame, task_info, group_name)

        if completed_tasks:
            ctk.CTkFrame(self.tasks_frame, height=2, fg_color=self.app.SEPARATOR_COLOR[self.app.appearance_mode]).pack(fill="x", padx=5, pady=20)
            ctk.CTkLabel(self.tasks_frame, text="Completed", font=self.app.main_header_font, anchor="w").pack(fill="x", padx=5, pady=(0,10))
            last_date_obj = None
            for task_info in completed_tasks:
                date_obj = task_info['deadline'].date()
                if date_obj != last_date_obj:
                    formatted_date = self.app._format_date_header(date_obj)
                    ctk.CTkLabel(self.tasks_frame, text=formatted_date, font=self.app.date_header_font, text_color="gray").pack(fill="x", padx=5, pady=(15, 5), anchor="w")
                    last_date_obj = date_obj
                self.app._create_task_widget(self.tasks_frame, task_info, group_name)
