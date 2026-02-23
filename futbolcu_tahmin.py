import streamlit as st
from PIL import Image, ImageFilter
import random
import os

st.title("⚽ Futbolcu Tahmin Oyunu - İpuçlu Versiyon (Local Resimler)")

# Futbolcu listesi ve verileri (resim dosyası artık local)
players = {
    "lionel messi": {
        "file": "images/messi.jpg",
        "team": "Inter Miami",
        "nationality": "Arjantin",
        "position": "Forvet"
    },
    "cristiano ronaldo": {
        "file": "images/ronaldo.jpg",
        "team": "Al Nassr",
        "nationality": "Portekiz",
        "position": "Forvet"
    },
    "neymar": {
        "file": "images/neymar.jpg",
        "team": "Al-Hilal",
        "nationality": "Brezilya",
        "position": "Forvet"
    },
    "kylian mbappé": {
        "file": "images/mbappe.jpg",
        "team": "Paris Saint-Germain",
        "nationality": "Fransa",
        "position": "Forvet"
    },
    "erling haaland": {
        "file": "images/haaland.jpg",
        "team": "Manchester City",
        "nationality": "Norveç",
        "position": "Forvet"
    }
}

# Session state ile oyun durumu
if "player_name" not in st.session_state or st.button("Yeni Oyun"):
    st.session_state.player_name = random.choice(list(players.keys()))
    st.session_state.attempts = 0
    st.session_state.max_attempts = 5
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.revealed_hints = 0  # Gösterilen ipucu sayısı

# Bulanıklık seviyeleri
blur_values = [15, 12, 9, 6, 3, 0]
current_blur = blur_values[st.session_state.attempts]

# Resim yolu
image_path = players[st.session_state.player_name]["file"]

# Resim kontrolü
if not os.path.exists(image_path):
    st.error(f"Resim bulunamadı: {image_path}")
else:
    image = Image.open(image_path)
    blurred_image = image.filter(ImageFilter.GaussianBlur(current_blur))
    st.image(
        blurred_image,
        caption=f"Tahmin et: Futbolcu kim? ({st.session_state.max_attempts - st.session_state.attempts} hakkınız kaldı)"
    )

    # İpuçları listesi
    hints_list = [
        f"Milliyeti: {players[st.session_state.player_name]['nationality']}",
        f"Takımı: {players[st.session_state.player_name]['team']}",
        f"Pozisyonu: {players[st.session_state.player_name]['position']}"
    ]

    # Başlangıçta sadece 1 ipucu göster
    if st.session_state.revealed_hints == 0:
        st.info(f"İpucu: {hints_list[0]}")

    # Tahmin input
    if not st.session_state.game_over:
        guess = st.text_input("Futbolcu ismini yazın:").lower()
        if st.button("Tahmini Gönder"):
            if guess == "":
                st.warning("Tahmin boş bırakılamaz!")
            elif guess == st.session_state.player_name.lower():
                st.success("🎉 Doğru! Tebrikler!")
                st.session_state.score = (st.session_state.max_attempts - st.session_state.attempts) * 20
                st.session_state.game_over = True
                st.write(f"Skorunuz: {st.session_state.score} puan")
            else:
                # Yanlış tahmin
                st.session_state.attempts += 1
                # Yeni ipucu göster
                if st.session_state.revealed_hints < len(hints_list)-1:
                    st.session_state.revealed_hints += 1
                    st.info(f"Yeni ipucu: {hints_list[st.session_state.revealed_hints]}")
                if st.session_state.attempts >= st.session_state.max_attempts:
                    st.error(f"😢 Hakkınız bitti. Doğru cevap: {st.session_state.player_name.title()}")
                    st.session_state.score = 0
                    st.session_state.game_over = True
                else:
                    st.warning("Yanlış tahmin! Bulanıklık biraz azaldı, tekrar deneyin.")
