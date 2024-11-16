import streamlit as st
import joblib
import pandas as pd

# Load the PyCaret model
stress_model = joblib.load('base_model_nurse_stress_15min.pkl')

# Load recommendations from the uploaded file
file_path = 'rekomendasi.xlsx'
recommendations_df = pd.read_excel(file_path)

# Set up the main title and subtitle
st.title("NurstressAI")
st.subheader("Aplikasi Web Prediksi dan Penanganan Stres Perawat Berdasarkan Aspek Fisiologis dan Tipe Kepribadian Myers-Briggs (MBTI)")
st.markdown("Prediksi tingkat stres untuk perawat berdasarkan input **EDA**, **HR**, dan **TEMP**, serta dapatkan rekomendasi berdasarkan tipe kepribadian!")

# Main input section
st.markdown("#### 🩺 Masukkan Parameter Input")
st.write("Isi nilai untuk **EDA**, **HR**, **TEMP**, dan pilih **Tipe Kepribadian** untuk memprediksi tingkat stres.")

# Create three columns for numerical inputs
col1, col2, col3 = st.columns(3)

with col1:
    eda = st.number_input("🖐️ EDA (Aktivitas Elektrodermal)", min_value=0.0, max_value=100.0, value=5.0)

with col2:
    hr = st.number_input("❤️ HR (Denyut Jantung)", min_value=0, max_value=200, value=60)

with col3:
    temp = st.number_input("🌡️ TEMP (Temperatur)", min_value=30.0, max_value=45.0, value=36.5)

# Dropdown input for personality type
personality_types = recommendations_df['Tipe'].unique().tolist()
personality = st.selectbox("🧠 Pilih Tipe Kepribadian", options=personality_types)

# Create a "Predict" button
if st.button("🚑 Prediksi"):
    # Create feature array for prediction
    features = pd.DataFrame([[eda, hr, temp]], columns=['EDA', 'HR', 'TEMP'])

    # Predict stress level
    stress_prediction = stress_model.predict(features)[0]

    # Map prediction to stress level category
    stress_level_map = {0: "Tidak Stres", 1: "Stres Rendah", 2: "Stres Tinggi"}
    stress_level = stress_level_map.get(stress_prediction, "Tidak Diketahui")

    # Find recommendations for the selected personality type
    recommendations = recommendations_df.loc[recommendations_df['Tipe'] == personality, 'Rekomendasi'].tolist()

    # Display the prediction
    st.markdown("### 🧾 Hasil Prediksi")
    st.write(f"Tingkat Stres yang Diprediksi: **{stress_level}**")

    # Display the recommendations as bullet points
    st.markdown("### 🌟 Rekomendasi Manajemen Stres")
    if recommendations:
        st.write(f"Berdasarkan tipe kepribadian **{personality}**, disarankan:")
        for rec in recommendations:
            st.markdown(f"- {rec}")
    else:
        st.write("Tidak ada rekomendasi yang tersedia untuk tipe kepribadian ini.")

    st.markdown("<div style='margin-bottom: 100px;'></div>", unsafe_allow_html=True)

