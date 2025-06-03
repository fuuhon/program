import flet as ft
from datetime import datetime
import random
import os

class Film:
    def __init__(self, judul, sutradara, genre, durasi, tahun_rilis, deskripsi, rating, jadwal_penayangan, poster):
        self.__judul = judul
        self.__sutradara = sutradara
        self.__genre = genre
        self.__durasi = durasi
        self.__tahun_rilis = tahun_rilis
        self.__deskripsi = deskripsi
        self.__rating = rating
        self.__jadwal_penayangan = jadwal_penayangan
        self.__poster = poster

    def get_judul(self):
        return self.__judul
    def get_sutradara(self):
        return self.__sutradara
    def get_genre(self):
        return self.__genre
    def get_durasi(self):
        return self.__durasi
    def get_tahun_rilis(self):
        return self.__tahun_rilis
    def get_deskripsi(self):
        return self.__deskripsi
    def get_rating(self):
        return self.__rating
    def get_jadwal_penayangan(self):
        return self.__jadwal_penayangan
    def get_poster(self):
        return self.__poster

    def set_judul(self, judul):
        self.__judul = judul
    def set_sutradara(self, sutradara):
        self.__sutradara = sutradara
    def set_genre(self, genre):
        self.__genre = genre
    def set_durasi(self, durasi):
        self.__durasi = durasi
    def set_tahun_rilis(self, tahun_rilis):
        self.__tahun_rilis = tahun_rilis
    def set_deskripsi(self, deskripsi):
        self.__deskripsi = deskripsi
    def set_rating(self, rating):
        self.__rating = rating
    def set_jadwal_penayangan(self, jadwal_penayangan):
        self.__jadwal_penayangan = jadwal_penayangan
    def set_poster(self, poster):
        self.__poster = poster

class ListFilm:
    def __init__(self):
        self.films = []
        self.muat_film_dari_file()
        
        if len(self.films) == 0 or all(f.get_judul() == "" for f in self.films):
            self.tambah_film_default()
            self.simpan_ke_file()
    
    def muat_film_dari_file(self, nama_file="daftar1.txt"):
        try:
            with open(nama_file, 'r', encoding='utf-8') as file:
                for baris in file:
                    data = baris.strip().split('|')
                    if len(data) >= 9:
                        film = Film(
                            judul=data[0],
                            sutradara=data[1],
                            genre=data[2],
                            durasi=int(data[3]),
                            tahun_rilis=int(data[4]),
                            deskripsi=data[5],
                            rating=data[6],
                            jadwal_penayangan=data[7],
                            poster=data[8]
                        )
                        self.films.append(film)
        except FileNotFoundError:
            print("File daftar1.txt tidak ditemukan, akan dibuat saat menyimpan.")
        except Exception as e:
            print(f"Error membaca file: {e}")
    
    def tambah_film_default(self):
        default_films = [
            Film("The Shawshank Redemption", "Frank Darabont", "Drama", 142, 1994, 
                 "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.", 
                 "9.3/10", "10:00, 14:00, 18:00", "shaw.jpg"),
            Film("The Godfather", "Francis Ford Coppola", "Crime", 175, 1972, 
                 "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.", 
                 "9.2/10", "11:00, 15:00, 19:00", "shaw.jpg"),
            Film("Pulp Fiction", "Quentin Tarantino", "Crime", 154, 1994, 
                 "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.", 
                 "8.9/10", "12:00, 16:00, 20:00", "shaw.jpg")
        ]
        self.films.extend(default_films)
    
    def simpan_ke_file(self, nama_file="daftar1.txt"):
        try:
            with open(nama_file, 'w', encoding='utf-8') as file:
                for film in self.films:
                    line = "|".join([
                        film.get_judul(),
                        film.get_sutradara(),
                        film.get_genre(),
                        str(film.get_durasi()),
                        str(film.get_tahun_rilis()),
                        film.get_deskripsi(),
                        film.get_rating(),
                        film.get_jadwal_penayangan(),
                        film.get_poster()
                    ])
                    file.write(line + "\n")
        except Exception as e:
            print(f"Error menyimpan file: {e}")

