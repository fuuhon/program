from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'static/img'

from jinja2 import Environment

def format_currency(value):
    return "{:,.0f}".format(value)

app.jinja_env.filters['format_currency'] = format_currency

# Film Class
class Film:
    def __init__(self, kode, judul, deskripsi, tahun_rilis, durasi, sutradara, genre, harga, rating, hari_tayang, jam_tayang, gambar):
        self.__kode = kode
        self.__judul = judul
        self.__deskripsi = deskripsi
        self.__tahun_rilis = tahun_rilis
        self.__durasi = durasi
        self.__sutradara = sutradara
        self.__genre = genre
        self.__harga = harga
        self.__rating = rating
        self.__hari_tayang = hari_tayang
        self.__jam_tayang = jam_tayang
        self.__gambar = gambar

    # Getter methods
    def get_kode(self):
        return self.__kode
    
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

    def get_harga(self):
        return self.__harga
    
    def get_gambar(self):
        return self.__gambar
    
    def get_hari_tayang(self):
        return self.__hari_tayang
    
    def get_jam_tayang(self):
        return self.__jam_tayang
    
    def get_poster_url(self):
        return f"/static/img/{self.__gambar}"


# List Film Manager
class ListFilm:
    def __init__(self):
        self.films = []
    
    def muat_film_dari_file(self, nama_file):
        try:
            with open(nama_file, 'r', encoding='utf-8') as file:
                for line in file:
                    data = line.strip().split('|')
                    if len(data) >= 12:
                        film = Film(
                            kode=data[0],
                            judul=data[1],
                            deskripsi=data[2],
                            tahun_rilis=data[3],
                            durasi=int(data[4]),
                            sutradara=data[5],
                            genre=data[6],
                            harga=int(data[7]),
                            rating=int(data[8]),
                            hari_tayang=data[9],
                            jam_tayang=data[10],
                            gambar=data[11]
                        )
                        self.films.append(film)
        except FileNotFoundError:
            print("File database tidak ditemukan")
        except Exception as e:
            print(f"Error membaca database: {str(e)}")


# Theater Seat Management
EMPTY = 0
TAKEN = 1


class TheaterKursi:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.seats = [[EMPTY for _ in range(cols)] for _ in range(rows)]

    def tampilkan_kursi(self):
        return self.seats

    def pesan_kursi(self, baris, kolom):
        r, c = baris - 1, kolom - 1
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return False, "Posisi tidak valid."
        if self.seats[r][c] == TAKEN:
            return False, "Kursi sudah diambil."
        self.seats[r][c] = TAKEN
        return True, f"Kursi baris {baris}, kolom {kolom} berhasil dipesan."

    def batal_pesan(self, baris, kolom):
        r, c = baris - 1, kolom - 1
        if self.seats[r][c] == EMPTY:
            return False, "Kursi belum dipesan."
        else:
            self.seats[r][c] = EMPTY
            return True, f"Pemesanan kursi baris {baris}, kolom {kolom} dibatalkan."


# Studio Classes
class Studio:
    def __init__(self, jumlah_kursi, fasilitas):
        self.jumlah_kursi = jumlah_kursi
        self.fasilitas = fasilitas
        self.kursi = TheaterKursi(10, 10)  # Example: 10x10 seats
        self.film_schedule = {}


class Premiere(Studio):
    def __init__(self, jumlah_kursi):
        super().__init__(jumlah_kursi, {"kursi premium", "selimut", "snack eksklusif", "recliner"})


# Konsumsi (Food and Beverage)
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

    def get_menu_makanan(self):
        return self.makanan

    def get_menu_minuman(self):
        return self.minuman


konsumen_db = [
    {"username": "user", "password": "user123", "role": "user"},
    {"username": "admin", "password": "admin123", "role": "admin"}
]


class Konsumen:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def login(username, password):
        for user in konsumen_db:
            if user['username'] == username and user['password'] == password:
                return Konsumen(username)
        return None



