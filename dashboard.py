import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import warnings

warnings.filterwarnings("ignore")

# 1. Sayfa Ayarları
st.set_page_config(page_title="Finansal Gösterge Paneli", page_icon="💸", layout="wide")
st.title("💸 Kişisel Finans ve Harcama Tahmin Paneli")
st.markdown("Veri Tabanı (SQLite) ➔ API (FastAPI) ➔ Analiz (Pandas) ➔ **Arayüz (Streamlit)**")
st.markdown("---")


# 2. Veri Çekme Fonksiyonu
@st.cache_data
def veri_getir():
    conn = sqlite3.connect('finance.db')
    sorgu = """
    SELECT t.date, t.amount, t.description, c.name as category, c.type 
    FROM transactions t
    JOIN categories c ON t.category_id = c.id
    """
    df = pd.read_sql_query(sorgu, conn)
    conn.close()
    return df


df = veri_getir()

if df.empty:
    st.warning("Henüz veri tabanında gösterilecek işlem yok. Önce API üzerinden veri ekleyin.")
else:
    # --- BÖLÜM 1: ÖZET METRİKLER (KPI) ---
    gelir_toplam = df[df['type'] == 'gelir']['amount'].sum()
    gider_toplam = df[df['type'] == 'gider']['amount'].sum()
    bakiye = gelir_toplam - gider_toplam

    col1, col2, col3 = st.columns(3)
    col1.metric("🟢 Toplam Gelir", f"{gelir_toplam:,.2f} ₺")
    col2.metric("🔴 Toplam Gider", f"{gider_toplam:,.2f} ₺")
    col3.metric("🔵 Net Bakiye", f"{bakiye:,.2f} ₺", delta="Pozitif" if bakiye > 0 else "Negatif")

    st.markdown("---")

    # --- BÖLÜM 2: GÖRSELLEŞTİRME VE ANALİZ ---
    col_grafik1, col_grafik2 = st.columns(2)

    with col_grafik1:
        st.subheader("Kategoriye Göre Gider Dağılımı")
        giderler = df[df['type'] == 'gider']
        kategori_ozet = giderler.groupby('category')['amount'].sum().reset_index()

        fig_pie = px.pie(kategori_ozet, values='amount', names='category', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_grafik2:
        st.subheader("Harcama Trendi (Ekonometrik Tahmin)")

        giderler['date'] = pd.to_datetime(giderler['date'])
        gunluk_gider = giderler.groupby('date')['amount'].sum().reset_index()
        gunluk_gider.set_index('date', inplace=True)
        haftalik_gider = gunluk_gider.resample('W').sum()

        haftalik_gider['Trend Tahmini'] = haftalik_gider['amount'].ewm(alpha=0.5, adjust=False).mean()
        haftalik_gider.reset_index(inplace=True)
        haftalik_gider.rename(columns={'amount': 'Gerçekleşen'}, inplace=True)

        fig_line = px.line(haftalik_gider, x='date', y=['Gerçekleşen', 'Trend Tahmini'],
                           labels={'value': 'Tutar (₺)', 'date': 'Tarih', 'variable': 'Gösterge'},
                           color_discrete_map={'Gerçekleşen': '#ef553b', 'Trend Tahmini': '#00cc96'})
        st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")

    # --- BÖLÜM 3: VERİ TABLOSU ---
    st.subheader("📋 Son İşlem Dökümü")
    st.dataframe(df.sort_values(by="date", ascending=False).style.format({"amount": "{:.2f} ₺"}),
                 use_container_width=True)