class TheaterKursi:
    EMPTY = 0
    TAKEN = 1
    SELECTED = 2  # Status baru untuk kursi yang sedang dipilih
    
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.seats = [[self.EMPTY for _ in range(cols)] for _ in range(rows)]
    
    def pesan_kursi(self, baris, kolom):
        r, c = baris - 1, kolom - 1
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return False
        if self.seats[r][c] == self.TAKEN:
            return False
        self.seats[r][c] = self.TAKEN
        return True
    
    def batal_pesan(self, baris, kolom):
        r, c = baris - 1, kolom - 1
        if self.seats[r][c] == self.EMPTY:
            return False
        self.seats[r][c] = self.EMPTY
        return True
    
    def toggle_pilih(self, baris, kolom):
        r, c = baris - 1, kolom - 1
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return False
        if self.seats[r][c] == self.TAKEN:
            return False
        self.seats[r][c] = self.SELECTED if self.seats[r][c] == self.EMPTY else self.EMPTY
        return True
    
    def get_selected_seats(self):
        selected = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.seats[r][c] == self.SELECTED:
                    selected.append((r+1, c+1))
        return selected
    
    def confirm_selection(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.seats[r][c] == self.SELECTED:
                    self.seats[r][c] = self.TAKEN

class Studio:
    def __init__(self, jumlah_kursi, fasilitas):
        self.jumlah_kursi = jumlah_kursi
        self.fasilitas = fasilitas
        self.kursi = TheaterKursi(10, 15)  # Example: 10 rows, 15 columns
        self.film = None

class Premiere(Studio):
    def __init__(self, jumlah_kursi):
        super().__init__(jumlah_kursi, {"kursi premium", "selimut", "snack eksklusif", "recliner"})

class Konsumsi:
    def __init__(self):
        self.makanan = {
            "1": ("Popcorn Caramel", {"Diet": 15000, "Medium": 30000, "Jumbo": 50000}),
            "2": ("Popcorn Butter", {"Diet": 14000, "Medium": 28000, "Jumbo": 48000}),
            "3": ("Popcorn Cheese", {"Diet": 16000, "Medium": 32000, "Jumbo": 52000}),
            "4": ("Popcorn Spicy", {"Diet": 16000, "Medium": 32000, "Jumbo": 52000}),
            "5": ("Kentang Goreng Spicy", {"Diet": 17000, "Medium": 31000, "Jumbo": 45000}),
            "6": ("Kentang Goreng Umami", {"Diet": 17000, "Medium": 31000, "Jumbo": 45000}),
            "7": ("Blood Dragon Hotdog", {"Diet": 20000, "Medium": 35000, "Jumbo": 50000}),
        }
        self.minuman = {
            "1": ("Lemon Soda", {"Diet": 12000, "Medium": 20000, "Jumbo": 30000}),
            "2": ("Blood Demon Soda", {"Diet": 15000, "Medium": 23000, "Jumbo": 33000}),
            "3": ("Ice Tea", {"Diet": 10000, "Medium": 18000, "Jumbo": 25000}),
            "4": ("Heavenly Ice Cream", {"Diet": 18000, "Medium": 25000, "Jumbo": 35000}),
        }

class Konsumen:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.transaksi_history = []

class Transaksi:
    def __init__(self, username, film, tanggal_pemesanan, no_kursi, studio, tipe_tiket, konsumsi=None, voucher=None):
        self.id_transaksi = f"TRX{random.randint(1000, 9999)}"
        self.username = username
        self.film = film
        self.tanggal_pemesanan = tanggal_pemesanan
        self.no_kursi = no_kursi
        self.studio = studio
        self.tipe_tiket = tipe_tiket
        self.konsumsi = konsumsi if konsumsi else []
        self.voucher = voucher
        self.harga_tiket = 100000 if tipe_tiket.lower() == "premiere" else 50000
        self.diskon = 0.2 if voucher and voucher.lower() == "diskon20" else 0
        self.status = "Pending"
    
    def hitung_total(self):
        total = self.harga_tiket * len(self.no_kursi)  # Total harga berdasarkan jumlah kursi
        
        # Weekend surcharge
        if self.tanggal_pemesanan.strftime("%A").lower() in ["saturday", "sunday"]:
            total += 20000 * len(self.no_kursi)
        
        # Add consumables
        for item in self.konsumsi:
            total += item["harga"]
        
        # Apply discount
        total -= total * self.diskon
        
        return total
    
    def confirm_payment(self):
        self.status = "Paid"
        return True




class CinemaApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Cinema Ticket Booking System"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.window_width = 1000
        self.page.window_height = 700
        self.page.window_min_width = 800
        self.page.window_min_height = 600
        
        # Initialize data
        self.konsumen_db = [
            Konsumen("budi", "123"),
            Konsumen("alya", "password1")
        ]
        self.current_user = None
        self.list_film = ListFilm()
        self.studios = {
            "Studio 1": Studio(150, {"kursi standar"}),
            "Studio 2": Studio(150, {"kursi standar"}),
            "Studio Premiere": Premiere(100)
        }
        self.konsumsi = Konsumsi()
        self.current_transaction = None
        self.selected_seats = []
        self.selected_consumables = []
        
        # UI Components
        self.create_login_ui()

    def open_date_picker(self):
        self.date_picker.open = True
        self.page.update()

    def update_date_display(self, e):
        if self.date_picker.value:
            self.selected_date.value = self.date_picker.value.strftime("%d/%m/%Y")
            self.page.update()

    def pick_date(self, e):
        if self.date_picker.value:
            self.selected_date.value = self.date_picker.value.strftime("%d/%m/%Y")
            self.page.update()
    
    def create_login_ui(self):
        self.username_field = ft.TextField(label="Username", width=300, autofocus=True)
        self.password_field = ft.TextField(label="Password", width=300, password=True, can_reveal_password=True)
        
        login_button = ft.ElevatedButton(
            "Login",
            on_click=self.handle_login,
            width=300
        )
        
        register_button = ft.TextButton(
            "Belum punya akun? Daftar disini",
            on_click=self.show_register_dialog
        )
        
        self.login_form = ft.Column(
            [
                ft.Text("Cinema Ticket Booking", size=24, weight="bold"),
                ft.Text("Silakan login untuk melanjutkan"),
                self.username_field,
                self.password_field,
                login_button,
                register_button
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        # Register dialog
        self.register_username = ft.TextField(label="Username")
        self.register_password = ft.TextField(label="Password", password=True)
        self.register_dialog = ft.AlertDialog(
            title=ft.Text("Daftar Akun Baru"),
            content=ft.Column([
                self.register_username,
                self.register_password
            ], tight=True),
            actions=[
                ft.TextButton("Daftar", on_click=self.handle_register),
                ft.TextButton("Batal", on_click=self.close_register_dialog)
            ]
        )
        
        self.page.clean()
        self.page.add(self.login_form)
    
    def show_register_dialog(self, e):
        self.page.dialog = self.register_dialog
        self.register_dialog.open = True
        self.page.update()
    
    def close_register_dialog(self, e):
        self.register_dialog.open = False
        self.page.update()
    
    def handle_register(self, e):
        username = self.register_username.value
        password = self.register_password.value
        
        if not username or not password:
            self.page.snack_bar = ft.SnackBar(ft.Text("Username dan password harus diisi"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        if any(user.username == username for user in self.konsumen_db):
            self.page.snack_bar = ft.SnackBar(ft.Text("Username sudah digunakan"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        self.konsumen_db.append(Konsumen(username, password))
        self.close_register_dialog(e)
        self.page.snack_bar = ft.SnackBar(ft.Text("Pendaftaran berhasil! Silakan login"))
        self.page.snack_bar.open = True
        self.page.update()
    
    def handle_login(self, e):
        username = self.username_field.value
        password = self.password_field.value
        
        user = next((u for u in self.konsumen_db if u.username == username and u.password == password), None)
        
        if user:
            self.current_user = user
            self.create_main_ui()
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Username atau password salah"))
            self.page.snack_bar.open = True
            self.page.update()
    
    def logout(self, e):
        self.current_user = None
        self.create_login_ui()
    
    def create_main_ui(self):
        self.film_list_view = ft.ListView(expand=True)
        self.update_film_list()
        
        self.tab_menu = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Film",
                    icon=ft.Icons.MOVIE,
                    content=self.film_list_view
                ),
                ft.Tab(
                    text="Pesan Tiket",
                    icon=ft.Icons.CONFIRMATION_NUMBER,
                    content=self.create_booking_ui_sederhana()
                ),
                ft.Tab(
                    text="Transaksi",
                    icon=ft.Icons.HISTORY,
                    content=self.create_transaction_ui()
                ),
            ],
            expand=True
        )
        
        logout_button = ft.ElevatedButton(
            "Logout",
            on_click=self.logout,
            icon=ft.Icons.LOGOUT,
            color=ft.Colors.RED
        )
        
        self.page.clean()
        self.page.add(
            ft.Row(
                [
                    ft.Text(f"Selamat datang, {self.current_user.username}", size=20, weight="bold"),
                    logout_button
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            self.tab_menu
        )

        
    
    def update_film_list(self):
        self.film_list_view.controls.clear()
        
        if not self.list_film.films:
            self.film_list_view.controls.append(ft.Text("Tidak ada film yang tersedia."))
            return
        
        for film in self.list_film.films:
            film_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.MOVIE),
                                title=ft.Text(film.get_judul(), weight="bold"),
                                subtitle=ft.Text(f"{film.get_genre()} | {film.get_durasi()} menit"),
                            ),
                            ft.Row(
                                [
                                    ft.Text(f"Sutradara: {film.get_sutradara()}"),
                                    ft.Text(f"Rating: {film.get_rating()}"),
                                ],
                                spacing=20
                            ),
                            ft.Text(film.get_deskripsi(), size=12),
                            ft.Text(f"Jadwal: {film.get_jadwal_penayangan()}"),
                            ft.Image(src=film.get_poster(), width=200, height=300, fit=ft.ImageFit.CONTAIN),
                        ],
                        spacing=5
                    ),
                    padding=10,
                    width=400
                )
            )
            self.film_list_view.controls.append(film_card)
        
        self.page.update()
    
    
    
    def create_booking_ui_sederhana(self):
        # Dropdown Film
        film_options = [ft.dropdown.Option(film.get_judul()) for film in self.list_film.films]
        self.film_dropdown = ft.Dropdown(
            label="Pilih Film",
            options=film_options,
            width=300
        )

        # Dropdown Studio
        studio_options = [ft.dropdown.Option(nama) for nama in self.studios.keys()]
        self.studio_dropdown = ft.Dropdown(
            label="Pilih Studio",
            options=studio_options,
            width=300,
            on_change=self.update_seat_grid
        )

        # Tipe Tiket
        self.ticket_type = ft.Dropdown(
            label="Tipe Tiket",
            options=[
                ft.dropdown.Option("Biasa"),
                ft.dropdown.Option("Premiere")
            ],
            width=300
        )
        
        # Voucher Field
        self.voucher_field = ft.TextField(
            label="Kode Voucher",
            width=200,
            hint_text="Masukkan DISKON20 untuk diskon 20%"
        )

        # Date Picker
        self.date_picker = ft.DatePicker(
            first_date=datetime.now(),
            on_change=self.update_date_display
        )
        self.page.overlay.append(self.date_picker)
        self.date_button = ft.ElevatedButton(
            "Pilih Tanggal",
            on_click=lambda e: self.open_date_picker()
        )    
        self.selected_date = ft.Text()

        # Seat Grid
        self.seat_grid = ft.GridView(
            runs_count=10,
            max_extent=40,
            spacing=5,
            run_spacing=5,
        )

        
       

        # Booking Button
        self.booking_button = ft.ElevatedButton(
            "Pesan Tiket",
            icon=ft.Icons.CHECK_CIRCLE,
            on_click=self.process_booking
        )

        return ft.Column([
            ft.Row([self.film_dropdown, self.studio_dropdown, self.ticket_type], spacing=20),
            ft.Row([self.date_button, self.selected_date], spacing=20),
            ft.Text("Pilih Kursi:", weight="bold"),
            self.voucher_field,
            self.seat_grid,
            self.booking_button
        ], spacing=20, scroll=ft.ScrollMode.AUTO)
    
    def update_seat_grid(self, e=None):
        self.seat_grid.controls.clear()
        
        if not self.studio_dropdown.value:
            return
            
        studio = self.studios[self.studio_dropdown.value]
        
        for row in range(1, studio.kursi.rows + 1):
            for col in range(1, studio.kursi.cols + 1):
                seat_status = studio.kursi.seats[row-1][col-1]
                
                if seat_status == TheaterKursi.EMPTY:
                    bgcolor = ft.Colors.GREEN_200
                elif seat_status == TheaterKursi.TAKEN:
                    bgcolor = ft.Colors.RED_200
                else:  # SELECTED
                    bgcolor = ft.Colors.BLUE_200
                
                seat = ft.Container(
                    content=ft.Text(f"{row}-{col}"),
                    width=40,
                    height=40,
                    bgcolor=bgcolor,
                    border_radius=5,
                    alignment=ft.alignment.center,
                    on_click=lambda e, r=row, c=col: self.toggle_seat_selection(r, c)
                )
                self.seat_grid.controls.append(seat)
        
        self.page.update()
    
    def toggle_seat_selection(self, row, col):
        studio = self.studios[self.studio_dropdown.value]
        if studio.kursi.toggle_pilih(row, col):
            self.update_seat_grid()
    
    def process_booking(self, e):
    
        # Validasi input form
        if not self.film_dropdown.value:
            self.show_error_message("Harap pilih film")
            return
        
        if not self.studio_dropdown.value:
            self.show_error_message("Harap pilih studio")
            return
        
        if not self.ticket_type.value:
            self.show_error_message("Harap pilih tipe tiket")
            return
        
        if not self.date_picker.value:
            self.show_error_message("Harap pilih tanggal")
            return
        
        # Validasi tanggal tidak boleh masa lalu
        if self.date_picker.value.date() < datetime.now().date():
            self.show_error_message("Tanggal tidak boleh masa lalu")
            return
        
        # Dapatkan kursi yang dipilih
        studio = self.studios[self.studio_dropdown.value]
        selected_seats = studio.kursi.get_selected_seats()
        
        if not selected_seats:
            self.show_error_message("Harap pilih minimal satu kursi")
            return
        
        # Validasi tipe tiket dengan studio
        if self.ticket_type.value == "Premiere" and self.studio_dropdown.value != "Studio Premiere":
            self.show_error_message("Tiket Premiere hanya tersedia di Studio Premiere")
            return
        
        if self.ticket_type.value == "Biasa" and self.studio_dropdown.value == "Studio Premiere":
            self.show_error_message("Studio Premiere hanya menerima tiket Premiere")
            return
        
        # Format nomor kursi
        seat_numbers = [f"{row}-{col}" for row, col in selected_seats]
        
        # Dapatkan film yang dipilih
        selected_film = next((f for f in self.list_film.films if f.get_judul() == self.film_dropdown.value), None)
        
        if not selected_film:
            self.show_error_message("Film tidak ditemukan")
            return
        
        # Buat transaksi
        self.current_transaction = Transaksi(
            username=self.current_user.username,
            film=selected_film,
            tanggal_pemesanan=self.date_picker.value,
            no_kursi=seat_numbers,
            studio=self.studio_dropdown.value,
            tipe_tiket=self.ticket_type.value,
            voucher=self.voucher_field.value if self.voucher_field.value else None
        )
        
            # Tampilkan dialog konfirmasi dengan opsi konsumsi
        self.show_consumption_dialog()
           
    def show_error_message(self, message):
        """Tampilkan pesan error"""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.RED_400
        )
        self.page.snack_bar.open = True
        self.page.update()
    
    def show_consumption_dialog(self):
        """Tampilkan dialog pilihan konsumsi sebelum pembayaran"""
        if not self.current_transaction:
            return
        
        # Reset selected consumables
        self.selected_consumables = []
        
        # Buat kontrol untuk makanan
        food_controls = []
        food_controls.append(ft.Text("Makanan:", weight="bold"))
        
        for key, (name, prices) in self.konsumsi.makanan.items():
            # Dropdown untuk ukuran
            size_dropdown = ft.Dropdown(
                label=f"Ukuran {name}",
                options=[
                    ft.dropdown.Option(size, data={"type": "food", "key": key, "name": name, "size": size, "price": price})
                    for size, price in prices.items()
                ],
                width=200,
                on_change=self.add_consumable
            )
            
            food_row = ft.Row([
                ft.Text(name, width=150),
                size_dropdown,
                ft.Text(f"Diet: Rp {prices['Diet']:,}\nMedium: Rp {prices['Medium']:,}\nJumbo: Rp {prices['Jumbo']:,}", size=10)
            ])
            food_controls.append(food_row)
        
        # Buat kontrol untuk minuman
        drink_controls = []
        drink_controls.append(ft.Text("Minuman:", weight="bold"))
        
        for key, (name, prices) in self.konsumsi.minuman.items():
            # Dropdown untuk ukuran
            size_dropdown = ft.Dropdown(
                label=f"Ukuran {name}",
                options=[
                    ft.dropdown.Option(size, data={"type": "drink", "key": key, "name": name, "size": size, "price": price})
                    for size, price in prices.items()
                ],
                width=200,
                on_change=self.add_consumable
            )
            
            drink_row = ft.Row([
                ft.Text(name, width=150),
                size_dropdown,
                ft.Text(f"Diet: Rp {prices['Diet']:,}\nMedium: Rp {prices['Medium']:,}\nJumbo: Rp {prices['Jumbo']:,}", size=10)
            ])
            drink_controls.append(drink_row)
        
        # List konsumsi yang dipilih
        self.selected_consumables_view = ft.Column([
            ft.Text("Konsumsi yang dipilih:", weight="bold"),
            ft.Text("Belum ada yang dipilih", color=ft.Colors.GREY)
        ])
        
        # Dialog konsumsi
        self.consumption_dialog = ft.AlertDialog(
            title=ft.Text("Pilih Konsumsi (Opsional)"),
            content=ft.Container(
                content=ft.Column([
                    ft.Column(food_controls, spacing=10),
                    ft.Divider(),
                    ft.Column(drink_controls, spacing=10),
                    ft.Divider(),
                    self.selected_consumables_view
                ], spacing=15, scroll=ft.ScrollMode.AUTO),
                width=500,
                height=400
            ),
            actions=[
                ft.TextButton("Lanjut ke Pembayaran", on_click=self.proceed_to_payment),
                ft.TextButton("Batal", on_click=self.cancel_booking)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.dialog = self.consumption_dialog
        self.consumption_dialog.open = True
        self.page.update()
    
    def add_consumable(self, e):
        """Tambah item konsumsi ke pilihan"""
        if not e.control.value or not e.control.data:
            return
        
        item_data = e.control.data
        
        # Cek apakah item sudah dipilih
        existing_item = next((item for item in self.selected_consumables 
                             if item["name"] == item_data["name"] and item["size"] == item_data["size"]), None)
        
        if not existing_item:
            consumable_item = {
                "name": item_data["name"],
                "size": item_data["size"],
                "harga": item_data["price"],
                "type": item_data["type"]
            }
            self.selected_consumables.append(consumable_item)
            self.update_selected_consumables_view()
    
    def remove_consumable(self, item_to_remove):
        """Hapus item konsumsi dari pilihan"""
        self.selected_consumables = [item for item in self.selected_consumables 
                                   if not (item["name"] == item_to_remove["name"] and item["size"] == item_to_remove["size"])]
        self.update_selected_consumables_view()
    
    def update_selected_consumables_view(self):
        """Update tampilan konsumsi yang dipilih"""
        self.selected_consumables_view.controls.clear()
        self.selected_consumables_view.controls.append(ft.Text("Konsumsi yang dipilih:", weight="bold"))
        
        if not self.selected_consumables:
            self.selected_consumables_view.controls.append(ft.Text("Belum ada yang dipilih", color=ft.Colors.GREY))
        else:
            total_consumable = 0
            for item in self.selected_consumables:
                total_consumable += item["harga"]
                item_row = ft.Row([
                    ft.Text(f"{item['name']} ({item['size']})"),
                    ft.Text(f"Rp {item['harga']:,}"),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color=ft.Colors.RED,
                        tooltip="Hapus",
                        on_click=lambda e, item=item: self.remove_consumable(item)
                    )
                ])
                self.selected_consumables_view.controls.append(item_row)
            
            self.selected_consumables_view.controls.append(ft.Divider())
            self.selected_consumables_view.controls.append(
                ft.Text(f"Total Konsumsi: Rp {total_consumable:,}", weight="bold")
            )
        
        self.page.update()
    
    def proceed_to_payment(self, e):
        """Lanjut ke proses pembayaran"""
        # Update konsumsi di transaksi
        if self.current_transaction:
            self.current_transaction.konsumsi = self.selected_consumables
        
        # Tutup dialog konsumsi
        self.consumption_dialog.open = False
        
        # Tampilkan dialog pembayaran
        self.show_payment_dialog()
    
    def cancel_booking(self, e):
        """Batalkan proses booking"""
        # Reset kursi yang dipilih
        if self.studio_dropdown.value:
            studio = self.studios[self.studio_dropdown.value]
            for row in range(studio.kursi.rows):
                for col in range(studio.kursi.cols):
                    if studio.kursi.seats[row][col] == TheaterKursi.SELECTED:
                        studio.kursi.seats[row][col] = TheaterKursi.EMPTY
            self.update_seat_grid()
        
        # Tutup dialog
        if hasattr(self, 'consumption_dialog'):
            self.consumption_dialog.open = False
        if hasattr(self, 'payment_dialog'):
            self.payment_dialog.open = False
        
        # Reset transaksi
        self.current_transaction = None
        self.selected_consumables = []
        
        self.page.update()
    
#====================================================================================================================================================
        # Dapatkan kursi yang dipilih
        studio = self.studios[self.studio_dropdown.value]
        selected_seats = studio.kursi.get_selected_seats()
        
        if not selected_seats:
            self.page.snack_bar = ft.SnackBar(ft.Text("Harap pilih minimal satu kursi"))
            self.page.snack_bar.open = True
            self.page.update()
            return
        
        # Format nomor kursi
        seat_numbers = [f"{row}-{col}" for row, col in selected_seats]
        
        # Dapatkan film yang dipilih
        selected_film = next(f for f in self.list_film.films if f.get_judul() == self.film_dropdown.value)
        
        # Buat transaksi
        self.current_transaction = Transaksi(
            username=self.current_user.username,
            film=selected_film,
            tanggal_pemesanan=self.date_picker.value,
            no_kursi=seat_numbers,
            studio=self.studio_dropdown.value,
            tipe_tiket=self.ticket_type.value,
            voucher=self.voucher_field.value
        )
        
        # Tampilkan dialog konfirmasi
        self.show_payment_dialog()
    
    def show_payment_dialog(self):
        if not self.current_transaction:
            return
        
        # Hitung total
        total = self.current_transaction.hitung_total()
        
        # Format detail transaksi
        transaction_details = [
            f"Film: {self.current_transaction.film.get_judul()}",
            f"Studio: {self.current_transaction.studio}",
            f"Tipe Tiket: {self.current_transaction.tipe_tiket}",
            f"Tanggal: {self.current_transaction.tanggal_pemesanan.strftime('%d/%m/%Y')}",
            f"Kursi: {', '.join(self.current_transaction.no_kursi)}",
            f"Voucher: {self.current_transaction.voucher if self.current_transaction.voucher else 'Tidak ada'}",
            f"Diskon: {self.current_transaction.diskon*100}%",
            f"Total: Rp {total:,}"
        ]
        
        # Buat dialog
        self.payment_dialog = ft.AlertDialog(
            title=ft.Text("Konfirmasi Pembayaran"),
            content=ft.Column(
                [ft.Text(line) for line in transaction_details],
                spacing=10
            ),
            actions=[
                ft.TextButton("Bayar", on_click=self.confirm_payment),
                ft.TextButton("Batal", on_click=self.cancel_payment)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.dialog = self.payment_dialog
        self.payment_dialog.open = True
        self.page.update()
    
    def confirm_payment(self, e):
        if not self.current_transaction:
            return
        
        # Konfirmasi pembayaran
        self.current_transaction.confirm_payment()
        
        # Tambahkan ke history transaksi
        if not hasattr(self.current_user, 'transaksi_history'):
            self.current_user.transaksi_history = []
        self.current_user.transaksi_history.append(self.current_transaction)
        
        # Konfirmasi pemilihan kursi
        studio = self.studios[self.current_transaction.studio]
        studio.kursi.confirm_selection()
        
        # Tutup dialog
        self.page.dialog.open = False
        
        # Tampilkan pesan sukses
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Pembayaran berhasil! Tiket telah dipesan."),
            open=True
        )
        
        # Update history transaksi
        self.update_transaction_history()
        
        # Reset form
        self.reset_booking_form()
        
        self.page.update()
    
    def cancel_payment(self, e):
        self.page.dialog.open = False
        self.page.update()
    
    def reset_booking_form(self):
        self.film_dropdown.value = None
        self.studio_dropdown.value = None
        self.ticket_type.value = None
        self.date_picker.value = None
        self.selected_date.value = ""
        self.voucher_field.value = ""
        self.selected_consumables = []
        
        # Reset seat selection
        for studio in self.studios.values():
            for row in range(studio.kursi.rows):
                for col in range(studio.kursi.cols):
                    if studio.kursi.seats[row][col] == TheaterKursi.SELECTED:
                        studio.kursi.seats[row][col] = TheaterKursi.EMPTY
        
        self.update_seat_grid()
        self.page.update()
    
    def create_transaction_ui(self):
        self.transaction_list_view = ft.ListView(expand=True)
        self.update_transaction_history()
        
        return ft.Column([
            ft.Text("Riwayat Transaksi", size=20, weight="bold"),
            self.transaction_list_view
        ], expand=True)
    
    def update_transaction_history(self):
        self.transaction_list_view.controls.clear()
        
        if not hasattr(self.current_user, 'transaksi_history') or not self.current_user.transaksi_history:
            self.transaction_list_view.controls.append(ft.Text("Belum ada transaksi"))
            return
        
        for transaksi in reversed(self.current_user.transaksi_history):
            transaction_card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            title=ft.Text(f"ID: {transaksi.id_transaksi}"),
                            subtitle=ft.Text(f"Status: {transaksi.status}"),
                        ),
                        ft.Text(f"Film: {transaksi.film.get_judul()}"),
                        ft.Text(f"Studio: {transaksi.studio}"),
                        ft.Text(f"Kursi: {', '.join(transaksi.no_kursi)}"),
                        ft.Text(f"Tanggal: {transaksi.tanggal_pemesanan.strftime('%d/%m/%Y')}"),
                        ft.Text(f"Total: Rp {transaksi.hitung_total():,}"),
                    ], spacing=5),
                    padding=10,
                    width=400
                )
            )
            self.transaction_list_view.controls.append(transaction_card)
        
        self.page.update()

def main(page: ft.Page):
    # Set app theme and properties
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE,
        visual_density=ft.VisualDensity.COMFORTABLE
    )
    
    # Create and run the app
    app = CinemaApp(page)

if __name__ == "__main__":
    ft.app(target=main)