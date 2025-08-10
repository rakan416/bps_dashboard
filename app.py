from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from flask_sqlalchemy import SQLAlchemy # Impor SQLAlchemy
from werkzeug.utils import secure_filename
from sqlalchemy.sql import func
import pandas as pd
import os
import io


app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- KONFIGURASI DATABASE ---
# Format URI: postgresql://[user]:[password]@[host]:[port]/[dbname]
# Ganti dengan detail database Anda
link_DB = 'postgresql://postgres.rvlsrtvgpnvevbhzmgik:medalion19@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = link_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Opsional, untuk menonaktifkan notifikasi yang tidak perlu

# Inisialisasi objek database
db = SQLAlchemy(app)

class Dashboard(db.Model):
    # Ganti 'nama_tabel_dashboard' dengan nama tabel Anda yang sebenarnya di PostgreSQL
    __tablename__ = 'data_dashboard'

    # Asumsi 'id' adalah Primary Key
    id = db.Column('id_data', db.Integer, primary_key=True)

    id_landmark = db.Column('id_landmark', db.String, nullable=True)
    id_alokasi = db.Column('id_alokasi', db.String(255), nullable=True)
    user_created_at = db.Column('user_created_at', db.String(255), nullable=True)
    user_upload_at = db.Column('user_upload_at', db.String(255), nullable=True)
    timestamp = db.Column('Timestamp', db.String(255), nullable=True)
    wid = db.Column('wid', db.String(255), nullable=True)
    nama = db.Column('nama', db.String(255), nullable=True)
    nm_project = db.Column('nm_project', db.String(255), nullable=True)
    deskripsi_project = db.Column('deskripsi_project', db.String(255), nullable=True)
    iddesa = db.Column('iddesa', db.String(255), nullable=True)
    accuracy = db.Column('accuracy', db.String(255), nullable=True)
    status = db.Column('status', db.String(255), nullable=True)
    kode_kategori = db.Column('kode_kategori', db.String(255), nullable=True)
    kategori_landmark = db.Column('kategori_landmark', db.String(255), nullable=True)
    kode_landmark_tipe = db.Column('kode_landmark_tipe', db.String(255), nullable=True)
    tipe_landmark = db.Column('tipe_landmark', db.String(255), nullable=True)
    user_creator_nama = db.Column('user_creator_nama', db.String(255), nullable=True)
    photo_url = db.Column('photo_url', db.String(255), nullable=True)
    idsls = db.Column('idsls', db.String(255), nullable=True)
    latlon = db.Column('latlon', db.String(255), nullable=True)
    semester = db.Column('semester', db.String(255), nullable=True)
    idsubsls = db.Column('idsubsls', db.String(255), nullable=True)
    nmsls = db.Column('nmsls', db.String(255), nullable=True)
    nama_ketua = db.Column('nama_ketua', db.String(255), nullable=True)
    jenis = db.Column('jenis', db.String(255), nullable=True)
    kdprov = db.Column('kdprov', db.String(255), nullable=True)
    nmprov = db.Column('nmprov', db.String(255), nullable=True)
    kdkab = db.Column('kdkab', db.String(255), nullable=True)
    nmkab = db.Column('nmkab', db.String(255), nullable=True)
    kdkec = db.Column('kdkec', db.String(255), nullable=True)
    nmkec = db.Column('nmkec', db.String(255), nullable=True)
    kddesa = db.Column('kddesa', db.String(255), nullable=True)
    nmdesa = db.Column('nmdesa', db.String(255), nullable=True)
    klas = db.Column('klas', db.String(255), nullable=True)
    kdsls = db.Column('kdsls', db.String(255), nullable=True)
    kdsubsls = db.Column('kdsubsls', db.String(255), nullable=True)
    jumlah_kk = db.Column('jumlah_kk', db.String(255), nullable=True)
    jumlah_bstt = db.Column('jumlah_bstt', db.String(255), nullable=True)
    jumlah_bsbtt = db.Column('jumlah_bsbtt', db.String(255), nullable=True)
    jumlah_bsttk = db.Column('jumlah_bsttk', db.String(255), nullable=True)
    jumlah_bskeko = db.Column('jumlah_bskeko', db.String(255), nullable=True)
    dominan = db.Column('dominan', db.String(255), nullable=True)
    pemeta = db.Column('PEMETA', db.String(255), nullable=True)
    email_pemeta = db.Column('EMAIL_PEMETA', db.String(255), nullable=True)
    pengawas = db.Column('PENGAWAS', db.String(255), nullable=True)
    email_pengawas = db.Column('EMAIL_PENGAWAS', db.String(255), nullable=True)
    kode_kecamatan = db.Column('KODE_KECAMATAN', db.String(255), nullable=True)
    kode_desa = db.Column('KODE_DESA', db.String(255), nullable=True)
    kode_sls_non_sls = db.Column('KODE_SLS/NON_SLS', db.String(255), nullable=True)
    kode_sls = db.Column('KODE_SLS', db.String(255), nullable=True)
    nama_sls_non_sls = db.Column('NAMA_SLS_/_NON_SLS_(contoh:_RT_001_RW_001)', db.String(255), nullable=True)
    perkiraan_jumlah_muatan_kk = db.Column('PERKIRAAN_JUMLAH_MUATAN_KK', db.String(255), nullable=True)
    perkiraan_jumlah_usaha = db.Column('PERKIRAAN_JUMLAH_USAHA_INFO_DARI_PAK_RT', db.String(255), nullable=True)
    jumlah_bangunan_tempat_tinggal = db.Column('JUMLAH_BANGUNAN_TEMPAT_TINGGAL_(BTT)', db.String(255), nullable=True)
    jumlah_bangunan_tempat_tinggal_kosong = db.Column('JUMLAH_BANGUNAN_TEMPAT_TINGGAL_KOSONG_(BTT_KOSONG)', db.String(255), nullable=True)
    jumlah_bangunan_khusus_usaha = db.Column('JUMLAH_BANGUNAN_KHUSUS_USAHA_(BKU)', db.String(255), nullable=True)
    jumlah_bangunan_bukan_tempat_tinggal = db.Column('JUMLAH_BANGUNAN_BUKAN_TEMPAT_TINGGAL_(BBTT_NON_USAHA)', db.String(255), nullable=True)
    perkiraan_jumlah_muatan_usaha = db.Column('PERKIRAAN_JUMLAH_MUATAN_USAHA', db.String(255), nullable=True)
    total_muatan = db.Column('TOTAL_MUATAN_(MAKS_BTT,KK_+_BTT_+BTTK_+_BBTT_NON_USAHA)', db.String(255), nullable=True)
    apakah_ada_perubahan_batas = db.Column('APAKAH_ADA_PERUBAHAN_BATAS_PADA_SLS_TERSEBUT?', db.String(255), nullable=True)

    def __repr__(self):
        return f'<Dashboard Data ID: {self.id}>'


