import streamlit as st
from PIL import Image
import io
import zipfile
import random

st.title("🖼️ Image Converter")
st.markdown("Pilih jenis konversi yang kamu butuhkan:")

# Pilihan mode konversi
mode = st.radio(
    "📌 Pilih Mode Konversi:",
    options=["224px Converter", "Hanya Rename + JPG Convert"]
)

# Inisialisasi uploader
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = "uploader_" + str(random.randint(1, 10000))

if st.button("🔄 Reset Semua Gambar"):
    st.session_state.uploader_key = "uploader_" + str(random.randint(1, 10000))

# Input prefix
prefix = st.text_input("📛 Prefix nama file hasil:", value="gambar")

# Upload gambar
uploaded_files = st.file_uploader(
    "Upload gambar", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True, 
    help="Maksimal 20 file",
    key=st.session_state.uploader_key
)

# Proses jika ada file
if uploaded_files:
    if len(uploaded_files) > 20:
        st.warning("Maksimal hanya bisa upload 20 gambar.")
    else:
        processed_images = []
        st.subheader("📄 Hasil:")

        cols = st.columns(4)

        for i, file in enumerate(uploaded_files):
            image = Image.open(file).convert("RGB")

            # Resize jika mode 224px
            if mode == "224px Converter":
                image = image.resize((224, 224))

            # Simpan ke buffer sebagai JPEG
            buf = io.BytesIO()
            image.save(buf, format="JPEG")
            buf.seek(0)

            with cols[i % 4]:
                st.image(image, use_container_width=True)

                default_name = f"{prefix}_{i+1}.jpg"
                custom_name = st.text_input(
                    label="Nama file:",
                    value=default_name,
                    key=f"name_input_{i}"
                )

                if not custom_name.lower().endswith(".jpg"):
                    custom_name += ".jpg"

                processed_images.append((custom_name, buf))

                st.download_button(
                    label="Download",
                    data=buf,
                    file_name=custom_name,
                    mime="image/jpeg",
                    key=f"download_{i}"
                )

        st.subheader("📦 Download Semua Sekaligus:")
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for name, buffer in processed_images:
                zip_file.writestr(name, buffer.getvalue())
        zip_buffer.seek(0)

        st.download_button(
            label="Download Semua (ZIP)",
            data=zip_buffer,
            file_name=f"{prefix}_converted_images.zip",
            mime="application/zip"
        )
