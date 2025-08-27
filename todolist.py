import customtkinter as ctk
import os
import json
from datetime import date, datetime, timedelta
from tkcalendar import DateEntry
from tkinter import ttk

# Pastikan file-file ini ada di folder yang sama
from settings_page import SettingsPage
from college_page import CollegePage
from group_tasks_page import GroupTasksPage

# Nama file untuk menyimpan data
TASKS_FILE = "tasks_data.json"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("My Task Manager")
        self.geometry("400x700")

        # --- KONFIGURASI TEMA & WARNA ---
        self.appearance_mode = "Dark"; ctk.set_appearance_mode(self.appearance_mode)
        self.BACKGROUND_COLOR = {"Dark": "#242424", "Light": "#F2F2F2"}; self.PRIMARY_COLOR = {"Dark": "#1F6AA5", "Light": "#3B8ED0"}; self.TASK_FRAME_COLOR = {"Dark": "#333333", "Light": "#FFFFFF"}; self.TASK_FRAME_COMPLETED_COLOR = {"Dark": "#2B2B2B", "Light": "#F5F5F5"}; self.TEXT_COLOR = {"Dark": "#FFFFFF", "Light": "#1A1A1A"}; self.TEXT_COMPLETED_COLOR = "gray"; self.SEPARATOR_COLOR = {"Dark": "#3D3D3D", "Light": "#DCDCDC"}
        self.configure(fg_color=self.BACKGROUND_COLOR[self.appearance_mode])
        
        # --- FONT ---
        self.default_font = ctk.CTkFont(family="Segoe UI", size=14); self.strikethrough_font = ctk.CTkFont(family="Segoe UI", size=14, overstrike=True); self.deadline_font = ctk.CTkFont(family="Segoe UI", size=11, slant="italic"); self.main_header_font = ctk.CTkFont(family="Segoe UI", size=16, weight="bold"); self.page_title_font = ctk.CTkFont(family="Segoe UI", size=24, weight="bold"); self.date_header_font = ctk.CTkFont(family="Segoe UI", size=12, weight="bold")
        
        # --- STRUKTUR DATA ---
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(1, weight=1)
        self.all_tasks_data = []
        self.college_tasks = {}
        self.current_group = None
        self.menu_is_open = False
        
        # --- MEMBUAT SEMUA ELEMEN UI ---
        self._create_header_with_search()
        self._create_content_area()
        self._create_fab()
        self._create_side_menu()
        self._load_and_render_tasks()

    def _create_header_with_search(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent"); header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure(1, weight=1)
        menu_button = ctk.CTkButton(header_frame, text="☰", font=ctk.CTkFont(size=22), width=40, height=35, fg_color="transparent", hover_color="#444444", command=self._toggle_side_menu); menu_button.grid(row=0, column=0, sticky="w")
        self.search_entry = ctk.CTkEntry(header_frame, placeholder_text="🔍 Search task...", height=35, border_width=1); self.search_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        self.search_entry.bind("<KeyRelease>", self._filter_tasks)

    def _create_content_area(self):
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=0)
        self.content_container.grid_rowconfigure(0, weight=1); self.content_container.grid_columnconfigure(0, weight=1)

        self.tasks_page_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        self.settings_page_frame = SettingsPage(parent=self.content_container, app_instance=self)
        self.college_page_frame = CollegePage(parent=self.content_container, app_instance=self)
        self.group_tasks_page_frame = GroupTasksPage(parent=self.content_container, app_instance=self)

        self.tasks_page_frame.grid(row=0, column=0, sticky="nsew")
        self.settings_page_frame.grid(row=0, column=0, sticky="nsew")
        self.college_page_frame.grid(row=0, column=0, sticky="nsew")
        self.group_tasks_page_frame.grid(row=0, column=0, sticky="nsew")

        self._populate_tasks_page()
        self._show_page(self.tasks_page_frame)
        
    def _populate_tasks_page(self):
        self.content_frame = ctk.CTkScrollableFrame(self.tasks_page_frame, fg_color="transparent")
        self.content_frame.pack(expand=True, fill="both")
        self.placeholder_label = ctk.CTkLabel(self.content_frame, text="Tidak ada tugas saat ini.\nKlik '+' untuk menambahkan.", font=self.default_font, text_color="gray")

    def _create_side_menu(self):
        self.side_menu = ctk.CTkFrame(self, width=250, corner_radius=0, border_width=2)
        self.side_menu.place(x=-250, y=0, relheight=1.0)
        menu_header_frame = ctk.CTkFrame(self.side_menu, fg_color="transparent"); menu_header_frame.pack(fill="x", padx=10, pady=10)
        close_menu_button = ctk.CTkButton(menu_header_frame, text="☰", font=ctk.CTkFont(size=22), width=40, height=35, fg_color="transparent", hover_color="#444444", command=self._toggle_side_menu); close_menu_button.pack(side="left")
        ctk.CTkLabel(menu_header_frame, text="Menu", font=self.main_header_font).pack(side="left", padx=10)
        
        all_tasks_button = ctk.CTkButton(self.side_menu, text="All Tasks", anchor="w", fg_color="transparent", height=40)
        all_tasks_button.configure(command=lambda: self._navigate_to(self.tasks_page_frame, all_tasks_button))
        all_tasks_button.pack(fill="x", padx=10)
        
        college_button = ctk.CTkButton(self.side_menu, text="Tugas Kuliah", anchor="w", fg_color="transparent", height=40)
        college_button.configure(command=lambda: self._navigate_to(self.college_page_frame, college_button))
        college_button.pack(fill="x", padx=10)

        settings_button = ctk.CTkButton(self.side_menu, text="Settings", anchor="w", fg_color="transparent", height=40)
        settings_button.configure(command=lambda: self._navigate_to(self.settings_page_frame, settings_button))
        settings_button.pack(fill="x", padx=10)
        
    def _toggle_side_menu(self):
        if self.menu_is_open:
            # Tutup menu (geser ke kiri)
            self.side_menu.place(x=-250, y=0, relheight=1.0)
            self.menu_is_open = False
        else:
            # Buka menu (geser ke kanan)
            self.side_menu.place(x=0, y=0, relheight=1.0)
            self.menu_is_open = True

    def _show_page(self, page_frame):
    # Sembunyikan semua frame di dalam content_container
        for frame in (self.tasks_page_frame, self.settings_page_frame, self.college_page_frame, self.group_tasks_page_frame):
            frame.grid_forget()
        # Tampilkan frame yang dipilih
        page_frame.grid(row=0, column=0, sticky="nsew")


    def _navigate_to_group(self, group_name):
        self.current_group = group_name
        self._show_page(self.group_tasks_page_frame)
        self.group_tasks_page_frame.render_tasks_for_group(group_name)
        self.fab_button.place(relx=0.95, rely=0.95, anchor="se")

    def _navigate_to(self, page_frame, button):
        self._show_page(page_frame)
        if self.menu_is_open:
            self._toggle_side_menu()

        if page_frame == self.college_page_frame:
            self.fab_button.place_forget()
        else:
            self.fab_button.place(relx=0.95, rely=0.95, anchor="se")
            self.current_group = None

        for child in self.side_menu.winfo_children():
            if isinstance(child, ctk.CTkButton):
                child.configure(fg_color="transparent")
        if button:
            button.configure(fg_color="#333333")

    def create_new_group(self, group_name):
        if group_name not in self.college_tasks:
            self.college_tasks[group_name] = []
            self._save_tasks()
            self.college_page_frame.render_groups()

    def delete_group(self, group_name):
        if group_name in self.college_tasks:
            del self.college_tasks[group_name]
            self._save_tasks()
            self.college_page_frame.render_groups() # Render ulang halaman grup

    def add_task_from_popup(self, task_entry, date_picker, hour_var, minute_var, window):
        task_text = task_entry.get().strip()
        if not task_text: return
        selected_date = date_picker.get_date(); selected_hour = int(hour_var.get()); selected_minute = int(minute_var.get())
        deadline_dt = datetime(selected_date.year, selected_date.month, selected_date.day, selected_hour, selected_minute)
        new_task_data = {'text': task_text, 'deadline': deadline_dt, 'is_checked': False, 'id': os.urandom(4).hex()}

        if self.current_group:
            self.college_tasks.setdefault(self.current_group, []).append(new_task_data)
        else:
            self.all_tasks_data.append(new_task_data)
        
        self._save_and_refresh_ui(self.current_group)
        window.destroy()

    def _save_tasks(self):
        all_data = { "personal_tasks": self.all_tasks_data, "college_tasks": self.college_tasks }
        with open(TASKS_FILE, "w") as f:
            json.dump(all_data, f, indent=4, default=str)

    def _load_and_render_tasks(self):
        if os.path.exists(TASKS_FILE):
            try:
                with open(TASKS_FILE, "r") as f:
                    all_data = json.load(f)
                    self.all_tasks_data = all_data.get("personal_tasks", [])
                    for task in self.all_tasks_data:
                        task['deadline'] = datetime.fromisoformat(task['deadline'])
                    self.college_tasks = all_data.get("college_tasks", {})
                    for group in self.college_tasks:
                        for task in self.college_tasks[group]:
                            task['deadline'] = datetime.fromisoformat(task['deadline'])
            except (json.JSONDecodeError, TypeError):
                self.all_tasks_data = []; self.college_tasks = {}
        self._render_all_tasks()
        self.college_page_frame.render_groups()
    
    def _create_task_widget(self, parent_frame, task_info, group_name=None):
        task_frame = ctk.CTkFrame(parent_frame, fg_color=self.TASK_FRAME_COLOR[self.appearance_mode]); task_frame.pack(fill="x", padx=5, pady=4); task_frame.grid_columnconfigure(0, weight=1)
        text_frame = ctk.CTkFrame(task_frame, fg_color="transparent"); text_frame.grid(row=0, column=0, sticky="ew", padx=(15, 5), pady=(5,5))
        task_label = ctk.CTkLabel(text_frame, text=task_info['text'], font=self.default_font, anchor="w"); task_label.pack(fill="x")
        deadline_label = ctk.CTkLabel(text_frame, text=f"Deadline: {task_info['deadline'].strftime('%H:%M')}", font=self.deadline_font, text_color="gray", anchor="w"); deadline_label.pack(fill="x")
        options_button = ctk.CTkButton(task_frame, text="⋮", width=28, height=28, font=ctk.CTkFont(size=20), text_color="gray", fg_color="transparent", hover_color="#444444"); options_button.grid(row=0, column=1, sticky="e", padx=(0, 10))
        task_info['widgets'] = {'frame': task_frame, 'label': task_label, 'deadline_label': deadline_label}
        options_button.configure(command=lambda info=task_info, btn=options_button: self._show_task_options_menu(info, btn, group_name)); self._update_task_appearance(task_info)
    
    def _show_task_options_menu(self, task_info, button, group_name=None):
        menu = ctk.CTkToplevel(self); menu.overrideredirect(True); menu_frame = ctk.CTkFrame(menu, corner_radius=8, border_width=1, border_color="#555555"); menu_frame.pack()
        toggle_text = "Batal tandai" if task_info['is_checked'] else "Tandai selesai"; toggle_button = ctk.CTkButton(menu_frame, text=toggle_text, fg_color="transparent", anchor="w", command=lambda: (self._toggle_task_completion(task_info, group_name), menu.destroy())); toggle_button.pack(fill="x", padx=5, pady=5)
        delete_button = ctk.CTkButton(menu_frame, text="Hapus", fg_color="transparent", text_color="#F47174", anchor="w", command=lambda: (self._delete_task(task_info, group_name), menu.destroy())); delete_button.pack(fill="x", padx=5, pady=(0, 5))
        x = button.winfo_rootx() - menu.winfo_width() + 40; y = button.winfo_rooty() + button.winfo_height(); menu.geometry(f"+{x}+{y}")
        menu.bind("<FocusOut>", lambda event: menu.destroy())

    def _toggle_task_completion(self, task_info, group_name=None):
        task_info['is_checked'] = not task_info['is_checked']; self._save_and_refresh_ui(group_name)

    def _delete_task(self, task_info_to_delete, group_name=None):
        if group_name:
            if task_info_to_delete in self.college_tasks[group_name]:
                self.college_tasks[group_name].remove(task_info_to_delete)
        else:
            if task_info_to_delete in self.all_tasks_data:
                self.all_tasks_data.remove(task_info_to_delete)
        self._save_and_refresh_ui(group_name)

    def _save_and_refresh_ui(self, group_name=None):
        self._save_tasks()
        if group_name:
            self.group_tasks_page_frame.render_tasks_for_group(group_name)
        else:
            self._render_all_tasks()
        self.college_page_frame.render_groups()

    def _render_all_tasks(self):
        parent_frame = self.content_frame;
        for widget in parent_frame.winfo_children(): widget.destroy()
        tasks_list = self.all_tasks_data
        if not tasks_list:
            placeholder_label = ctk.CTkLabel(self.content_frame, text="Tidak ada tugas saat ini.\nKlik '+' untuk menambahkan.", font=self.default_font, text_color="gray")
            placeholder_label.pack(expand=True, pady=50)
            return
        
        incomplete_tasks = sorted([t for t in tasks_list if not t['is_checked']], key=lambda x: x['deadline'])
        completed_tasks = sorted([t for t in tasks_list if t['is_checked']], key=lambda x: x['deadline'], reverse=True)
        if incomplete_tasks:
            ctk.CTkLabel(parent_frame, text="Tasks to do", font=self.main_header_font, anchor="w").pack(fill="x", padx=5, pady=(5,10))
            last_date_obj = None
            for task_info in incomplete_tasks:
                date_obj = task_info['deadline'].date()
                if date_obj != last_date_obj:
                    formatted_date = self._format_date_header(date_obj)
                    ctk.CTkLabel(parent_frame, text=formatted_date, font=self.date_header_font, text_color="gray").pack(fill="x", padx=5, pady=(15, 5), anchor="w"); last_date_obj = date_obj
                self._create_task_widget(parent_frame, task_info)
        if completed_tasks:
            ctk.CTkFrame(parent_frame, height=2, fg_color=self.SEPARATOR_COLOR[self.appearance_mode]).pack(fill="x", padx=5, pady=20)
            ctk.CTkLabel(parent_frame, text="Completed", font=self.main_header_font, anchor="w").pack(fill="x", padx=5, pady=(0,10))
            last_date_obj = None
            for task_info in completed_tasks:
                date_obj = task_info['deadline'].date()
                if date_obj != last_date_obj:
                    formatted_date = self._format_date_header(date_obj)
                    ctk.CTkLabel(parent_frame, text=formatted_date, font=self.date_header_font, text_color="gray").pack(fill="x", padx=5, pady=(15, 5), anchor="w"); last_date_obj = date_obj
                self._create_task_widget(parent_frame, task_info)
    
    def _create_fab(self):
        self.fab_button = ctk.CTkButton(
            self,
            text="+",
            font=ctk.CTkFont(size=28, weight="bold"),
            width=55,
            height=55,
            corner_radius=30,
            fg_color=self.PRIMARY_COLOR[self.appearance_mode],  # ✅ fix di sini
            command=self.open_add_task_window
        )
        self.fab_button.place(relx=0.95, rely=0.95, anchor="se")
    
    def _toggle_theme(self):
        self.appearance_mode = "Light" if self.appearance_mode == "Dark" else "Dark"
        ctk.set_appearance_mode(self.appearance_mode)
        self.configure(fg_color=self.BACKGROUND_COLOR[self.appearance_mode])
        self.fab_button.configure(fg_color=self.PRIMARY_COLOR[self.appearance_mode])
        self.side_menu.configure(border_color=self.SEPARATOR_COLOR[self.appearance_mode])
        self.settings_page_frame.update_theme_elements()
        self._render_all_tasks()
        self.college_page_frame.render_groups()
        if self.current_group:
            self.group_tasks_page_frame.render_tasks_for_group(self.current_group)
        
    def _update_task_appearance(self, task_info):
        widgets = task_info.get('widgets');
        if not widgets: return
        if task_info['is_checked']:
            widgets['label'].configure(font=self.strikethrough_font, text_color=self.TEXT_COMPLETED_COLOR); widgets['deadline_label'].configure(text_color=self.TEXT_COMPLETED_COLOR); widgets['frame'].configure(fg_color=self.TASK_FRAME_COMPLETED_COLOR[self.appearance_mode])
        else:
            widgets['label'].configure(font=self.default_font, text_color=self.TEXT_COLOR[self.appearance_mode]); widgets['deadline_label'].configure(text_color="gray"); widgets['frame'].configure(fg_color=self.TASK_FRAME_COLOR[self.appearance_mode])
            
    def _filter_tasks(self, event=None):
        search_term = self.search_entry.get().lower()
        active_page_tasks = []
        if self.tasks_page_frame.winfo_viewable():
            active_page_tasks = self.all_tasks_data
        elif self.group_tasks_page_frame.winfo_viewable() and self.current_group:
            active_page_tasks = self.college_tasks.get(self.current_group, [])

        for task in active_page_tasks:
            widgets = task.get('widgets')
            if widgets and widgets['frame'].winfo_exists():
                if search_term in task['text'].lower():
                    widgets['frame'].pack(fill="x", padx=5, pady=4)
                else:
                    widgets['frame'].pack_forget()

    def render_groups(self):
        # Hapus semua widget lama dalam scrollable_frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Jika tidak ada grup, tampilkan placeholder
        if not self.groups or len(self.groups) == 0:
            placeholder_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="Belum ada grup, silakan tambahkan terlebih dahulu.",
                font=ctk.CTkFont(size=14, weight="normal")
            )
            placeholder_label.pack(expand=True, pady=50)
            return

        # Jika ada grup, render satu per satu
        for group in self.groups:
            group_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
            group_frame.pack(fill="x", pady=5, padx=10)

            group_label = ctk.CTkLabel(
                group_frame,
                text=group.get("name", "Tanpa Nama Grup"),
                font=ctk.CTkFont(size=16, weight="bold")
            )
            group_label.pack(anchor="w", padx=10, pady=5)

            # Tampilkan daftar tugas di dalam grup
            tasks = group.get("tasks", [])
            if not tasks:
                empty_label = ctk.CTkLabel(
                    group_frame,
                    text="(Belum ada tugas)",
                    font=ctk.CTkFont(size=13, slant="italic")
                )
                empty_label.pack(anchor="w", padx=20, pady=(0, 5))
            else:
                for task in tasks:
                    task_label = ctk.CTkLabel(
                        group_frame,
                        text=f"- {task}",
                        font=ctk.CTkFont(size=13)
                    )
                    task_label.pack(anchor="w", padx=20, pady=(0, 2))

    def open_add_task_window(self):
        if hasattr(self, 'add_window') and self.add_window.winfo_exists(): self.add_window.focus(); return
        self.add_window = ctk.CTkToplevel(self); self.add_window.title("Add New Task"); self.add_window.geometry("400x300"); self.add_window.transient(self); self.add_window.grab_set()
        
        main_frame = ctk.CTkFrame(self.add_window, fg_color="transparent"); main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.grid_columnconfigure(0, weight=2); main_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(main_frame, text="Task Description").grid(row=0, column=0, columnspan=2, sticky="w")
        task_entry = ctk.CTkEntry(main_frame, placeholder_text="What do you need to do?", height=35); task_entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5, 20)); task_entry.focus()
        
        ctk.CTkLabel(main_frame, text="Due Date").grid(row=2, column=0, sticky="w")
        date_picker = DateEntry(
            main_frame, date_pattern='y-mm-dd',
            background=self.TASK_FRAME_COMPLETED_COLOR[self.appearance_mode], foreground=self.TEXT_COLOR[self.appearance_mode],
            bordercolor="#444444" if self.appearance_mode == "Dark" else "#AAAAAA",
            headersbackground=self.TASK_FRAME_COMPLETED_COLOR[self.appearance_mode], normalbackground=self.TASK_FRAME_COMPLETED_COLOR[self.appearance_mode],
            weekendbackground=self.TASK_FRAME_COMPLETED_COLOR[self.appearance_mode], othermonthforeground='gray40',
            othermonthbackground=self.TASK_FRAME_COMPLETED_COLOR[self.appearance_mode], selectbackground=self.PRIMARY_COLOR[self.appearance_mode],
            selectforeground='white', arrowcolor=self.TEXT_COLOR[self.appearance_mode],
        )
        date_picker.grid(row=3, column=0, sticky="ew", pady=(5, 0), ipady=5)

        ctk.CTkLabel(main_frame, text="Time").grid(row=2, column=1, sticky="w", padx=(10, 0))
        time_frame = ctk.CTkFrame(main_frame, fg_color="transparent"); time_frame.grid(row=3, column=1, sticky="ew", padx=(10, 0), pady=(5, 0))
        time_frame.grid_columnconfigure(0, weight=1); time_frame.grid_columnconfigure(1, weight=1)
        hours = [f"{h:02d}" for h in range(24)]; minutes = [f"{m:02d}" for m in range(0, 60, 5)]; hour_var = ctk.StringVar(value="23"); minute_var = ctk.StringVar(value="55")
        hour_menu = ctk.CTkOptionMenu(time_frame, variable=hour_var, values=hours, width=80); hour_menu.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        minute_menu = ctk.CTkOptionMenu(time_frame, variable=minute_var, values=minutes, width=80); minute_menu.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        
        add_button_command = lambda: self.add_task_from_popup(task_entry, date_picker, hour_var, minute_var, self.add_window)
        button = ctk.CTkButton(main_frame, text="Add Task", height=40, command=add_button_command); button.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(30, 0))
        task_entry.bind("<Return>", lambda event: add_button_command())

    def _format_date_header(self, date_obj):
        today = date.today(); yesterday = today - timedelta(days=1)
        if date_obj == today: return f"Hari ini - {date_obj.strftime('%d %B %Y')}"
        elif date_obj == yesterday: return f"Kemarin - {date_obj.strftime('%d %B %Y')}"
        else: return date_obj.strftime('%A, %d %B %Y')

if __name__ == "__main__":
    app = App()
    app.mainloop()