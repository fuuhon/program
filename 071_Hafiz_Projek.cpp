#include <iostream>
using namespace std;

const int MAX_NODE = 100;
int jumlahRestoran = 0;

struct pesanan
{
    string idPesanan;
    string pengirim;
    string konsumen;
    string restoran;
    string alamatTujuan;
    string status;
    pesanan *next;
    pesanan *prev;
    pesanan *nextKurir;
    pesanan *prevKurir;
};

pesanan *headPesanan = nullptr;
pesanan *tailPesanan = nullptr;

struct kurir
{
    string idKurir;
    string nama;
    string password;
    string status;
    pesanan *daftarPesanan;
    kurir *next;
    kurir *prev;
};

struct konsumen
{
    string idKonsumen;
    string nama;
    string password;
};

struct restoran
{
    string namaRestoran;
    string menu[100];
    float harga[100];
    string jenisMenu[100];
};

struct treeMenu
{
    string nama;
    treeMenu *left;
    treeMenu *right;
};

treeMenu *rootMenuTree = nullptr;

treeMenu *buatNode(const string &nama)
{
    treeMenu *node = new treeMenu;
    node->nama = nama;
    node->left = nullptr;
    node->right = nullptr;
    return node;
}

void insertMenuTree(treeMenu *&root, const string &kategori, const string &namaMenu)
{
    if (!root)
    {
        root = buatNode(kategori);
        root->left = buatNode(namaMenu);
        return;
    }
    if (root->nama == kategori)
    {
        if (!root->left)
            root->left = buatNode(namaMenu);
        else if (!root->right)
            root->right = buatNode(namaMenu);
        return;
    }
    insertMenuTree(root->left, kategori, namaMenu);
    insertMenuTree(root->right, kategori, namaMenu);
}

struct MenuKategoriNodeTree
{
    string namaMenu;
    float harga;
    string restoran;
    MenuKategoriNodeTree *left;
    MenuKategoriNodeTree *right;
};

struct KategoriMenuTree
{
    string kategori;
    MenuKategoriNodeTree *menuRoot;
    KategoriMenuTree *left;
    KategoriMenuTree *right;
};

void insertKategori(KategoriMenuTree *&root, const string &kategori)
{
    if (!root)
    {
        root = new KategoriMenuTree{kategori, nullptr, nullptr, nullptr};
        return;
    }
    if (kategori < root->kategori)
        insertKategori(root->left, kategori);
    else if (kategori > root->kategori)
        insertKategori(root->right, kategori);
}

void insertMenu(MenuKategoriNodeTree *&root, const string &namaMenu, float harga, const string &restoran)
{
    if (!root)
    {
        root = new MenuKategoriNodeTree{namaMenu, harga, restoran, nullptr, nullptr};
        return;
    }
    if (namaMenu < root->namaMenu)
        insertMenu(root->left, namaMenu, harga, restoran);
    else if (namaMenu > root->namaMenu)
        insertMenu(root->right, namaMenu, harga, restoran);
}

KategoriMenuTree *rootKategoriMenu = nullptr;

KategoriMenuTree *findKategori(KategoriMenuTree *root, const string &kategori)
{
    if (!root)
        return nullptr;
    if (root->kategori == kategori)
        return root;
    if (kategori < root->kategori)
        return findKategori(root->left, kategori);
    return findKategori(root->right, kategori);
}

void tampilkanMenu(MenuKategoriNodeTree *root)
{
    if (!root)
        return;
    tampilkanMenu(root->left);
    cout << root->namaMenu << " (Restoran: " << root->restoran << ", Harga: Rp " << root->harga << ")\n";
    tampilkanMenu(root->right);
}

void tampilkanMenuWithNumber(MenuKategoriNodeTree *root, int &idx)
{
    if (!root)
        return;
    tampilkanMenuWithNumber(root->left, idx);
    cout << idx++ << ". " << root->namaMenu << " (Restoran: " << root->restoran << ", Harga: Rp " << root->harga << ")\n";
    tampilkanMenuWithNumber(root->right, idx);
}

void rekomendasiFleksibel(const string &kategori)
{
    cout << "\n";
    KategoriMenuTree *kat = findKategori(rootKategoriMenu, kategori);
    if (!kat || !kat->menuRoot)
    {
        cout << "Tidak ada menu untuk kategori " << kategori << ".\n";
        return;
    }
    cout << "Rekomendasi untuk kategori " << kategori << ":\n";
    int idx = 1;
    tampilkanMenuWithNumber(kat->menuRoot, idx);
}

struct hashtableKonsumen
{
    konsumen *table[100];
    bool occupied[100];
    hashtableKonsumen()
    {
        for (int i = 0; i < 100; ++i)
        {
            table[i] = nullptr;
            occupied[i] = false;
        }
    }
    int hashFunction(const string &idKonsumen)
    {
        int hash = 0;
        for (char c : idKonsumen)
            hash = (hash + c) % 100;
        return hash;
    }

    void insertKonsumen(konsumen *konsumen)
    {
        int index = hashFunction(konsumen->idKonsumen);
        while (occupied[index])
        {
            index = (index + 1) % 100;
        }
        table[index] = konsumen;
        occupied[index] = true;
    }

    konsumen *searchKonsumen(const string &idKonsumen)
    {
        int index = hashFunction(idKonsumen);
        int startIndex = index;
        while (occupied[index])
        {
            if (table[index]->idKonsumen == idKonsumen)
                return table[index];
            index = (index + 1) % 100;
            if (index == startIndex)
                break;
        }
        return nullptr;
    }
};

struct hashtableKurir
{
    kurir *table[100];
    bool occupied[100] = {false};
    int hashFunction(const string &idKurir)
    {
        int hash = 0;
        for (char c : idKurir)
            hash = (hash + c) % 100;
        return hash;
    }