class TransaksiTiket:
    def __init__(self, id_transaksi, username, film, tanggal_pemesanan, no_kursi, studio, tipe_tiket, voucher=None, diskon=0):
        self.id_transaksi = id_transaksi
        self.username = username
        self.film = film
        self.tanggal_pemesanan = tanggal_pemesanan
        self.no_kursi = no_kursi
        self.studio = studio
        self.tipe_tiket = tipe_tiket
        self.voucher = voucher
        self.diskon = diskon
        self.harga_tiket = self._get_harga_tiket()  # Initialize harga_tiket
        
        # Konversi tanggal ke hari
        try:
            tanggal_obj = datetime.strptime(tanggal_pemesanan, '%Y-%m-%d')
            self.hari = tanggal_obj.strftime('%A').lower()
        except:
            self.hari = ''

    def _get_harga_tiket(self):
        # Implement logic to get ticket price based on film and studio type
        # This is a placeholder - you'll need to implement the actual logic
        return 50000  # Default price

    def hitung_total(self):
        total = self.harga_tiket
        
        # Weekend charge
        if self.hari in ['saturday', 'sunday', 'sabtu', 'minggu']:
            total += 20000
        
        # Voucher discount
        if self.diskon > 0:
            total *= (1 - self.diskon)
        
        return round(total)

    def metode_pembayaran(self):
        # Sistem pembayaran lebih fleksibel
        metode = {
            'premiere': ['Credit Card', 'Bank Transfer', 'E-Wallet'],
            'regular': ['Cash', 'QRIS', 'E-Wallet']
        }
        return metode.get(self.tipe_tiket, ['Cash'])

from datetime import datetime
import time