# ... setelah app = Flask(__name__) ...
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def index():
    try:
        # Jalankan query sederhana
        db.session.execute(db.text('SELECT 1'))
        return redirect(url_for('upload_file'))
    except Exception as e:
        # Jika terjadi error, tampilkan pesan errornya
        return f'<h1>Koneksi ke database gagal.</h1><p>Error: {e}</p>'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        # 1. Cek apakah ada file di dalam request
        # if 'file_excel' not in request.files:
        #     flash('Tidak ada bagian file!', 'error')
        #     return redirect(request.url)
        
        file_alokasi = request.files['alokasi']
        file_landmark = request.files['landmark']
        file_rekap_lkm = request.files['rekap_lkm']

        # 2. Cek apakah pengguna memilih file
        if file_landmark.filename == '':
            flash('Tidak ada file yang dipilih!', 'error')
            return redirect(request.url)

        # 3. Cek apakah file valid dan memiliki ekstensi yang diizinkan
        if file_alokasi and allowed_file(file_alokasi.filename):
            try:
                df_alokasi = pd.read_excel(file_alokasi, sheet_name=None, dtype=str)
                KEC = df_alokasi['3519']['kdkec'].unique()
                df_main = df_alokasi['3519'].drop(columns=['PEMETA', 'PENGAWAS', 'PENGOLAH']).copy()
                all_kec = []
                for k in KEC:
                    all_kec.append(df_alokasi[k][['id', 'PEMETA', 'EMAIL PEMETA', 'PENGAWAS', 'EMAIL PENGAWAS']])
                df_all_kec = pd.concat(all_kec, ignore_index=True)
                df_main = df_main.merge(df_all_kec, how='left', on='id')
                df_main['idsls'] = df_main['idsubsls'].str.slice(0, 14)
                df_main.rename(columns={'id':'id_alokasi'}, inplace=True)
                df_landmark = pd.read_excel(file_landmark, dtype=str)
                df_landmark['idsls'] = df_landmark['iddesa'] + df_landmark['nm_project']
                df_landmark['latlon'] = df_landmark['latitude'] + ',' + df_landmark['longitude']
                df_landmark.rename(columns={'id':'id_landmark'}, inplace=True)
                df_landmark.drop(columns=['latitude', 'longitude'], inplace=True)
                df_main = df_landmark.merge(df_main, how='outer', on='idsls')
                df_LKM = pd.read_excel(file_rekap_lkm, sheet_name='Form Responses 1', dtype=str)
                df_LKM['idsls'] = '3519'+df_LKM['KODE SLS']
                df_main = df_main.merge(df_LKM, on='idsls', how='outer')
                kolom = df_main.columns
                for col in kolom:
                    if ' ' in str(col):
                        new_col = col.replace(' ', '_')
                        df_main.rename(columns={col:new_col}, inplace=True)
                df_main.reset_index(drop=True, inplace=True)

                num_rows_deleted = Dashboard.query.delete()
                print(num_rows_deleted)
                for index, row in df_main.iterrows():
                        # if str(row.get('id_x')) == 'nan':
                        #     continue

                        new_dashboard_data = Dashboard(
                            id=index,
                            id_landmark=row.get('id_landmark'),
                            id_alokasi=row.get('id_alokasi'),
                            wid=row.get('wid'),
                            nama=row.get('nama'),
                            nm_project=row.get('nm_project'),
                            deskripsi_project=row.get('deskripsi_project'),
                            iddesa=row.get('iddesa'),
                            accuracy=row.get('accuracy'),
                            status=row.get('status'),
                            kode_kategori=row.get('kode_kategori'),
                            kategori_landmark=row.get('kategori_landmark'),
                            kode_landmark_tipe=row.get('kode_landmark_tipe'),
                            tipe_landmark=row.get('tipe_landmark'),
                            user_created_at=row.get('user_created_at'),
                            user_upload_at=row.get('user_upload_at'),
                            user_creator_nama=row.get('user_creator_nama'),
                            photo_url=row.get('photo_url'),
                            idsls=row.get('idsls'),
                            latlon=row.get('latlon'),
                            semester=row.get('semester'),
                            idsubsls=row.get('idsubsls'),
                            nmsls=row.get('nmsls'),
                            nama_ketua=row.get('nama_ketua'),
                            jenis=row.get('jenis'),
                            kdprov=row.get('kdprov'),
                            nmprov=row.get('nmprov'),
                            kdkab=row.get('kdkab'),
                            nmkab=row.get('nmkab'),
                            kdkec=row.get('kdkec'),
                            nmkec=row.get('nmkec'),
                            kddesa=row.get('kddesa'),
                            nmdesa=row.get('nmdesa'),
                            klas=row.get('klas'),
                            kdsls=row.get('kdsls'),
                            kdsubsls=row.get('kdsubsls'),
                            jumlah_kk=row.get('jumlah_kk'),
                            jumlah_bstt=row.get('jumlah_bstt'),
                            jumlah_bsbtt=row.get('jumlah_bsbtt'),
                            jumlah_bsttk=row.get('jumlah_bsttk'),
                            jumlah_bskeko=row.get('jumlah_bskeko'),
                            dominan=row.get('dominan'),
                            pemeta=row.get('PEMETA'),
                            email_pemeta=row.get('EMAIL_PEMETA'),
                            pengawas=row.get('PENGAWAS'),
                            email_pengawas=row.get('EMAIL_PENGAWAS'),
                            timestamp=row.get('Timestamp'),
                            kode_kecamatan=row.get('KODE_KECAMATAN'),
                            kode_desa=row.get('KODE_DESA'),
                            kode_sls_non_sls=row.get('KODE_SLS/NON_SLS'),
                            kode_sls=row.get('KODE_SLS'),
                            nama_sls_non_sls=row.get('NAMA_SLS_/_NON_SLS_(contoh:_RT_001_RW_001)'),
                            perkiraan_jumlah_muatan_kk=row.get('PERKIRAAN_JUMLAH_MUATAN_KK'),
                            perkiraan_jumlah_usaha=row.get('PERKIRAAN_JUMLAH_USAHA_INFO_DARI_PAK_RT'),
                            jumlah_bangunan_tempat_tinggal=row.get('JUMLAH_BANGUNAN_TEMPAT_TINGGAL_(BTT)'),
                            jumlah_bangunan_tempat_tinggal_kosong=row.get('JUMLAH_BANGUNAN_TEMPAT_TINGGAL_KOSONG_(BTT_KOSONG)'),
                            jumlah_bangunan_khusus_usaha=row.get('JUMLAH_BANGUNAN_KHUSUS_USAHA_(BKU)'),
                            jumlah_bangunan_bukan_tempat_tinggal=row.get('JUMLAH_BANGUNAN_BUKAN_TEMPAT_TINGGAL_(BBTT_NON_USAHA)'),
                            perkiraan_jumlah_muatan_usaha=row.get('PERKIRAAN_JUMLAH_MUATAN_USAHA'),
                            total_muatan=row.get('TOTAL_MUATAN_(MAKS_BTT,KK_+_BTT_+BTTK_+_BBTT_NON_USAHA)'),
                            apakah_ada_perubahan_batas=row.get('APAKAH_ADA_PERUBAHAN_BATAS_PADA_SLS_TERSEBUT?')
                        )

                        # print(new_dashboard_data)
                        db.session.add(new_dashboard_data)

                db.session.commit()
                flash('File berhasil di-upload dan data telah diproses!', 'success')
                return redirect(url_for('upload_file'))

            except Exception as e:
                # Jika terjadi error saat memproses file (misal, nama kolom salah)
                flash(f'Terjadi error saat memproses file: {e}', 'error')
                return redirect(request.url)
        else:
            flash('Tipe file tidak diizinkan!', 'error')
            return redirect(request.url)

    # Jika metodenya GET, tampilkan halaman upload
    return render_template('upload.html')

if __name__ == '__main__':
    app.run()