    void insertKurir(kurir *kurir)
    {
        int index = hashFunction(kurir->idKurir);
        while (occupied[index])
        {
            index = (index + 1) % 100;
        }
        table[index] = kurir;
        occupied[index] = true;
    }

    kurir *searchKurir(const string &idKurir)
    {
        int index = hashFunction(idKurir);
        int startIndex = index;
        while (occupied[index])
        {
            if (table[index]->idKurir == idKurir)
                return table[index];
            index = (index + 1) % 100;
            if (index == startIndex)
                break;
        }
        return nullptr;
    }
};

struct NodeQueuePesanan
{
    pesanan *data;
    NodeQueuePesanan *next;
};

struct QueuePesanan
{
    NodeQueuePesanan *front;
    NodeQueuePesanan *rear;

    QueuePesanan()
    {
        front = rear = nullptr;
    }

    void enqueue(pesanan *p)
    {
        NodeQueuePesanan *baru = new NodeQueuePesanan;
        baru->data = p;
        baru->next = nullptr;
        if (rear == nullptr)
        {
            front = rear = baru;
        }
        else
        {
            rear->next = baru;
            rear = baru;
        }
    }

    pesanan *dequeue()
    {
        if (front == nullptr)
            return nullptr;
        NodeQueuePesanan *temp = front;
        pesanan *hasil = temp->data;
        front = front->next;
        if (front == nullptr)
            rear = nullptr;
        delete temp;
        return hasil;
    }

    bool isEmpty()
    {
        return front == nullptr;
    }

    void tampilkanQueue()
    {
        NodeQueuePesanan *temp = front;
        int idx = 1;
        while (temp != nullptr)
        {
            cout << idx++ << ". ID: " << temp->data->idPesanan
                 << ", Konsumen: " << temp->data->konsumen
                 << ", Alamat: " << temp->data->alamatTujuan << endl;
            temp = temp->next;
        }
        if (idx == 1)
            cout << "Antrian kosong.\n";
    }
};

QueuePesanan queueKonfirmasi;

string namaNode[MAX_NODE];
int adjMatrix[MAX_NODE][MAX_NODE];
int jumlahNode = 0;

void initGraph()
{
    for (int i = 0; i < MAX_NODE; i++)
    {
        for (int j = 0; j < MAX_NODE; j++)
        {
            adjMatrix[i][j] = 0;
        }
    }
}

void tambahNode(const string &nama)
{
    if (jumlahNode >= MAX_NODE)
    {
        cout << "Jumlah node sudah mencapai batas maksimum.\n";
        return;
    }

    bool alamatSudahAda = false;
    for (int i = 0; i < jumlahNode; i++)
    {
        if (namaNode[i] == nama)
        {
            alamatSudahAda = true;
            break;
        }
    }
    if (!alamatSudahAda && jumlahNode < MAX_NODE)
    {
        namaNode[jumlahNode++] = nama;
    }
}

void tambahEdge(const string &dari, const string &ke, int bobot)
{
    int idxDari = -1, idxKe = -1;
    for (int i = 0; i < jumlahNode; i++)
    {
        if (namaNode[i] == dari)
            idxDari = i;
        if (namaNode[i] == ke)
            idxKe = i;
    }
    if (idxDari != -1 && idxKe != -1)
    {
        adjMatrix[idxDari][idxKe] = bobot;
        adjMatrix[idxKe][idxDari] = bobot;
    }
}

void tampilkanGraph()
{
    cout<<"\n";
    cout << "=== Graph Restoran & Alamat ===\n";
    for (int i = 0; i < jumlahNode; i++)
    {
        cout << namaNode[i] << " terhubung ke:\n";
        bool adaEdge = false;
        for (int j = 0; j < jumlahNode; j++)
        {
            if (adjMatrix[i][j] > 0)
            {
                cout << "  - " << namaNode[j] << " (jarak: " << adjMatrix[i][j] << " meter)\n";
                adaEdge = true;
            }
        }
        if (!adaEdge)
            cout << "  (tidak ada koneksi)\n";
    }
}

restoran restoranList[MAX_NODE];

void addRestoran()
{
    restoran restoran;
    cout << "\n";
    cout << "=== Tambah Restoran ===\n";
    cout << "Masukkan nama restoran: ";
    cin.ignore();
    getline(cin, restoran.namaRestoran);
    if (restoran.namaRestoran.empty())
    {
        cout << "Nama restoran tidak boleh kosong.\n";
        return;
    };

    int stop = 0;
    int i = 0;
    while (stop == 0)
    {
        if (i >= 100)
        {
            cout << "Jumlah menu sudah mencapai batas maksimum.\n";
            stop = 1;
            break;
        }
        cout << "Masukkan nama menu " << i + 1 << ": ";
        getline(cin, restoran.menu[i]);
        cout << "Masukkan harga menu " << i + 1 << ": ";
        cin >> restoran.harga[i];
        if (restoran.harga[i] < 0)
        {
            cout << "Harga tidak boleh negatif.\n";
            cin.ignore();
            continue;
        }

        int jenisPilihan;
        cout << "Pilih jenis menu " << i + 1 << ":\n";
        cout << "1. Makanan Berat\n";
        cout << "2. Makanan Ringan\n";
        cout << "3. Minuman\n";
        cout << "Pilihan: ";
        cin >> jenisPilihan;
        cin.ignore();
        if (jenisPilihan == 1)
            restoran.jenisMenu[i] = "Makanan Berat";
        else if (jenisPilihan == 2)
            restoran.jenisMenu[i] = "Makanan Ringan";
        else if (jenisPilihan == 3)
            restoran.jenisMenu[i] = "Minuman";
        else
        {
            cout << "Pilihan tidak valid. Ulangi input jenis menu.\n";
            continue;
        }

        insertMenuTree(rootMenuTree, restoran.jenisMenu[i], restoran.menu[i]);
        insertKategori(rootKategoriMenu, restoran.jenisMenu[i]);
        KategoriMenuTree *kat = findKategori(rootKategoriMenu, restoran.jenisMenu[i]);
        if (kat)
        {
            insertMenu(kat->menuRoot, restoran.menu[i], restoran.harga[i], restoran.namaRestoran);
        }

        int validInput = 0;
        while (!validInput)
        {
            cout << "Apakah Anda ingin menambah menu lagi? (Y/n): ";
            string stopInput;
            cin >> stopInput;
            cin.ignore();
            if (stopInput == "y" || stopInput == "Y")
            {
                validInput = 1;
                i++;
            }
            else if (stopInput == "n" || stopInput == "N")
            {
                stop = 1;
                validInput = 1;
            }
            else
            {
                cout << "Pilihan tidak valid. Silakan coba lagi.\n";
            }
        }
    }
    if (jumlahNode < MAX_NODE)
    {
        namaNode[jumlahNode] = restoran.namaRestoran;
        jumlahNode++;
    }
    int jumlahMenu = i + 1;
    for (int j = 0; j < jumlahMenu; j++)
    {
        cout << "Menu " << j + 1 << ": " << restoran.menu[j] << " ("
             << restoran.jenisMenu[j] << ") - Rp " << restoran.harga[j] << endl;
    }
    if (jumlahRestoran < MAX_NODE)
    {
        restoranList[jumlahRestoran++] = restoran;
    }
    cout << "Restoran berhasil ditambahkan!\n";
}

