import streamlit as st
from PIL import Image, ImageFilter
import random
import os

st.set_page_config(page_title="⚽ Futbolcu Tahmin Oyunu", layout="wide")

# ----- Futbolcu Verileri -----
players = {
    "lionel messi": {
        "file": "images/messi.jpg",
        "team": "Inter Miami",
        "nationality": "Arjantin",
        "position": "Forvet",
        "age": 36,
        "birth_year": 1987
    },
    "cristiano ronaldo": {
        "file": "images/ronaldo.jpg",
        "team": "Al Nassr",
        "nationality": "Portekiz",
        "position": "Forvet",
        "age": 38,
        "birth_year": 1985
    },
    "neymar": {
        "file": "images/neymar.jpg",
        "team": "Al-Hilal",
        "nationality": "Brezilya",
        "position": "Forvet",
        "age": 31,
        "birth_year": 1992
    },
    "kylian mbappé": {
        "file": "images/mbappe.jpg",
        "team": "Paris Saint-Germain",
        "nationality": "Fransa",
        "position": "Forvet",
        "age": 24,
        "birth_year": 1998
    },
    "erling haaland": {
        "file": "images/haaland.jpg",
        "team": "Manchester City",
        "nationality": "Norveç",
        "position": "Forvet",
        "age": 23,
        "birth_year": 2000
    }
}

# ----- Session State Başlat -----
if "player_name" not in st.session_state:
    st.session_state.player_name = random.choice(list(players.keys()))
    st.session_state.attempts = 0
    st.session_state.max_attempts = 5
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.revealed_hints = []
    st.session_state.guess = ""

# ----- Sağ Üstte Toplam Puan -----
st.sidebar.header("🏆 Toplam Puan")
st.sidebar.write(st.session_state.score)

# ----- Oyun Bitti Kontrol -----
if st.session_state.game_over:
    st.success("Oyun Bitti! 🎮")
    st.write(f"Doğru cevabı: **{st.session_state.player_name.title()}**")
    st.write(f"Toplam puanınız: **{st.session_state.score}**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Yeniden Oyna"):
            st.session_state.player_name = random.choice(list(players.keys()))
            st.session_state.attempts = 0
            st.session_state.score = 0
            st.session_state.game_over = False
            st.session_state.revealed_hints = []
            st.experimental_rerun()
    with col2:
        if st.button("❌ Çıkış"):
            st.stop()

# ----- Bulanıklık Ayarı -----
blur_values = [15, 12, 9, 6, 3, 0]
current_blur = blur_values[min(st.session_state.attempts, len(blur_values)-1)]

# ----- Resim Yükle ve Göster -----
image_path = players[st.session_state.player_name]["file"]
if not os.path.exists(image_path):
    st.error(f"Resim bulunamadı: {image_path}")
else:
    image = Image.open(image_path)
    blurred_image = image.filter(ImageFilter.GaussianBlur(current_blur))
    st.image(
        blurred_image,
        caption=f"Tahmin et: Futbolcu kim? ({st.session_state.max_attempts - st.session_state.attempts} hakkınız kaldı)"
    )

# ----- İpuçları -----
all_hints = [
    f"Milliyeti: {players[st.session_state.player_name]['nationality']}",
    f"Takımı: {players[st.session_state.player_name]['team']}",
    f"Pozisyonu: {players[st.session_state.player_name]['position']}",
    f"Yaşı: {players[st.session_state.player_name]['age']}",
    f"Doğum Yılı: {players[st.session_state.player_name]['birth_year']}"
]

# İpuçlarını alt alta göster
for i in st.session_state.revealed_hints:
    st.info(all_hints[i])

# ----- Tahmin Input -----
guess = st.text_input("Futbolcunun adını veya soyadını yazabilirsiniz:", key="guess")
if st.button("Tahmini Gönder"):
    guess_text = st.session_state.guess.strip().lower()
    if guess_text == "":
        st.warning("Tahmin boş bırakılamaz!")
    else:
        # Ad, soyad veya tamamı doğruysa kabul
        player_full_name = st.session_state.player_name.lower()
        first_name, last_name = player_full_name.split(" ")[0], player_full_name.split(" ")[-1]
        if guess_text == first_name or guess_text == last_name or guess_text == player_full_name:
            st.success("🎉 Doğru! Tebrikler!")
            st.session_state.score += (st.session_state.max_attempts - st.session_state.attempts) * 20
            # Yeni futbolcuya otomatik geç
            st.session_state.player_name = random.choice(list(players.keys()))
            st.session_state.attempts = 0
            st.session_state.revealed_hints = []
            st.session_state.guess = ""
            st.experimental_rerun()
        else:
            st.session_state.attempts += 1
            # Yeni ipucu ekle
            if len(st.session_state.revealed_hints) < len(all_hints):
                st.session_state.revealed_hints.append(len(st.session_state.revealed_hints))
            # Hakkı dolduysa oyun biter
            if st.session_state.attempts >= st.session_state.max_attempts:
                st.error(f"😢 Hakkınız bitti. Doğru cevap: {st.session_state.player_name.title()}")
                st.session_state.score += 0
                st.session_state.game_over = True
            else:
                st.warning("Yanlış tahmin! Bulanıklık biraz azaldı, tekrar deneyin.")
            # Inputu temizle
            st.session_state.guess = ""
            st.experimental_rerun()
