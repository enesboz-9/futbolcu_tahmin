import streamlit as st
from PIL import Image, ImageFilter
import random
import os

# Sayfa Ayarları
st.set_page_config(page_title="⚽ Futbolcu Tahmin Oyunu", layout="centered")

# ----- Futbolcu Verileri -----
players = {
    "Lionel Messi": {"file": "images/messi.jpg", "team": "Inter Miami", "nationality": "Arjantin", "position": "Forvet", "age": 36},
    "Cristiano Ronaldo": {"file": "images/ronaldo.jpg", "team": "Al Nassr", "nationality": "Portekiz", "position": "Forvet", "age": 38},
    "Neymar": {"file": "images/neymar.jpg", "team": "Al-Hilal", "nationality": "Brezilya", "position": "Forvet", "age": 31},
    "Kylian Mbappe": {"file": "images/mbappe.jpg", "team": "Real Madrid", "nationality": "Fransa", "position": "Forvet", "age": 25},
    "Erling Haaland": {"file": "images/haaland.jpg", "team": "Manchester City", "nationality": "Norveç", "position": "Forvet", "age": 23}
}

# ----- Session State Başlat -----
if "target_player" not in st.session_state:
    st.session_state.target_player = random.choice(list(players.keys()))
    st.session_state.attempts = 0
    st.session_state.max_attempts = 5
    st.session_state.total_score = 0
    st.session_state.game_over = False
    st.session_state.hints_shown = []

def reset_game(next_player=True):
    if next_player:
        st.session_state.target_player = random.choice(list(players.keys()))
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.hints_shown = []
    st.rerun()

# ----- Arayüz -----
st.title("⚽ Futbolcuyu Tanıyabilecek misin?")
st.divider()

# Sidebar Puan Durumu
st.sidebar.header("📊 İstatistikler")
st.sidebar.metric("Toplam Puan", st.session_state.total_score)
if st.sidebar.button("Oyunu Sıfırla"):
    st.session_state.total_score = 0
    reset_game()

# Oyun Ekranı
col1, col2 = st.columns([1, 1])

# Bulanıklık Hesaplama
blur_levels = [25, 18, 12, 6, 2, 0]
current_blur = blur_levels[min(st.session_state.attempts, len(blur_levels)-1)]

player_data = players[st.session_state.target_player]

with col1:
    # Resim İşleme
    if os.path.exists(player_data["file"]):
        img = Image.open(player_data["file"])
        blurred_img = img.filter(ImageFilter.GaussianBlur(current_blur))
        st.image(blurred_img, use_container_width=True, caption="Kim bu futbolcu?")
    else:
        st.error(f"Resim bulunamadı: {player_data['file']}")

with col2:
    st.subheader("İpuçları")
    
    # Mevcut ipuçlarını oluştur
    all_hints = [
        f"🌍 Uyruk: {player_data['nationality']}",
        f"🏃 Pozisyon: {player_data['position']}",
        f"🎂 Yaş: {player_data['age']}",
        f"🏢 Takım: {player_data['team']}"
    ]
    
    # Her yanlışta bir ipucu göster
    for i in range(st.session_state.attempts):
        if i < len(all_hints):
            st.info(all_hints[i])
        elif i == len(all_hints):
            st.warning("Son Şans! Resim neredeyse netleşti.")

# ----- Tahmin Formu -----
if not st.session_state.game_over:
    with st.form(key="guess_form", clear_on_submit=True):
        user_guess = st.text_input("Tahmininizi buraya yazın:").strip().lower()
        submit_button = st.form_submit_button("Tahmin Et")

    if submit_button:
        if user_guess == "":
            st.warning("Lütfen bir isim girin.")
        else:
            correct_name = st.session_state.target_player.lower()
            
            # Basit kontrol: İsim veya soyisim içeriyor mu?
            if user_guess in correct_name and len(user_guess) > 3:
                gain = (st.session_state.max_attempts - st.session_state.attempts) * 20
                st.session_state.total_score += gain
                st.balloons()
                st.success(f"✅ TEBRİKLER! Doğru cevap: {st.session_state.target_player}. {gain} puan kazandınız!")
                st.session_state.game_over = True
                st.button("Sonraki Futbolcu", on_click=reset_game)
            else:
                st.session_state.attempts += 1
                if st.session_state.attempts >= st.session_state.max_attempts:
                    st.error(f"❌ Haklarınız bitti! Doğru cevap: {st.session_state.target_player}")
                    st.session_state.game_over = True
                    st.button("Yeniden Dene", on_click=reset_game)
                else:
                    st.rerun() # Bulanıklığı ve ipucunu güncellemek için
else:
    if st.session_state.attempts >= st.session_state.max_attempts:
        st.button("Yeni Oyun", on_click=reset_game)