void lihatRestoranTersedia()
{
    cout << "\n";
    cout << "=== Daftar Restoran Tersedia ===\n";
    if (jumlahRestoran == 0)
    {
        cout << "Belum ada restoran yang terdaftar.\n";
        return;
    }
    for (int i = 0; i < jumlahRestoran; i++)
    {
        cout << i + 1 << ". " << restoranList[i].namaRestoran << endl;
        for (int j = 0; j < 100; j++)
        {
            if (restoranList[i].menu[j].empty())
                break;
            cout << "   - " << restoranList[i].menu[j]
                 << " (" << restoranList[i].jenisMenu[j] << ")"
                 << " - Rp " << restoranList[i].harga[j] << endl;
        }
    }
}

void cariRestoranGraph(const string &nama)
{
    cout << "\n";
    bool found = false;
    for (int i = 0; i < jumlahRestoran; i++)
    {
        if (restoranList[i].namaRestoran.find(nama) != string::npos)
        {
            cout << "Restoran ditemukan: " << restoranList[i].namaRestoran << endl;
            for (int j = 0; j < 100; j++)
            {
                if (restoranList[i].menu[j].empty())
                    break;
                cout << "   - " << restoranList[i].menu[j]
                     << " (" << restoranList[i].jenisMenu[j] << ")"
                     << " - Rp " << restoranList[i].harga[j] << endl;
            }
            found = true;
        }
    }
    if (!found)
    {
        cout << "Restoran tidak ditemukan.\n";
    }
}

void cariMakanan(const string &namaMakanan)
{
    bool found = false;
    auto toLower = [](const string &z)
    {
        string result = z;
        for (size_t i = 0; i < result.length(); ++i)
            if (result[i] >= 'A' && result[i] <= 'Z')
                result[i] = result[i] - 'A' + 'a';
        return result;
    };

    string cariLower = toLower(namaMakanan);
    for (int i = 0; i < jumlahRestoran; i++)
    {
        for (int j = 0; j < 100; j++)
        {
            if (restoranList[i].menu[j].empty())
                break;
            string menuLower = toLower(restoranList[i].menu[j]);

            if (menuLower.find(cariLower) != string::npos)
            {
                cout << "- " << restoranList[i].menu[j]
                     << " (" << restoranList[i].jenisMenu[j] << ")"
                     << " - Rp " << restoranList[i].harga[j]
                     << " [Restoran: " << restoranList[i].namaRestoran << "]\n";
                found = true;
            }
        }
    }
    if (!found)
    {
        cout << "Makanan tidak ditemukan.\n";
    }
}

void tambahKonsumen(hashtableKonsumen &htKonsumen)
{
    cout <<"\n";
    konsumen *newKonsumen = new konsumen;
    cout << "=== Tambah Konsumen ===\n";
    cout << "Masukkan Nama Konsumen: ";
    cin.ignore();
    getline(cin, newKonsumen->nama);
    if (newKonsumen->nama.empty())
    {
        cout << "Nama konsumen tidak boleh kosong.\n";
        return;
    }

    string id = "";
    do
    {
        for (char c : newKonsumen->nama)
        {
            if (c != ' ')
                id += tolower(c);
            if (id.length() == 3)
                break;
        }
        while (id.length() < 3)
            id += 'x';

        int angka = rand() % 100;
        if (angka < 10)
            id += "0" + to_string(angka);
        else
            id += to_string(angka);
    } while (htKonsumen.searchKonsumen(id) != nullptr);

    newKonsumen->idKonsumen = id;

    cout << "Masukkan Password: ";
    getline(cin, newKonsumen->password);
    htKonsumen.insertKonsumen(newKonsumen);
    cout << "Konsumen berhasil ditambahkan!\n";
    cout << "ID Konsumen Anda: " << newKonsumen->idKonsumen << endl;
}

void tambahKurir(hashtableKurir &htKurir)
{
    cout << "\n";
    kurir *newKurir = new kurir;
    cout << "=== Tambah Kurir ===\n";
    cout << "Masukkan Nama Kurir: ";
    cin.ignore();
    getline(cin, newKurir->nama);
    if (newKurir->nama.empty())
    {
        cout << "Nama kurir tidak boleh kosong.\n";
        return;
    }

    string id;
    do
    {
        id = "";
        for (char c : newKurir->nama)
        {
            if (c != ' ')
                id += tolower(c);
            if (id.length() == 3)
                break;
        }
        while (id.length() < 3)
            id += 'x';

        int angka = rand() % 100;
        if (angka < 10)
            id += "0" + to_string(angka);
        else
            id += to_string(angka);
    } while (htKurir.searchKurir(id) != nullptr);

    newKurir->idKurir = id;

    cout << "Masukkan Password: ";
    getline(cin, newKurir->password);
    newKurir->status = "Aktif";
    htKurir.insertKurir(newKurir);
    cout << "Kurir berhasil ditambahkan!\n";
    cout << "ID Kurir Anda: " << newKurir->idKurir << endl;
}

