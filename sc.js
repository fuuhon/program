 let kursiTerpilih = [];
 
// Tambahkan di awal sc.js

function bukaHalamanFilm(kodeFilm) {
    fetch(`/api/film/${kodeFilm}`)
        .then(response => response.json())
        .then(film => {
            document.getElementById('film-title').textContent = film.judul;
            document.getElementById('film-description').textContent = film.deskripsi;
            // Isi data film lainnya...
            bukaHalaman('film');
        });
}

// Fungsi untuk fetch data dari backend
async function fetchData(endpoint) {
    const response = await fetch(endpoint);
    return await response.json();
}
const app = new Vue({
  el: '#halaman-user',
  data: {
    films: []
  }
});

// Load film dari backend
async function loadFilms() {
    try {
        const films = await fetchData('/api/films');
        const container = document.querySelector('#halaman-user .film-container');
        
        films.forEach(film => {
            const filmElement = document.createElement('img');
            filmElement.src = 'static/img/abs1.png'; // Ganti dengan gambar sesuai film
            filmElement.className = 'img3';
            filmElement.onclick = () => bukaHalamanFilm(film.kode);
            container.appendChild(filmElement);
        });
    } catch (error) {
        console.error('Gagal memuat film:', error);
    }
}

// Fungsi untuk memuat detail film
async function bukaHalamanFilm(kodeFilm) {
    try {
        const film = await fetchData(`/api/film/${kodeFilm}`);
        document.getElementById('film-title').textContent = film.judul;
        document.getElementById('film-description').textContent = film.deskripsi;
        // Isi detail film lainnya...
        
        bukaHalaman('film');
    } catch (error) {
        console.error('Gagal memuat detail film:', error);
    }
}

// Fungsi untuk memesan kursi
async function pesanKursi(namaKursi) {
    const studioType = document.getElementById('studio').value;
    const [baris, kolom] = parseKursi(namaKursi); // Fungsi untuk mengubah A1 -> 1,1
    
    try {
        const response = await fetch('/api/kursi/pesan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                studio: studioType,
                baris: baris,
                kolom: kolom
            })
        });
        
        const result = await response.json();
        if (result.status === 'success') {
            // Update UI untuk kursi terpesan
            const kursiElement = document.getElementById(namaKursi);
            kursiElement.classList.add('dipilih');
            kursiDipilih.push(namaKursi);
            document.getElementById('output').value = kursiDipilih.join(', ');
        } else {
            alert(result.message);
        }
    } catch (error) {
        console.error('Gagal memesan kursi:', error);
    }
}

// Panggil loadFilms saat halaman dimuat
document.addEventListener('DOMContentLoaded', () => {
    if (window.location.pathname === '/') {
        loadFilms();
    }
});

//=============================================================================================================================================
   function bukaHalaman(halaman) {
  console.log("Membuka halaman:", halaman);

  document.querySelectorAll('.halaman').forEach(el => {
    el.style.display = 'none';
  });
  document.getElementById('halaman-utama').style.display = 'none';

  const target = document.getElementById('halaman-' + halaman);
  if (target) {
    target.style.display = 'block';
  } else {
    console.warn("Halaman tidak ditemukan:", halaman);
  }
}
function kembali() {
  
  document.querySelectorAll('.halaman').forEach(el => {
    el.style.display = 'none';
  });
  document.getElementById('halaman-utama').style.display = 'block';
}

  

  
    let kursiDipilih = [];
    

  function pilihKursi(namaKursi) {
    const kursi = document.getElementById(namaKursi);

    if (!kursiDipilih.includes(namaKursi)) {
      kursiDipilih.push(namaKursi);
      kursi.classList.add('dipilih'); // Tambahkan class 'dipilih' agar warna berubah
    }

    document.getElementById('output').value = kursiDipilih.join(', ');
  }
const makananDipilih = [];
let total = 0;

const hargaMakanan = {
  'POP CORN CARAMEL - RP 35000': 35000,
  'POP CORN BUTTER - RP 25000': 25000,
  'POP CORN CHEESE - RP 15000': 15000,
  'POP COEN SPICY - RP 20000': 20000,
  'HOT DRAGON - RP 10000': 10000,
  'FRIED SPICY POTATO - RP 18000': 18000,
  'FRIED POTATO - RP 12000': 12000,
  'LEMON SODA - RP 15000': 15000,
  'ICED TEA - RP 8000': 8000,
  'BLOOD DEMON - RP 10000': 10000,
  'HEAVENLY ICE CREAM - RP 5000': 5000
};


function fnb(idMakanan, labelMakanan) {
  const makanan = document.getElementById(idMakanan);

  
  makananDipilih.push(labelMakanan);
  makanan.classList.add('dipilih1'); 

  total += hargaMakanan[labelMakanan] || 0;

 
  document.getElementById('outputmkn').value = makananDipilih.join('\n');
  document.getElementById('totalHarga').value = 'RP ' + total.toLocaleString('id-ID');
  


 
}

 function tampilkan() {
    const nama = document.getElementById("username").value;
    const film = document.getElementById("film").value;
    const tanggal = document.getElementById("tanggal").value;
    const jam = document.getElementById("sesi").value;
    const studio = document.getElementById("studio").value;
    const kursi = kursiDipilih.join(", ");


     // Tambahkan list makanan yang dipilih
  const makananPesanan = makananDipilih.length > 0 ? makananDipilih.join("\n") : "Tidak ada makanan dipesan";
  
  // Total harga makanan juga ditampilkan
  const totalMakanan = total > 0 ? `RP ${total.toLocaleString('id-ID')}` : "0";

    let hasil = `
    ============================
         TIKET BIOSKOP
    ============================
    Nama    : ${nama}
    Film    : ${film}
    Tanggal : ${tanggal}
    Jam     : ${jam}
    Studio  : ${studio}
    Kursi   : ${kursi}
    ============================

  
    ============================
         MAKANAN DI PESAN
    ============================
      ${makananPesanan}
    ============================

    Total Harga Makanan: ${totalMakanan}

    ====================================
    `;

    // Tempelkan hasil ke halaman cetak tiket
   const halamanCetak = document.getElementById("halaman-cetaktiket");
     halamanCetak.innerHTML = `<pre>${hasil}</pre>
    <button onclick="kembali()" class="btn3">Kembali</button>
    <button onclick="bukaHalaman('makanan')" class="btn3">Pesan Makanan</button>
    <button onclick="" class="btn3">Pembayaran</button>
`;
    
  }