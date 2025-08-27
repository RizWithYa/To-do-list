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
        
        self.placeholder_label = ctk.CTkLabel(self.groups_frame, text="Belum ada grup.\nBuat grup untuk mata kuliahmu!", text_color="gray")
        
    def render_groups(self):
        """Menggambar ulang daftar grup."""
        for widget in self.groups_frame.winfo_children():
            widget.destroy()

        if not self.app.college_tasks:
            # Buat placeholder baru setiap kali dibutuhkan
            placeholder_label = ctk.CTkLabel(
                self.groups_frame,
                text="Belum ada grup, silakan tambahkan terlebih dahulu.",
                font=self.group_font
            )
            placeholder_label.pack(expand=True, pady=50)
            return

        # Jika ada grup, tampilkan tombol-tombol grup
        sorted_groups = sorted(self.app.college_tasks.keys())
        
        for group_name in sorted_groups:
            group_button = ctk.CTkButton(
                self.groups_frame,
                text=group_name,
                font=self.group_font,
                height=50,
                anchor="w",
                fg_color=self.app.TASK_FRAME_COLOR[self.app.appearance_mode],
                command=lambda gn=group_name: self.app._navigate_to_group(gn)
            )
            group_button.pack(fill="x", pady=5)

    def open_add_group_window(self):
        """Membuka pop-up untuk membuat grup baru."""
        dialog = ctk.CTkInputDialog(text="Masukkan nama mata kuliah:", title="Buat Grup Baru")
        group_name = dialog.get_input()
        if group_name and group_name.strip():
            self.app.create_new_group(group_name.strip())