konsumen *loginKonsumen(hashtableKonsumen &htKonsumen)
{
    cout << "\n";
    string idKonsumen, password;
    cout << "=== Login Konsumen ===\n";
    cout << "Masukkan ID Konsumen: ";
    cin >> idKonsumen;
    cout << "Masukkan Password: ";
    cin >> password;

    konsumen *konsumen = htKonsumen.searchKonsumen(idKonsumen);
    if (konsumen && konsumen->password == password)
    {
        cout << "Login berhasil! Selamat datang, " << konsumen->nama << ".\n";
        return konsumen;
    }
    else
    {
        cout << "ID atau password salah. Silakan coba lagi.\n";
        return nullptr;
    }
}

kurir *loginKurir(hashtableKurir &htKurir)
{
    cout << "\n";
    string idKurir, password;
    cout << "=== Login Kurir ===\n";
    cout << "Masukkan ID Kurir: ";
    cin >> idKurir;
    cout << "Masukkan Password: ";
    cin >> password;

    kurir *kurir = htKurir.searchKurir(idKurir);
    if (kurir && kurir->password == password)
    {
        cout << "Login berhasil! Selamat datang, " << kurir->nama << ".\n";
        return kurir;
    }
    else
    {
        cout << "ID atau password salah. Silakan coba lagi.\n";
        return nullptr;
    }
}

void tampilkanMenuUrutHarga()
{
    struct DataMenu
    {
        string namaMenu;
        float harga;
        string restoran;
        string kategori;
    };
    DataMenu semuaMenu[1000];
    int nMenu = 0;

    for (int i = 0; i < jumlahRestoran; i++)
    {
        for (int j = 0; j < 100; j++)
        {
            if (restoranList[i].menu[j].empty())
                break;
            semuaMenu[nMenu].namaMenu = restoranList[i].menu[j];
            semuaMenu[nMenu].harga = restoranList[i].harga[j];
            semuaMenu[nMenu].restoran = restoranList[i].namaRestoran;
            semuaMenu[nMenu].kategori = restoranList[i].jenisMenu[j];
            nMenu++;
        }
    }

    cout << "Urutkan berdasarkan harga:\n";
    cout << "1. Termurah ke Termahal\n";
    cout << "2. Termahal ke Termurah\n";
    cout << "Pilih: ";
    int urutan;
    cin >> urutan;

    for (int i = 0; i < nMenu - 1; i++)
    {
        for (int j = 0; j < nMenu - i - 1; j++)
        {
            bool swap = false;
            if (urutan == 1 && semuaMenu[j].harga > semuaMenu[j + 1].harga)
                swap = true;
            else if (urutan == 2 && semuaMenu[j].harga < semuaMenu[j + 1].harga)
                swap = true;
            if (swap)
            {
                DataMenu temp = semuaMenu[j];
                semuaMenu[j] = semuaMenu[j + 1];
                semuaMenu[j + 1] = temp;
            }
        }
    }

    cout << "\n";
    cout << "=== Daftar Menu Makanan Urut Harga ===\n";
    for (int i = 0; i < nMenu; i++)
    {
        cout << i + 1 << ". " << semuaMenu[i].namaMenu
             << " (" << semuaMenu[i].kategori << ")"
             << " - Rp " << semuaMenu[i].harga
             << " [Restoran: " << semuaMenu[i].restoran << "]\n";
    }
    if (nMenu == 0)
        cout << "Belum ada menu makanan yang terdaftar.\n";
}

