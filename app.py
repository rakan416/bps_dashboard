from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from supabase import create_client
from dotenv import load_dotenv
import pandas as pd
import os
import numpy as np

# Load .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

# Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Allowed extensions
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Test koneksi ke Supabase
    try:
        result = supabase.table("data_dashboard").select("id_data").limit(1).execute()
        return redirect(url_for('upload_file'))
    except Exception as e:
        return f'<h1>Koneksi ke Supabase gagal.</h1><p>Error: {e}</p>'

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file_alokasi = request.files['alokasi']
        file_landmark = request.files['landmark']
        file_rekap_lkm = request.files['rekap_lkm']

        if file_landmark.filename == '':
            flash('Tidak ada file yang dipilih!', 'error')
            return redirect(request.url)

        if file_alokasi and allowed_file(file_alokasi.filename):
            # Proses file Alokasi
            df_alokasi = pd.read_excel(file_alokasi, sheet_name=None, dtype=str)
            KEC = df_alokasi['3519']['kdkec'].unique()
            df_main = df_alokasi['3519'].drop(columns=['PEMETA', 'PENGAWAS', 'PENGOLAH']).copy()
            all_kec = []
            for k in KEC:
                all_kec.append(df_alokasi[k][['id', 'PEMETA', 'EMAIL PEMETA', 'PENGAWAS', 'EMAIL PENGAWAS']])
            df_all_kec = pd.concat(all_kec, ignore_index=True)
            df_main = df_main.merge(df_all_kec, how='left', on='id')
            del df_all_kec, df_alokasi
            df_main['idsls'] = df_main['idsubsls'].str.slice(0, 14)
            df_main.rename(columns={'id':'id_alokasi'}, inplace=True)

            # Proses file Landmark
            df_landmark = pd.read_excel(file_landmark, dtype=str)
            df_landmark['idsls'] = df_landmark['iddesa'] + df_landmark['nm_project']
            df_landmark['latlon'] = df_landmark['latitude'] + ',' + df_landmark['longitude']
            df_landmark.rename(columns={'id':'id_landmark'}, inplace=True)
            df_landmark.drop(columns=['latitude', 'longitude'], inplace=True)
            df_main = df_landmark.merge(df_main, how='outer', on='idsls')
            del df_landmark

            # Proses file LKM
            df_LKM = pd.read_excel(file_rekap_lkm, sheet_name='Form Responses 1', dtype=str)
            df_LKM['KODE SLS'] = df_LKM['KODE KECAMATAN'] + df_LKM['KODE DESA'] + df_LKM['KODE SLS/NON SLS']
            df_LKM['idsls'] = '3519' + df_LKM['KODE SLS']
            df_main = df_main.merge(df_LKM, on='idsls', how='outer')
            del df_LKM

            # Bersihkan nama kolom
            df_main.columns = [c.replace(' ', '_') for c in df_main.columns]
            df_main.reset_index(drop=True, inplace=True)
            df_main = df_main.replace({np.nan: None, np.inf: None, -np.inf: None})
            df_main.reset_index(inplace=True)
            df_main.rename(columns={'index':'id'})

            try:
                # Hapus semua data lama
                supabase.table("data_dashboard").delete().execute()
                print('Deletion Berhasil')

                # Insert batch ke Supabase
                data_to_insert = df_main.to_dict(orient='records')
                batch_size = 500

                for i in range(0, len(data_to_insert), batch_size):
                    supabase.table("data_dashboard").insert(data_to_insert[i:i+batch_size]).execute()

                flash(f'Berhasil mengunggah {len(df_main)} data ke Supabase!', 'success')
                return redirect(url_for('upload_file'))

            except Exception as e:
                flash(f'Terjadi error saat memproses file: {e}', 'error')
                print(e)
                return redirect(request.url)
        else:
            flash('Tipe file tidak diizinkan!', 'error')
            return redirect(request.url)

    return render_template('upload.html')

@app.route('/laporan')
def laporan():
    return render_template('laporan.html')

if __name__ == '__main__':
    app.run()