@app.route('/api/transaksi/buat', methods=['POST'])
def buat_transaksi():
    if 'username' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    data = request.json
    
    # Validasi data
    required_fields = ['film', 'tanggal', 'no_kursi', 'studio', 'tipe_tiket']
    if not all(field in data for field in required_fields):
        return jsonify({'status': 'error', 'message': 'Data tidak lengkap'}), 400

    try:
        # Buat objek transaksi
        transaksi = TransaksiTiket(
            id_transaksi=f"TXN-{int(time.time())}",
            username=session['username'],
            film=data['film'],
            tanggal_pemesanan=data['tanggal'],
            no_kursi=data['no_kursi'],
            studio=data['studio'],
            tipe_tiket=data['tipe_tiket'],
            voucher=data.get('voucher'),
            diskon=data.get('diskon', 0)
        )

        # Simpan ke database (dalam contoh ini menggunakan session)
        transaksi_data = {
            'id': transaksi.id_transaksi,
            'username': transaksi.username,
            'film': transaksi.film,
            'tanggal': transaksi.tanggal_pemesanan,
            'kursi': transaksi.no_kursi,
            'studio': transaksi.studio,
            'tipe': transaksi.tipe_tiket,
            'total': transaksi.hitung_total(),
            'metode_pembayaran': transaksi.metode_pembayaran(),
            'status': 'pending',
            'waktu': datetime.now().isoformat()
        }

        if 'transaksi' not in session:
            session['transaksi'] = []
        session['transaksi'].append(transaksi_data)

        # Response dengan detail lengkap
        return jsonify({
            'status': 'success',
            'data': transaksi_data,
            'actions': [
                {'method': 'GET', 'url': '/api/transaksi/' + transaksi.id_transaksi, 'description': 'Lihat detail transaksi'},
                {'method': 'POST', 'url': '/api/transaksi/' + transaksi.id_transaksi + '/bayar', 'description': 'Proses pembayaran'}
            ]
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/transaksi/<id_transaksi>', methods=['GET'])
def detail_transaksi(id_transaksi):
    if 'transaksi' not in session:
        return jsonify({'status': 'error', 'message': 'Tidak ada transaksi'}), 404
    
    transaksi = next((t for t in session['transaksi'] if t['id'] == id_transaksi), None)
    
    if not transaksi:
        return jsonify({'status': 'error', 'message': 'Transaksi tidak ditemukan'}), 404
    
    return jsonify({'status': 'success', 'data': transaksi})


@app.route('/api/transaksi/<id_transaksi>/bayar', methods=['POST'])
def proses_pembayaran(id_transaksi):
    if 'transaksi' not in session:
        return jsonify({'status': 'error', 'message': 'Tidak ada transaksi'}), 404
    
    transaksi = next((t for t in session['transaksi'] if t['id'] == id_transaksi), None)
    
    if not transaksi:
        return jsonify({'status': 'error', 'message': 'Transaksi tidak ditemukan'}), 404
    
    # Update status transaksi
    transaksi['status'] = 'paid'
    transaksi['waktu_bayar'] = datetime.now().isoformat()
    
    return jsonify({
        'status': 'success',
        'message': 'Pembayaran berhasil',
        'data': transaksi
    })

list_film = ListFilm()
list_film.muat_film_dari_file('films.txt')
konsumsi = Konsumsi()
studio_regular = Studio(100, {"kursi standar"})
studio_premiere = Premiere(50)



@app.route('/api/films')
def get_all_films():
    films = []
    for film in list_film.films:
        films.append({
            'kode': film.get_kode(),
            'judul': film.get_judul(),
            'deskripsi': film.get_deskripsi(),
            'poster_url': film.get_poster_url(),
            'harga': film.get_harga(),
            'rating': film.get_rating(),
            'jam_tayang': film.get_jam_tayang()
        })
    return jsonify(films)

@app.route('/api/film/<kode>')
def get_film(kode):
    film = next((f for f in list_film.films if f.kode == kode), None)
    if film:
        return jsonify({
            'kode': film.kode,
            'judul': film.judul,
            'deskripsi': film.deskripsi,
            'poster_url': film.get_poster_url(),
            'durasi': film.durasi,
            'sutradara': film.sutradara,
            'genre': film.genre,
            'harga': film.harga,
            'rating': film.rating,
            'hari_tayang': film.hari_tayang,
            'jam_tayang': film.jam_tayang
        })
    return jsonify({'error': 'Film tidak ditemukan'}), 404




@app.route('/api/kursi/status')
def get_kursi_status():
    studio_type = request.args.get('studio', 'regular')
    studio = studio_premiere if studio_type == 'premiere' else studio_regular
    return jsonify({'kursi': studio.kursi.tampilkan_kursi()})

@app.route('/api/kursi/pesan', methods=['POST'])
def pesan_kursi():
    data = request.json
    studio_type = data.get('studio', 'regular')
    studio = studio_premiere if studio_type == 'premiere' else studio_regular
    
    success, message = studio.kursi.pesan_kursi(data['baris'], data['kolom'])
    if success:
        return jsonify({'status': 'success', 'message': message})
    return jsonify({'status': 'error', 'message': message}), 400

@app.route('/api/makanan')
def get_makanan():
    return jsonify(konsumsi.get_menu_makanan())

@app.route('/api/minuman')
def get_minuman():
    return jsonify(konsumsi.get_menu_minuman())

# Rute untuk halaman
@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        films_data = [{
            'kode': film.get_kode(),
            'judul': film.get_judul(),
            'deskripsi': film.get_deskripsi(),
            'harga': film.get_harga(),
            'rating': film.get_rating()
        } for film in list_film.films]
        
        return render_template(
            'bioskop.html',
            username=session['username'],
            role=session['role'],
            films=films_data
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        return render_template('bioskop.html', films=[])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((u for u in konsumen_db if u['username'] == username and u['password'] == password), None)
        if user:
            session['username'] = user['username']
            session['role'] = user['role']
            flash('Login berhasil!', 'success')
            return redirect(url_for('home'))  # Redirect ke home setelah login
    
    # Untuk GET request atau login gagal
    return render_template(
        'login.html',  # Buat file login.html terpisah
        error=request.args.get('error')
    )
@app.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)