void menuKonsumenLengkap(konsumen *konsumen)
{
    while (true)
    {
        cout << "\n";
        cout << "=== Menu Konsumen ===\n";
        cout << "1. Buat Pesanan\n";
        cout << "2. Cari Restoran\n";
        cout << "3. Cari Makanan\n";
        cout << "4. Daftar Restoran\n";
        cout << "5. Rekomendasi Makanan\n";
        cout << "6. Urutkan Menu Makanan Berdasarkan Harga\n";
        cout << "7. Kembali\n";
        cout << "8. Exit\n";
        cout << "Pilih: ";
        int pilihan;
        cin >> pilihan;
        cin.ignore();

        if (pilihan == 1)
        {
            if (jumlahRestoran == 0)
            {
                cout << "Belum ada restoran yang tersedia.\n";
                continue;
            }
            cout << "\n";
            cout << "=== Buat Pesanan ===\n";
            cout << "Daftar restoran:\n";
            for (int i = 0; i < jumlahRestoran; i++)
            {
                cout << i + 1 << ". " << restoranList[i].namaRestoran << endl;
            }
            cout << "Pilih nomor restoran: ";
            int idxRestoran;
            cin >> idxRestoran;
            cin.ignore();
            if (idxRestoran < 1 || idxRestoran > jumlahRestoran)
            {
                cout << "Pilihan tidak valid.\n";
                continue;
            }
            string namaRestoran = restoranList[idxRestoran - 1].namaRestoran;

            restoran *restoDipilih = nullptr;
            for (int i = 0; i < jumlahRestoran; i++)
            {
                if (restoranList[i].namaRestoran == namaRestoran)
                {
                    restoDipilih = &restoranList[i];
                    break;
                }
            }
            if (!restoDipilih)
            {
                cout << "Data menu restoran tidak ditemukan.\n";
                continue;
            }
            cout << "Menu di " << namaRestoran << ":\n";
            int jumlahMenu = 0;
            while (!restoDipilih->menu[jumlahMenu].empty() && jumlahMenu < 100)
                jumlahMenu++;
            for (int i = 0; i < jumlahMenu; i++)
            {
                cout << i + 1 << ". " << restoDipilih->menu[i]
                     << " (" << restoDipilih->jenisMenu[i] << ") - Rp " << restoDipilih->harga[i] << endl;
            }
            if (jumlahMenu == 0)
            {
                cout << "Tidak ada menu yang tersedia di restoran ini.\n";
                continue;
            }

            int pesananMenuIdx[100];
            int pesananJumlah[100];
            int pesananCount = 0;
            while (true)
            {
                cout << "Pilih nomor menu yang ingin dipesan (0 untuk selesai): ";
                int pilihMenu;
                cin >> pilihMenu;
                if (pilihMenu == 0)
                    break;
                if (pilihMenu < 1 || pilihMenu > jumlahMenu)
                {
                    cout << "Pilihan tidak valid.\n";
                    continue;
                }
                cout << "Jumlah: ";
                int qty;
                cin >> qty;
                if (qty < 1)
                {
                    cout << "Jumlah minimal 1.\n";
                    continue;
                }
                pesananMenuIdx[pesananCount] = pilihMenu - 1;
                pesananJumlah[pesananCount] = qty;
                pesananCount++;
            }
            cin.ignore();

            cout << "Konfirmasi pesanan Anda:\n";
            int total = 0;
            for (int i = 0; i < pesananCount; i++)
            {
                int idx = pesananMenuIdx[i];
                int qty = pesananJumlah[i];
                int subtotal = restoDipilih->harga[idx] * qty;
                cout << "- " << restoDipilih->menu[idx] << " x" << qty << " = Rp " << subtotal << endl;
                total += subtotal;
            }
            cout << "Total: Rp " << total << endl;
            cout << "Lanjutkan pemesanan? (y/n): ";
            char konfirmasi;
            cin >> konfirmasi;
            cin.ignore();
            if (konfirmasi != 'y' && konfirmasi != 'Y')
            {
                cout << "Pesanan dibatalkan.\n";
                continue;
            }

            string alamatTujuan;
            cout << "Masukkan alamat tujuan: ";
            getline(cin, alamatTujuan);

            tambahNode(alamatTujuan);
            
            int idxRestoranGraph = -1;
            int idxAlamatGraph = -1;
            for (int i = 0; i < jumlahNode; i++) {
                if (namaNode[i] == namaRestoran) idxRestoranGraph = i;
                if (namaNode[i] == alamatTujuan) idxAlamatGraph = i;
            }
            
            if (idxRestoranGraph != -1 && idxAlamatGraph != -1 && adjMatrix[idxRestoranGraph][idxAlamatGraph] == 0) {
                int jarak;
                cout << "Masukkan jarak dari " << namaRestoran << " ke " << alamatTujuan << " (meter): ";
                cin >> jarak;
                cin.ignore();
                tambahEdge(namaRestoran, alamatTujuan, jarak);
            } else {
                        cout << "Alamat tujuan sudah terhubung ke restoran. Tidak perlu input jarak.\n";
                }

            pesanan *p = new pesanan;
            p->idPesanan = "PSN" + to_string(rand() % 10000);
            p->pengirim = "-";
            p->konsumen = konsumen->nama;
            p->restoran = namaRestoran;
            p->alamatTujuan = alamatTujuan;
            p->status = "Menunggu";
            p->next = nullptr;
            p->prev = nullptr;

            if (headPesanan == nullptr)
            {
                headPesanan = tailPesanan = p;
            }
            else
            {
                tailPesanan->next = p;
                p->prev = tailPesanan;
                tailPesanan = p;
            }

            queueKonfirmasi.enqueue(p);

            cout << "Pesanan berhasil dibuat!\n";
            cout << "ID Pesanan: " << p->idPesanan << endl;
        }
        else if (pilihan == 2)
        {
            cout << "\n";
            cout << "=== Cari Restoran ===\n";
            cout << "Masukkan nama restoran: ";
            string namaRestoran;
            getline(cin, namaRestoran);
            cout << "Hasil pencarian restoran: " << endl;
            cariRestoranGraph(namaRestoran);
        }
        else if (pilihan == 3)
        {
            cout << "\n";
            cout << "=== Cari Makanan ===\n";
            cout << "Masukkan nama makanan: ";
            string namaMakanan;
            getline(cin, namaMakanan);
            cout << "Hasil pencarian makanan: " << endl;
            cariMakanan(namaMakanan);
        }
        else if (pilihan == 4)
        {
            cout << "\n";
            cout << "Daftar restoran:\n";
            for (int i = 0; i < jumlahRestoran; i++)
            {
                cout << i + 1 << ". " << restoranList[i].namaRestoran << endl;
            }
        }
        else if (pilihan == 5)
        {
            cout << "\n";
            cout << "=== Rekomendasi Menu ===\n";
            cout << "Pilih kategori makanan:\n";
            cout << "1. Makanan Berat\n";
            cout << "2. Makanan Ringan\n";
            cout << "3. Minuman\n";
            cout << "4. Kembali\n";
            cout << "5. Exit\n";
            cout << "Pilih: ";
            int pilihKat;
            cin >> pilihKat;
            cin.ignore();
            string kategori;
            if (pilihKat == 1)
                kategori = "Makanan Berat";
            else if (pilihKat == 2)
                kategori = "Makanan Ringan";
            else if (pilihKat == 3)
                kategori = "Minuman";
            else if (pilihKat == 4)
                return;
            else if (pilihKat == 5)
                exit(0);
            else
            {
                cout << "Pilihan tidak valid.\n";
                continue;
            }
            rekomendasiFleksibel(kategori);
        }
        else if (pilihan == 6)
        {
            cout << "\n";
            cout << "=== Urutan harga Menu Makanan ===\n";
            tampilkanMenuUrutHarga();
        }
        else if (pilihan == 7)
        {
            cout << "Kembali.\n";
            return;
        }
        else if (pilihan == 8)
        {
            cout << "Keluar dari program.\n";
            exit(0);
        }
        else
        {
            cout << "Pilihan tidak valid.\n";
        }
    }
}

