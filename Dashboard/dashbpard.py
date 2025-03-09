import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
all_data = pd.read_csv("all_data.csv")

all_data["dteday"] = pd.to_datetime(all_data["dteday"])

# Mapping label musim
season_map = {1: "Musim Semi", 2: "Musim Panas", 3: "Musim Gugur", 4: "Musim Dingin"}
all_data["season_label"] = all_data["season_x"].map(season_map)

# Mapping label kondisi cuaca
weathersit_map = {1: "Cerah", 2: "Berkabut", 3: "Hujan Ringan", 4: "Hujan Lebat"}
all_data["weathersit_label"] = all_data["weathersit_x"].map(weathersit_map)

# Sidebar untuk filter
st.sidebar.title("🎚 Filter Data")
selected_season = st.sidebar.selectbox("Pilih Musim", all_data["season_label"].unique())
selected_weathersit = st.sidebar.multiselect("Pilih Kondisi Cuaca", all_data["weathersit_label"].unique(), all_data["weathersit_label"].unique())

# Filter data berdasarkan pilihan user
filtered_data = all_data[(all_data["season_label"] == selected_season) & (all_data["weathersit_label"].isin(selected_weathersit))]

# Judul Dashboard
st.title("🚴‍♂️ Dashboard Analisis Peminjaman Sepeda")
st.write("Dashboard interaktif untuk memahami pola peminjaman sepeda berdasarkan musim dan kondisi cuaca.")

# 📌 Visualisasi 1: Tren Peminjaman Sepeda Berdasarkan Musim (GANTI KE BAR CHART)
st.subheader("📊 Tren Peminjaman Sepeda Berdasarkan Musim")

season_counts = all_data.groupby("season_label")["cnt_x"].sum().reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="season_label", y="cnt_x", data=season_counts, ax=ax, palette="coolwarm")
ax.set_xlabel("Musim")
ax.set_ylabel("Total Peminjaman Sepeda")
ax.set_title("Total Peminjaman Sepeda Berdasarkan Musim")
st.pyplot(fig)

# 📌 Visualisasi 2: Pengaruh Cuaca terhadap Peminjaman Sepeda (GANTI KE HORIZONTAL BAR CHART)
st.subheader("☁️ Pengaruh Cuaca terhadap Peminjaman Sepeda")
weathersit_counts = all_data.groupby("weathersit_label")["cnt_x"].sum().reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(y="weathersit_label", x="cnt_x", data=weathersit_counts, ax=ax, palette="viridis")
ax.set_ylabel("Kondisi Cuaca")
ax.set_xlabel("Total Peminjaman Sepeda")
ax.set_title("Total Peminjaman Sepeda Berdasarkan Kondisi Cuaca")
st.pyplot(fig)

# 📌 Visualisasi 3: Peminjaman Sepeda Per Bulan
st.subheader("📅 Jumlah Peminjaman Sepeda Per Bulan")
filtered_data["month"] = filtered_data["dteday"].dt.month
monthly_data = filtered_data.groupby("month")["cnt_x"].sum().reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x="month", y="cnt_x", data=monthly_data, ax=ax, palette="Greens_d")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Peminjaman Sepeda")
ax.set_title("Total Peminjaman Sepeda Per Bulan")
st.pyplot(fig)

# Insight
st.write("""
**🔍 Insight:**
- Peminjaman sepeda meningkat di musim panas dan menurun drastis di musim dingin.
- Cuaca cerah mendominasi peminjaman sepeda, sementara hujan lebat memiliki jumlah peminjaman yang rendah.
- Tren bulanan menunjukkan pola musiman yang dapat dimanfaatkan untuk strategi bisnis dan operasional.
""")
