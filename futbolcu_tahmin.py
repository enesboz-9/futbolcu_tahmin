import streamlit as st
from PIL import Image, ImageFilter
import random
import os
import time
import base64

# Sayfa Ayarları
st.set_page_config(page_title="⚽ Futbolcu Tahmin Oyunu", layout="centered")

# ----- Ses Çalma Fonksiyonu -----
def play_sound(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio autoplay="true">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.components.v1.html(md, height=0)

# ----- Futbolcu Verileri -----
players_data = {
    "lionel messi": {"file": "images/messi.jpg", "team": "Inter Miami", "nationality": "Arjantin", "position": "Forvet", "age": 36, "birth_year": 1987},
    "cristiano ronaldo": {"file": "images/ronaldo.jpg", "team": "Al Nassr", "nationality": "Portekiz", "position": "Forvet", "age": 38, "birth_year": 1985},
    "neymar": {"file": "images/neymar.jpg", "team": "Al-Hilal", "nationality": "Brezilya", "position": "Forvet", "age": 31, "birth_year": 1992},
    "kylian mbappé": {"file": "images/mbappe.jpg", "team": "Paris Saint-Germain", "nationality": "Fransa", "position": "Forvet", "age": 24, "birth_year": 1998},
    "erling haaland": {"file": "images/haaland.jpg", "team": "Manchester City", "nationality": "Norveç", "position": "Forvet", "age": 23, "birth_year": 2000}
}

# ----- Session State Başlat -----
if "difficulty" not in st.session_state:
    st.title("⚽ Futbolcu Tahmin Oyunu")
    st.subheader("Hoş Geldiniz! Başlamadan önce zorluk seçin:")
    diff = st.radio("Zorluk Seviyesi:", ["Kolay", "Orta", "Zor"], index=1)
    
    if st.button("Oyunu Başlat"):
        st.session_state.difficulty = diff
        # Zorluğa göre bulanıklık (blur) haritası
        if diff == "Kolay":
            st.session_state.blur_map = [12, 9, 6, 3, 1, 0]
            st.session_state.multiplier = 1
        elif diff == "Orta":
            st.session_state.blur_map = [25, 18, 12, 6, 2, 0]
            st.session_state.multiplier = 2
        else:
            st.session_state.blur_map = [45, 30, 20, 10, 5, 0]
            st.session_state.multiplier = 3
            
        st.session_state.played_players = []
        st.session_state.current_question = 1
        st.session_state.max_questions = 5
        st.session_state.target_player = None
        st.session_state.attempts = 0
        st.session_state.total_score = 0
        st.session_state.game_finished = False
        st.rerun()
    st.stop()

def pick_new_player():
    remaining = [p for p in players_data.keys() if p not in st.session_state.played_players]
    if remaining and st.session_state.current_question <= st.session_state.max_questions:
        new_player = random.choice(remaining)
        st.session_state.target_player = new_player
        st.session_state.played_players.append(new_player)
        st.session_state.attempts = 0
    else:
        st.session_state.game_finished = True

def reset_entire_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# İlk futbolcuyu seç
if st.session_state.target_player is None and not st.session_state.game_finished:
    pick_new_player()

# ----- OYUN BİTİŞ EKRANI -----
if st.session_state.game_finished:
    st.balloons()
    st.header("🏆 Tur Tamamlandı!")
    st.subheader(f"Zorluk: {st.session_state.difficulty}")
    st.title(f"Toplam Skor: {st.session_state.total_score}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Tekrar Oyna", use_container_width=True):
            reset_entire_game()
    with col2:
        if st.button("❌ Çıkış", use_container_width=True):
            st.stop()
    st.stop()

# ----- OYUN ARAYÜZÜ -----
st.title("⚽ Futbolcu Tahmin Turu")
st.caption(f"Zorluk: {st.session_state.difficulty} | Çarpan: x{st.session_state.multiplier}")

col_info1, col_info2 = st.columns(2)
col_info1.metric("Soru", f"{st.session_state.current_question} / {st.session_state.max_questions}")
col_info2.metric("Toplam Puan", st.session_state.total_score)

# Resim Hazırlama
player_info = players_data[st.session_state.target_player]
current_blur = st.session_state.blur_map[min(st.session_state.attempts, 5)]

image_placeholder = st.empty()
if os.path.exists(player_info["file"]):
    img = Image.open(player_info["file"])
    blurred_img = img.filter(ImageFilter.GaussianBlur(current_blur))
    image_placeholder.image(blurred_img, use_container_width=True)
else:
    st.error(f"Resim bulunamadı: {player_info['file']}")

# İpuçları
all_hints = [
    f"🌍 Milliyet: {player_info['nationality']}",
    f"🏢 Takım: {player_info['team']}",
    f"🏃 Pozisyon: {player_info['position']}",
    f"🎂 Yaş: {player_info['age']}",
    f"📅 Doğum Yılı: {player_info['birth_year']}"
]

with st.expander("💡 İpuçları", expanded=True):
    if st.session_state.attempts == 0:
        st.write("İpuçları yanlış tahminlerde açılır.")
    for i in range(st.session_state.attempts):
        if i < len(all_hints):
            st.info(all_hints[i])

# ----- TAHMİN FORMU -----
with st.form(key="action_form", clear_on_submit=True):
    user_guess = st.text_input("Tahmininizi yazın:").strip().lower()
    c1, c2 = st.columns(2)
    submit = c1.form_submit_button("Tahmin Et", use_container_width=True)
    pass_q = c2.form_submit_button("Pas Geç", use_container_width=True)

if submit:
    correct_name = st.session_state.target_player.lower()
    if user_guess != "" and (user_guess in correct_name and len(user_guess) > 3):
        # DOĞRU
        play_sound("sounds/goal.mp3")
        image_placeholder.image(img, use_container_width=True, caption=f"DOĞRU! Cevap: {st.session_state.target_player.title()}")
        gain = (5 - st.session_state.attempts) * 20 * st.session_state.multiplier
        st.session_state.total_score += gain
        st.success(f"✅ Tebrikler! {gain} puan kazandınız.")
        time.sleep(3)
        st.session_state.current_question += 1
        pick_new_player()
        st.rerun()
    else:
        # YANLIŞ
        st.session_state.attempts += 1
        if st.session_state.attempts >= 5:
            play_sound("sounds/whistle.mp3")
            image_placeholder.image(img, use_container_width=True, caption=f"Cevap: {st.session_state.target_player.title()}")
            st.error(f"❌ Haklarınız bitti! Cevap: {st.session_state.target_player.title()}")
            time.sleep(3)
            st.session_state.current_question += 1
            pick_new_player()
            st.rerun()
        else:
            st.rerun()

if pass_q:
    image_placeholder.image(img, use_container_width=True, caption=f"Cevap: {st.session_state.target_player.title()}")
    st.info(f"⏭️ Pas geçildi. Doğru cevap: {st.session_state.target_player.title()}")
    time.sleep(3)
    st.session_state.current_question += 1
    pick_new_player()
    st.rerun()