struct StackPesanan
{
    pesanan *data[200];
    int top;
    StackPesanan() { top = -1; }
    void push(pesanan *p)
    {
        if (top < 199)
            data[++top] = p;
    }
    pesanan *pop()
    {
        if (top >= 0)
            return data[top--];
        else
            return nullptr;
    }
    bool isEmpty() { return top == -1; }
};

void hapusPesananKonsumen(const string &namaKonsumen)
{
    cout << "\n";
    cout << "=== Hapus Pesanan ===\n";
    bool ada = false;
    pesanan *temp = headPesanan;
    int idx = 1;
    while (temp != nullptr)
    {
        if (temp->konsumen == namaKonsumen && temp->status == "Menunggu")
        {
            cout << idx << ". ID: " << temp->idPesanan
                 << ", Restoran: " << temp->restoran
                 << ", Alamat: " << temp->alamatTujuan << endl;
            ada = true;
            idx++;
        }
        temp = temp->next;
    }
    if (!ada)
    {
        cout << "Tidak ada pesanan yang bisa dihapus (hanya pesanan berstatus 'Menunggu' yang bisa dihapus).\n";
        return;
    }
    cout << "Masukkan ID Pesanan yang ingin dihapus (atau 0 untuk batal): ";
    string idHapus;
    getline(cin, idHapus);
    if (idHapus == "0")
        return;
    pesanan *hps = headPesanan;
    while (hps != nullptr)
    {
        if (hps->idPesanan == idHapus && hps->konsumen == namaKonsumen && hps->status == "Menunggu")
        {
            if (hps->idPesanan == idHapus && hps->konsumen == namaKonsumen && hps->status == "Menunggu") {
                hps->status = "Dibatalkan";
                cout << "Pesanan berhasil dibatalkan.\n";
                return;
            }
            cout << "Pesanan berhasil dihapus.\n";
            return;
        }
        hps = hps->next;
    }
    cout << "ID Pesanan tidak ditemukan atau tidak bisa dihapus.\n";
}

void riwayatPesananKonsumen(const string &namaKonsumen)
{
    StackPesanan rpk;
    pesanan *temp = headPesanan;
    while (temp != nullptr)
    {
        if (temp->konsumen == namaKonsumen)
        {
            rpk.push(temp);
        }
        temp = temp->next;
    }
    
    cout << "=== Riwayat Pesanan Anda (Terbaru di atas) ===\n";
    int idx = 1;
    while (!rpk.isEmpty())
    {
        pesanan *p = rpk.pop();
        cout << idx++ << ". ID: " << p->idPesanan
             << ", Restoran: " << p->restoran
             << ", Alamat: " << p->alamatTujuan
             << ", Status: " << p->status << endl;
    }
    if (idx == 1)
        cout << "Belum ada riwayat pesanan.\n";
}

void riwayatPesananKurir(const string &namaKurir)
{
    StackPesanan rpk;
    pesanan *temp = headPesanan;
    while (temp != nullptr)
    {
        if (temp->pengirim == namaKurir)
        {
            rpk.push(temp);
        }
        temp = temp->next;
    }
    cout << "=== Riwayat Pesanan yang Diantar (Terbaru di atas) ===\n";
    int idx = 1;
    while (!rpk.isEmpty())
    {
        pesanan *p = rpk.pop();
        cout << idx++ << ". ID: " << p->idPesanan
             << ", Konsumen: " << p->konsumen
             << ", Restoran: " << p->restoran
             << ", Alamat: " << p->alamatTujuan
             << ", Status: " << p->status << endl;
    }
    if (idx == 1)
        cout << "Belum ada riwayat pesanan.\n";
}

void adminMenu()
{
    while (true)
    {
        cout << "\n";
        cout << "=== Admin Menu ===\n";
        cout << "1. Tambah Restoran\n";
        cout << "2. Lihat Restoran tersedia\n";
        cout << "3. Konfirmasi Pesanan\n";
        cout << "4. lihat Graph\n";
        cout << "5. Kembali ke Menu Utama\n";
        cout << "6. Exit\n";
        cout << "Pilih: ";
        int adminPilihan;
        cin >> adminPilihan;
        if (adminPilihan == 1)
        {
            addRestoran();
        }
        else if (adminPilihan == 2)
        {
            cout << "Daftar Restoran:\n";
            lihatRestoranTersedia();
        }
        else if (adminPilihan == 3)
        {
            cout << "\n";
            cout << "=== Antrian Konfirmasi Pesanan ===\n";
            queueKonfirmasi.tampilkanQueue();
            if (!queueKonfirmasi.isEmpty())
            {
                cout << "Konfirmasi pesanan terdepan? (Y/N): ";
                string konfirmasi;
                cin >> konfirmasi;
                if (konfirmasi == "y" || konfirmasi == "Y")
                {
                    pesanan *pKonfirm = queueKonfirmasi.dequeue();
                    if (pKonfirm)
                    {
                        pKonfirm->status = "Dikonfirmasi Restoran";
                        cout << "Pesanan " << pKonfirm->idPesanan << " telah dikonfirmasi!\n";
                    }
                }
            }
        }

        else if (adminPilihan == 4)
        {
            tampilkanGraph();
        }
        else if (adminPilihan == 5)
        {
            cout << "Kembali ke menu utama.\n";
            break;
        }
        else if (adminPilihan == 6)
        {
            cout << "Keluar dari program.\n";
        }
    }
}

