import customtkinter as ctk

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, app_instance):
        super().__init__(parent, fg_color="transparent")
        
        self.app = app_instance # Simpan referensi ke aplikasi utama

        # --- FONT ---
        self.page_title_font = ctk.CTkFont(family="Segoe UI", size=24, weight="bold")
        self.default_font = ctk.CTkFont(family="Segoe UI", size=14)
        self.section_font = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")

        # --- KONTEN HALAMAN PENGATURAN ---
        ctk.CTkLabel(self, text="Settings", font=self.page_title_font).pack(pady=20, padx=20, anchor="w")

        # --- Bagian Tampilan (Appearance) ---
        ctk.CTkLabel(self, text="Appearance", font=self.section_font).pack(padx=20, anchor="w")
        
        self.theme_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.theme_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(self.theme_frame, text="Theme", font=self.default_font).pack(side="left")
        
        self.theme_button = ctk.CTkButton(
            self.theme_frame,
            width=150,
            command=self.app._toggle_theme # Panggil fungsi di aplikasi utama
        )
        self.theme_button.pack(side="right")
        
        # --- Bagian Info Aplikasi ---
        self.separator = ctk.CTkFrame(self, height=2)
        self.separator.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(self, text="Version: 1.0.0", font=self.default_font, text_color="gray").pack(padx=20, anchor="w")

        # Inisialisasi teks tombol dan warna saat pertama kali dibuat
        self.update_theme_elements()

    def update_theme_elements(self):
        """Memperbarui teks tombol tema dan warna elemen lain."""
        theme_text = f"Switch to {'Light' if self.app.appearance_mode == 'Dark' else 'Dark'} Mode"
        self.theme_button.configure(text=theme_text)
        
        # Ambil warna separator dari dictionary warna di aplikasi utama
        separator_color = self.app.SEPARATOR_COLOR[self.app.appearance_mode]
        self.separator.configure(fg_color=separator_color)