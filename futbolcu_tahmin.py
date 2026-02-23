import streamlit as st
from PIL import Image, ImageFilter
import random
import os
import time

# Sayfa Ayarları
st.set_page_config(page_title="⚽ Futbolcu Tahmin Oyunu", layout="centered")

# ----- Futbolcu Verileri (Resim yollarının doğruluğundan emin olun) -----
players_data = {
    "Lionel Messi": {"file": "images/messi.jpg", "team": "Inter Miami", "nationality": "Arjantin", "position": "Forvet", "age": 36},
    "Cristiano Ronaldo": {"file": "images/ronaldo.jpg", "team": "Al Nassr", "nationality": "Portekiz", "position": "Forvet", "age": 38},
    "Neymar": {"file": "images/neymar.jpg", "team": "Al-Hilal", "nationality": "Brezilya", "position": "Forvet", "age": 31},
    "Kylian Mbappe": {"file": "images/mbappe.jpg", "team": "Real Madrid", "nationality": "Fransa", "position": "Forvet", "age": 25},
    "Erling Haaland": {"file": "images/haaland.jpg", "team": "Manchester City", "nationality": "Norveç", "position": "Forvet", "age": 23},
    "Harry Kane": {"file": "images/kane.jpg", "team": "Bayern Münih", "nationality": "İngiltere", "position": "Forvet", "age": 30},
    "Kevin De Bruyne": {"file": "images/debruyne.jpg", "team": "Manchester City", "nationality": "Belçika", "position": "Orta Saha", "age": 32}
}

# ----- Session State Yönetimi -----
if "played_players" not in st.session_state:
    st.session_state.played_players = []
    st.session_state.current_question = 1
    st.session_state.max_questions = 5
    st.session_state.target_player = None
    st.session_state.attempts = 0
    st.session_state.total_score = 0
    st.session_state.game_finished = False

def pick_new_player():
    remaining_players = [p for p in players_data.keys() if p not in st.session_state.played_players]
    if remaining_players and st.session_state.current_question <= st.session_state.max_questions:
        new_player = random.choice(remaining_players)
        st.session_state.target_player = new_player
        st.session_state.played_players.append(new_player)
        st.session_state.attempts = 0
    else:
        st.session_state.game_finished = True

def reset_game():
    st.session_state.played_players = []
    st.session_state.current_question = 1
    st.session_state.target_player = None
    st.session_state.total_score = 0
    st.session_state.game_finished = False
    st.rerun()

# Oyun başında ilk futbolcuyu seç
if st.session_state.target_player is None and not st.session_state.game_finished:
    pick_new_player()

# ----- OYUN BİTİŞ EKRANI -----
if st.session_state.game_finished:
    st.balloons()
    st.header("🏆 Oyun Tamamlandı!")
    st.subheader(f"Toplam Skorunuz: {st.session_state.total_score}")
    st.write(f"5 futbolcudan oluşan turu tamamladınız.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Tekrar Oyna", use_container_width=True):
            reset_game()
    with col2:
        if st.button("❌ Çıkış", use_container_width=True):
            st.write("Oynadığınız için teşekkürler! Sayfayı kapatabilirsiniz.")
            st.stop()
    st.stop() # Oyun bittiyse aşağıdaki kodları çalıştırma

# ----- OYUN ARAYÜZÜ -----
st.title("⚽ Futbolcu Tahmin Turu")

# Durum Bilgisi
c1, c2 = st.columns(2)
c1.metric("Soru", f"{st.session_state.current_question} / {st.session_state.max_questions}")
c2.metric("Toplam Puan", st.session_state.total_score)

# Resim Alanı
image_placeholder = st.empty()
player_data = players_data[st.session_state.target_player]

# Bulanıklık Hesaplama (5 hakka göre 25'ten 0'a)
blur_levels = [25, 18, 12, 6, 2, 0]
current_blur = blur_levels[min(st.session_state.attempts, 5)]

if os.path.exists(player_data["file"]):
    img = Image.open(player_data["file"])
    blurred_img = img.filter(ImageFilter.GaussianBlur(current_blur))
    image_placeholder.image(blurred_img, use_container_width=True)
else:
    st.error(f"Resim bulunamadı: {player_data['file']}")

# İpuçları Alanı
all_hints = [
    f"🌍 Uyruk: {player_data['nationality']}",
    f"🏃 Pozisyon: {player_data['position']}",
    f"🎂 Yaş: {player_data['age']}",
    f"🏢 Takım: {player_data['team']}"
]

with st.expander("💡 İpuçlarını Gör", expanded=True):
    if st.session_state.attempts == 0:
        st.write("İlk ipucunu görmek için yanlış tahmin yapmalı veya pas geçmelisiniz.")
    for i in range(st.session_state.attempts):
        if i < len(all_hints):
            st.info(all_hints[i])

# ----- TAHMİN FORMU -----
with st.form(key="guess_form", clear_on_submit=True):
    user_guess = st.text_input("Tahmininiz (İsim veya Soyisim):").strip().lower()
    submit_button = st.form_submit_button("Gönder")

if submit_button:
    correct_name = st.session_state.target_player.lower()
    
    # DOĞRU TAHMİN
    if user_guess != "" and (user_guess in correct_name and len(user_guess) > 3):
        image_placeholder.image(img, use_container_width=True, caption=f"TEBRİKLER! Cevap: {st.session_state.target_player}")
        gain = (5 - st.session_state.attempts) * 20
        st.session_state.total_score += gain
        st.success(f"✅ Doğru! +{gain} Puan kazandınız.")
        time.sleep(2.5)
        st.session_state.current_question += 1
        pick_new_player()
        st.rerun()
    
    # YANLIŞ TAHMİN
    else:
        st.session_state.attempts += 1
        
        if st.session_state.attempts >= 5:
            # HAKLAR BİTTİ: Net resmi göster
            image_placeholder.image(img, use_container_width=True, caption=f"Cevap: {st.session_state.target_player}")
            st.error(f"❌ Bilemediniz! Doğru cevap: {st.session_state.target_player}")
            st.info("Puan alamadınız. Sonraki soruya geçiliyor...")
            time.sleep(3)
            st.session_state.current_question += 1
            pick_new_player()
            st.rerun()
        else:
            st.warning(f"Yanlış! {5 - st.session_state.attempts} hakkınız kaldı. Resim netleşiyor ve yeni ipucu geldi.")
            st.rerun()