void tampilkanPesananSiapDiambil()
{
    pesanan *temp = headPesanan;
    int idx = 1;
    while (temp != nullptr)
    {
        if (temp->status == "Dikonfirmasi Restoran")
        {
            cout << idx << ". ID: " << temp->idPesanan
                 << ", Konsumen: " << temp->konsumen
                 << ", Restoran: " << temp->restoran
                 << ", Alamat: " << temp->alamatTujuan << endl;
            idx++;
        }
        temp = temp->next;
    }
    if (idx == 1)
        cout << "Tidak ada pesanan yang siap diambil.\n";
}

void kurirMenuUtama(kurir *kurir)
{
    while (true)
    {
        cout << "\n";
        cout << "=== Menu Kurir ===\n";
        cout << "1. Ambil Pesanan\n";
        cout << "2. Status Pesanan\n";
        cout << "3. Lihat Riwayat Pesanan\n";
        cout << "4. konfirmasi Pesanan Sampai\n";
        cout << "5. Kembali\n";
        cout << "6. Exit\n";
        cout << "Pilih: ";
        int pilihan;
        cin >> pilihan;
        cin.ignore();
        if (pilihan == 1)
        {
            cout << "\n";
            cout << "=== Pesanan Siap Diambil ===\n";
            int pesananAktif = 0;
            pesanan *tmp = headPesanan;
            while (tmp != nullptr)
            {
                if (tmp->pengirim == kurir->nama && tmp->status == "Sedang Diantar")
                    pesananAktif++;
                tmp = tmp->next;
            }
            if (pesananAktif >= 1)
            {
                cout << "Kurir hanya boleh menerima 1 pesanan. Selesaikan pengantaran sebelumnya terlebih dahulu.\n";
                continue;
            }
            tampilkanPesananSiapDiambil();
            cout << "Masukkan ID Pesanan yang ingin diambil (atau 0 untuk batal): ";
            string idAmbil;
            getline(cin, idAmbil);
            if (idAmbil == "0")
                continue;
            pesanan *temp = headPesanan;
            bool found = false;
            while (temp != nullptr)
            {
                if (temp->idPesanan == idAmbil && temp->status == "Dikonfirmasi Restoran")
                {
                    temp->status = "Sedang Diantar";
                    temp->pengirim = kurir->nama;
                    cout << "Pesanan " << temp->idPesanan << " berhasil diambil oleh " << kurir->nama << "!\n";
                    found = true;
                    break;
                }
                temp = temp->next;
            }
            if (!found)
            {
                cout << "ID Pesanan tidak ditemukan atau belum siap diambil.\n";
            }
        }
        else if (pilihan == 2)
        {
            cout << "\n";
            cout << "=== Status Pesanan ===\n";
            cout << "Masukkan ID Pesanan yang ingin dilihat statusnya: ";
            string idStatus;
            getline(cin, idStatus);
            pesanan *temp = headPesanan;
            bool found = false;
            while (temp != nullptr)
            {
                if (temp->idPesanan == idStatus)
                {
                    cout << "ID Pesanan: " << temp->idPesanan
                         << ", Konsumen: " << temp->konsumen
                         << ", Restoran: " << temp->restoran
                         << ", Alamat: " << temp->alamatTujuan
                         << ", Status: " << temp->status << endl;
                    found = true;
                    break;
                }
                temp = temp->next;
            }
        }
        else if (pilihan == 3)
        {
            cout << "\n";
            riwayatPesananKurir(kurir->nama);
        }
        else if (pilihan == 4)
        {
            cout << "\n";
            cout << "=== Konfirmasi Pesanan Sampai ===\n";
            pesanan *tmp = headPesanan;
            int idx = 1;
            while (tmp != nullptr)
            {
                if (tmp->pengirim == kurir->nama && tmp->status == "Sedang Diantar")
                {
                    cout << idx++ << ". ID: " << tmp->idPesanan
                         << ", Konsumen: " << tmp->konsumen
                         << ", Alamat: " << tmp->alamatTujuan << endl;
                }
                tmp = tmp->next;
            }
            if (idx == 1)
            {
                cout << "Tidak ada pesanan yang sedang diantar.\n";
                return;
            }
            cout << "Masukkan ID Pesanan yang sudah sampai (atau 0 untuk batal): ";
            string idKonfirmasi;
            getline(cin, idKonfirmasi);
            if (idKonfirmasi == "0")
                return;
            tmp = headPesanan;
            bool found = false;
            while (tmp != nullptr)
            {
                if (tmp->idPesanan == idKonfirmasi && tmp->pengirim == kurir->nama && tmp->status == "Sedang Diantar")
                {
                    tmp->status = "Sampai";
                    cout << "Pesanan " << tmp->idPesanan << " telah dikonfirmasi sampai!\n";
                    found = true;
                    break;
                }
                tmp = tmp->next;
            }
            if (!found)
            {
                cout << "ID Pesanan tidak ditemukan atau belum bisa dikonfirmasi.\n";
            }
        }
        else if (pilihan == 5)
        {
            cout << "Kembali ke menu utama.\n";
            cout << "\n";
            break;
        }
        else if (pilihan == 6)
        {
            cout << "Keluar dari program.\n";
            exit(0);
        }
        else
        {
            cout << "Pilihan tidak valid.\n";
        }
    }
}

void kurirMenu(hashtableKurir &htKurir)
{
    while (true)
    {
        cout << "\n";
        cout << "=== Kurir login Menu ===\n";
        cout << "1. Login Kurir\n";
        cout << "2. Buat akun\n";
        cout << "3. Kembali ke Menu Utama\n";
        cout << "4. Exit\n";
        cout << "Pilih: ";
        int kurirPilihan;
        cin >> kurirPilihan;
        if (kurirPilihan == 1)
        {
            kurir *kurir = loginKurir(htKurir);
            if (kurir)
            {
                cout << "Selamat datang, " << kurir->nama << ".\n";
                kurirMenuUtama(kurir);
            }
        }
        else if (kurirPilihan == 2)
        {
            tambahKurir(htKurir);
        }
        else if (kurirPilihan == 3)
        {
            cout << "Kembali ke menu utama.\n";
            cout << "\n";
            break;
        }
        else if (kurirPilihan == 4)
        {
            cout << "Keluar dari program.\n";
            exit(0);
        }
    }
}

