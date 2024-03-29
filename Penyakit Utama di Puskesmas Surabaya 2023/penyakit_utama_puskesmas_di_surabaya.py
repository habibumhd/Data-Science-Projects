# -*- coding: utf-8 -*-
"""Penyakit Utama Puskesmas di Surabaya

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lN7o3dM50QLJlu-yhkpJrxucC-9gPg-a

# Penyakit Utama Puskesmas di Surabaya

Dataset diperoleh dari:

https://opendata.surabaya.go.id/dataset/banyaknya-penyakit-utama-yang-ditemukan-di-puskesmas-menurut-jenis-penyakit-tahun-2023

# Eksplorasi Data Awal

**Memahami Struktur Data**
1. Mengidentifikasi jumlah baris dan kolom dalam dataset.
2. Memeriksa tipe data masing-masing kolom.

**Penanganan Nilai Hilang dan Duplikat**
1. Mengidentifikasi apakah ada nilai yang hilang atau duplikat dalam dataset.
2. Menentukan strategi untuk menangani nilai yang hilang atau duplikat.
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.colab import drive

drive.mount('/content/drive')
path = '/content/drive/MyDrive/Dataset Repository/Data Penyakit Surabaya 2023.csv'

df = pd.read_csv(path, sep=';')
df.head()

# Jumlah baris dan kolom dalam dataset
print("Jumlah Baris dan Kolom:", df.shape)

# Tipe data masing-masing kolom
print("\nTipe Data:\n", df.dtypes)

# Statistik deskriptif untuk kolom-kolom numerik
print("\nStatistik Deskriptif:\n", df.describe())

# Identifikasi nilai yang hilang atau duplikat
print("\nJumlah Nilai Hilang:\n", df.isnull().sum())
print("\nJumlah Duplikat:\n", df.duplicated().sum())

"""# Data Visualization

1. Distribusi Jumlah Kasus Penyakit per Wilayah
2. Radar Chart untuk Menampilkan Perbandingan Jumlah Kasus antara Bulan
"""

# Distribusi Jumlah Kasus Penyakit per Wilayah

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df['Total Kasus'] = df.iloc[:, 4:].sum(axis=1)

plt.figure(figsize=(12, 6))
sns.barplot(x='Wilayah', y='Total Kasus', data=df, palette='viridis')
plt.title('Distribusi Jumlah Kasus Penyakit per Wilayah')
plt.xlabel('Wilayah')
plt.ylabel('Jumlah Kasus')
plt.xticks(rotation=45, ha='right')
plt.show()

# Radar Chart untuk Menampilkan Perbandingan Jumlah Kasus antara Bulan

from math import pi
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df.iloc[:, 4:16])

categories = df.columns[4:16]
angles = [n / float(len(categories)) * 2 * pi for n in range(len(categories))]
angles += angles[:1]

plt.figure(figsize=(8, 8))
for i in range(len(df['Wilayah'].unique())):
    values = scaled_data[i]
    values = np.append(values, values[:1])
    plt.polar(angles, values, label=df['Wilayah'].unique()[i], linewidth=2)
plt.title('Radar Chart Perbandingan Jumlah Kasus antara Bulan')
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
plt.xticks(angles[:-1], categories)
plt.show()

"""# Prediksi Jumlah Kasus di Masa Depan

1. Model regresi linier digunakan untuk memprediksi jumlah kasus berdasarkan 'Wilayah' dan 'Jenis Penyakit'.
2. Visualisasi scatter plot membantu melihat sejauh mana prediksi model mendekati nilai aktual.
3. *Mean Squared Error* (MSE) memberikan metrik kuantitatif tentang seberapa baik model bekerja, di mana nilai MSE yang lebih rendah menunjukkan kinerja yang lebih baik.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, LabelEncoder

df['Jumlah Bulan'] = df.iloc[:, 5:16].sum(axis=1)

# Memisahkan fitur dan target
X = df[['Wilayah', 'Jenis Penyakit', 'Jumlah Bulan']].copy()
y = df['Total Kasus']

# Label encode kolom 'Wilayah' dan 'Jenis Penyakit'
le = LabelEncoder()
X['Wilayah'] = le.fit_transform(X['Wilayah'])
X['Jenis Penyakit'] = le.fit_transform(X['Jenis Penyakit'])

# Normalisasi data menggunakan Min-Max Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Memisahkan data menjadi training dan testing set
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Membuat model regresi linier
model = LinearRegression()
model.fit(X_train, y_train)

# Melakukan prediksi pada data testing
y_pred = model.predict(X_test)

# Evaluasi model dengan Mean Squared Error
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

plt.figure(figsize=(10, 6))
plt.scatter(X_test[:, 0], y_test, color='blue', label='Actual')
plt.scatter(X_test[:, 0], y_pred, color='red', label='Predicted')
plt.title('Prediksi Jumlah Kasus (Wilayah)')
plt.xlabel('Wilayah (Scaled)')
plt.ylabel('Jumlah Kasus')
plt.legend()
plt.show()