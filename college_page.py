import customtkinter as ctk

class CollegePage(ctk.CTkFrame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, fg_color="transparent")
        self.app = app_instance

        self.page_title_font = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        self.group_font = ctk.CTkFont(family="Segoe UI", size=16)

        # --- KONTEN HALAMAN TUGAS KULIAH ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20, anchor="n")
        
        ctk.CTkLabel(header_frame, text="Tugas Kuliah", font=self.page_title_font).pack(side="left")
        
        # Tombol untuk menambah grup baru
        add_group_button = ctk.CTkButton(header_frame, text="+ Buat Grup", width=120, command=self.open_add_group_window)
        add_group_button.pack(side="right")

        # Frame untuk menampung daftar grup
        self.groups_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.groups_frame.pack(fill="both", expand=True, padx=20)
        
    def render_groups(self):
        """Menggambar ulang daftar grup dengan tombol opsi."""
        for widget in self.groups_frame.winfo_children():
            widget.destroy()

        if not self.app.college_tasks:
            placeholder_label = ctk.CTkLabel(
                self.groups_frame,
                text="Belum ada grup.\nBuat grup untuk mata kuliahmu!",
                text_color="gray",
                font=self.group_font
            )
            placeholder_label.pack(expand=True, pady=50)
            return

        sorted_groups = sorted(self.app.college_tasks.keys())
        
        for group_name in sorted_groups:
            # Buat frame untuk setiap baris grup
            group_row_frame = ctk.CTkFrame(
                self.groups_frame,
                fg_color=self.app.TASK_FRAME_COLOR[self.app.appearance_mode],
                height=50
            )
            group_row_frame.pack(fill="x", pady=5)
            group_row_frame.grid_columnconfigure(0, weight=1) # Agar nama grup memenuhi ruang

            # Tombol nama grup (untuk navigasi)
            group_button = ctk.CTkButton(
                group_row_frame,
                text=group_name,
                font=self.group_font,
                height=50,
                anchor="w",
                fg_color="transparent",
                command=lambda gn=group_name: self.app._navigate_to_group(gn)
            )
            group_button.grid(row=0, column=0, sticky="ew", padx=(10, 0))

            # Tombol Opsi (titik tiga)
            options_button = ctk.CTkButton(
                group_row_frame,
                text="⋮",
                font=ctk.CTkFont(size=20),
                width=30,
                height=30,
                fg_color="transparent",
                hover_color="#444444"
            )
            options_button.configure(command=lambda gn=group_name, btn=options_button: self.show_group_options_menu(gn, btn))
            options_button.grid(row=0, column=1, sticky="e", padx=(0, 10))

    def show_group_options_menu(self, group_name, button):
        """Menampilkan menu pop-up untuk opsi grup."""
        menu = ctk.CTkToplevel(self)
        menu.overrideredirect(True)
        
        menu_frame = ctk.CTkFrame(menu, corner_radius=8, border_width=1, border_color="#555555")
        menu_frame.pack()

        # Tombol Hapus Grup
        delete_button = ctk.CTkButton(
            menu_frame,
            text="Hapus Grup",
            fg_color="transparent",
            text_color="#F47174",
            anchor="w",
            command=lambda: (self.app.delete_group(group_name), menu.destroy())
        )
        delete_button.pack(fill="x", padx=5, pady=5)

        # Posisikan menu di dekat tombol opsi
        x = button.winfo_rootx() - menu.winfo_width() + 100
        y = button.winfo_rooty() + button.winfo_height()
        menu.geometry(f"+{x}+{y}")
        
        menu.bind("<FocusOut>", lambda event: menu.destroy())
        menu.focus_set()

    def open_add_group_window(self):
        """Membuka pop-up untuk membuat grup baru."""
        dialog = ctk.CTkInputDialog(text="Masukkan nama mata kuliah:", title="Buat Grup Baru")
        group_name = dialog.get_input()
        if group_name and group_name.strip():
            self.app.create_new_group(group_name.strip())