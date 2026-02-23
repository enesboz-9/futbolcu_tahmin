import streamlit as st
from PIL import Image, ImageFilter
import requests
from io import BytesIO
import random

st.title("⚽ Futbolcu Tahmin Oyunu - İpuçlu Versiyon")

# Futbolcu listesi ve verileri
players = {
    "lionel messi": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/89/Lionel_Messi_20180626.jpg",
        "team": "Inter Miami",
        "nationality": "Arjantin",
        "position": "Forvet"
    },
    "cristiano ronaldo": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg",
        "team": "Al Nassr",
        "nationality": "Portekiz",
        "position": "Forvet"
    },
    "neymar": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/3/34/Neymar_2018.jpg",
        "team": "Al-Hilal",
        "nationality": "Brezilya",
        "position": "Forvet"
    },
    "kylian mbappé": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/6/6c/Kylian_Mbapp%C3%A9_2019.jpg",
        "team": "Paris Saint-Germain",
        "nationality": "Fransa",
        "position": "Forvet"
    },
    "erling haaland": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/f/f2/Erling_Haaland_2019.jpg",
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

# Resmi yükle
image_url = players[st.session_state.player_name]["url"]
response = requests.get(image_url)
image = Image.open(BytesIO(response.content))
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