void konsumenMenuUtama(konsumen *konsumen)
{
    while (true)
    {
        cout << "\n";
        cout << "=== Menu Konsumen ===\n";
        cout << "1. Buat Pesanan\n";
        cout << "2. Lihat Riwayat Pesanan\n";
        cout << "3. Lihat Status Pesanan\n";
        cout << "4. Konfirmasi Pesanan Sampai\n";
        cout << "5. Hapus Pesanan\n";
        cout << "6. Kembali\n";
        cout << "7. Exit\n";
        cout << "Pilih: ";
        int pilihan;
        cin >> pilihan;
        cin.ignore();
        if (pilihan == 1)
        {
            menuKonsumenLengkap(konsumen);
        }
        else if (pilihan == 2)
        {
            cout << "\n";
            riwayatPesananKonsumen(konsumen->nama);
        }
        else if (pilihan == 3)
        {
            cout << "\n";
            cout << "=== Lihat Status Pesanan ===\n";
            cout << "Masukkan ID Pesanan yang ingin dilihat statusnya: ";
            string idStatus;
            getline(cin, idStatus);
            pesanan *temp = headPesanan;
            bool found = false;
            while (temp != nullptr)
            {
                if (temp->idPesanan == idStatus && temp->konsumen == konsumen->nama)
                {
                    cout << "ID Pesanan: " << temp->idPesanan
                         << ", Restoran: " << temp->restoran
                         << ", Alamat: " << temp->alamatTujuan
                         << ", Status: " << temp->status << endl;
                    found = true;
                    break;
                }
                else
                {
                    cout << "ID Pesanan tidak ditemukan.\n";
                }
                temp = temp->next;
            }
        }
        else if (pilihan == 4)
        {
            cout << "\n";
            cout << "=== Konfirmasi Pesanan Sampai ===\n";
            pesanan *temp = headPesanan;
            int idx = 1;
            bool ada = false;
            while (temp != nullptr)
            {
                if (temp->konsumen == konsumen->nama && temp->status == "Sedang Diantar")
                {
                    cout << idx << ". ID: " << temp->idPesanan
                         << ", Restoran: " << temp->restoran
                         << ", Alamat: " << temp->alamatTujuan
                         << ", Kurir: " << temp->pengirim << endl;
                    ada = true;
                    idx++;
                }
                temp = temp->next;
            }
            if (!ada)
            {
                cout << "Tidak ada pesanan yang sedang diantar.\n";
            }
            else
            {
                cout << "Masukkan ID Pesanan yang sudah sampai (atau 0 untuk batal): ";
                string idKonfirmasi;
                getline(cin, idKonfirmasi);
                if (idKonfirmasi != "0")
                {
                    temp = headPesanan;
                    bool found = false;
                    while (temp != nullptr)
                    {
                        if (temp->idPesanan == idKonfirmasi && temp->konsumen == konsumen->nama && temp->status == "Sedang Diantar")
                        {
                            temp->status = "Sampai";
                            cout << "Pesanan " << temp->idPesanan << " telah dikonfirmasi sampai!\n";
                            found = true;
                            break;
                        }
                        temp = temp->next;
                    }
                    if (!found)
                    {
                        cout << "ID Pesanan tidak ditemukan atau belum bisa dikonfirmasi.\n";
                    }
                }
            }
        }
        else if (pilihan == 5)
        {
            hapusPesananKonsumen(konsumen->nama);
        }
        else if (pilihan == 6)
        {
            cout << "Kembali ke menu utama.\n";
            cout << "\n";
            break;
        }
        else if (pilihan == 7)
        {
            cout << "Keluar dari program.\n";
            exit(0);
        }
    }
}

void konsumenMenu(hashtableKonsumen &htKonsumen)
{
    while (true)
    {
        cout << "\n";
        cout << "=== Konsumen login Menu ===\n";
        cout << "1. Login Konsumen\n";
        cout << "2. Buat akun\n";
        cout << "3. Kembali ke menu utama\n";
        cout << "4. Exit\n";
        cout << "Pilih: ";
        int konsumenPilihan;
        cin >> konsumenPilihan;
        if (konsumenPilihan == 1)
        {
            konsumen *konsumen = loginKonsumen(htKonsumen);
            if (konsumen)
            {
                cout << "Selamat datang, " << konsumen->nama << ".\n";
                konsumenMenuUtama(konsumen);
            }
        }
        else if (konsumenPilihan == 2)
        {
            tambahKonsumen(htKonsumen);
        }
        else if (konsumenPilihan == 3)
        {
            cout << "Kembali ke menu utama.\n";
            break;
        }
        else if (konsumenPilihan == 4)
        {
            cout << "Keluar dari program.\n";
            exit(0);
        }
    }
}

int main()
{
    hashtableKonsumen htKonsumen;
    hashtableKurir htKurir;
    while (true)
    {
        cout << "\n";
        cout << "=== Selamat Datang di Aplikasi Pengantaran Makanan ===\n";
        cout << "=== Login Sebagai ===\n";
        cout << "1. Admin\n";
        cout << "2. Kurir\n";
        cout << "3. Konsumen\n";
        cout << "4. Exit\n";
        int pilihan;
        cout << "Pilih: ";
        cin >> pilihan;
        cin.ignore();
        if (pilihan == 1)
        {
            adminMenu();
        }
        else if (pilihan == 2)
        {
            kurirMenu(htKurir);
        }
        else if (pilihan == 3)
        {
            konsumenMenu(htKonsumen);
        }
        else if (pilihan == 4)
        {
            cout << "Keluar dari program.\n";
            break;
        }
        else
        {
            cout << "Pilihan tidak valid.\n";
        }
    }
    return 0;
}