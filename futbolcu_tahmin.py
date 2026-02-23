,import streamlit as st
from PIL import Image, ImageFilter
import random
import os
import time

# Sayfa Ayarları
st.set_page_config(page_title="⚽ Futbolcu Tahmin Oyunu", layout="centered")

# ----- Futbolcu Verileri (Sadece senin verdiklerin) -----
if "players_data" not in st.session_state:
    st.session_state.players_data = {
        "lionel messi": {"file": "images/messi.jpg", "team": "Inter Miami", "nationality": "Arjantin", "position": "Forvet", "age": 36, "birth_year": 1987},
        "cristiano ronaldo": {"file": "images/ronaldo.jpg", "team": "Al Nassr", "nationality": "Portekiz", "position": "Forvet", "age": 38, "birth_year": 1985},
        "neymar": {"file": "images/neymar.jpg", "team": "Al-Hilal", "nationality": "Brezilya", "position": "Forvet", "age": 31, "birth_year": 1992},
        "kylian mbappé": {"file": "images/mbappe.jpg", "team": "Paris Saint-Germain", "nationality": "Fransa", "position": "Forvet", "age": 24, "birth_year": 1998},
        "erling haaland": {"file": "images/haaland.jpg", "team": "Manchester City", "nationality": "Norveç", "position": "Forvet", "age": 23, "birth_year": 2000}
    }

# ----- Session State Başlat -----
if "played_players" not in st.session_state:
    st.session_state.played_players = []
    st.session_state.current_question = 1
    st.session_state.max_questions = 5
    st.session_state.target_player = None
    st.session_state.attempts = 0
    st.session_state.total_score = 0
    st.session_state.game_finished = False

def pick_new_player():
    remaining = [p for p in st.session_state.players_data.keys() if p not in st.session_state.played_players]
    if remaining and st.session_state.current_question <= st.session_state.max_questions:
        new_player = random.choice(remaining)
        st.session_state.target_player = new_player
        st.session_state.played_players.append(new_player)
        st.session_state.attempts = 0
    else:
        st.session_state.game_finished = True

def reset_game():
    st.session_state.played_players = []
    st.session_state.current_question = 1
    st.session_state.total_score = 0
    st.session_state.game_finished = False
    st.session_state.target_player = None
    pick_new_player()
    st.rerun()

# Oyun başında futbolcu seç
if st.session_state.target_player is None and not st.session_state.game_finished:
    pick_new_player()

# ----- OYUN BİTİŞ EKRANI -----
if st.session_state.game_finished:
    st.balloons()
    st.header("🏆 Tur Tamamlandı!")
    st.subheader(f"Toplam Puanınız: {st.session_state.total_score}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Tekrar Oyna", use_container_width=True):
            reset_game()
    with col2:
        if st.button("❌ Çıkış", use_container_width=True):
            st.stop()
    st.stop()

# ----- OYUN ARAYÜZÜ -----
st.title("⚽ Futbolcu Tahmin Oyunu")

# Bilgi Paneli
c1, c2 = st.columns(2)
c1.metric("Soru", f"{st.session_state.current_question} / {st.session_state.max_questions}")
c2.metric("Toplam Puan", st.session_state.total_score)

# Resim ve İpucu Hazırlığı
player_info = st.session_state.players_data[st.session_state.target_player]
blur_levels = [15, 12, 9, 6, 3, 0]
current_blur = blur_levels[min(st.session_state.attempts, 5)]

image_placeholder = st.empty()
if os.path.exists(player_info["file"]):
    img = Image.open(player_info["file"])
    blurred_img = img.filter(ImageFilter.GaussianBlur(current_blur))
    image_placeholder.image(blurred_img, use_container_width=True)
else:
    st.error(f"Resim dosyası bulunamadı: {player_info['file']}")

# İpuçları
all_hints = [
    f"🌍 Milliyet: {player_info['nationality']}",
    f"🏢 Takım: {player_info['team']}",
    f"🏃 Pozisyon: {player_info['position']}",
    f"🎂 Yaş: {player_info['age']}",
    f"📅 Doğum Yılı: {player_info['birth_year']}"
]

with st.expander("💡 İpuçları (Yanlış tahminlerde açılır)", expanded=True):
    for i in range(st.session_state.attempts):
        if i < len(all_hints):
            st.info(all_hints[i])

# ----- TAHMİN VE PAS FORMU -----
with st.form(key="game_form", clear_on_submit=True):
    user_guess = st.text_input("Futbolcunun adı:").strip().lower()
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        submit = st.form_submit_button("Tahmin Et", use_container_width=True)
    with col_btn2:
        pass_btn = st.form_submit_button("Pas Geç", use_container_width=True)

# ----- OYUN MANTIĞI -----
if submit:
    if user_guess == "":
        st.warning("Lütfen bir isim yazın!")
    else:
        correct_name = st.session_state.target_player.lower()
        # İsim veya soyisim kontrolü
        if user_guess in correct_name and len(user_guess) > 3:
            image_placeholder.image(img, use_container_width=True, caption=f"TEBRİKLER! Cevap: {st.session_state.target_player.title()}")
            gain = (5 - st.session_state.attempts) * 20
            st.session_state.total_score += gain
            st.success(f"✅ Doğru! +{gain} puan.")
            time.sleep(3) # 3 saniye bekleme
            st.session_state.current_question += 1
            pick_new_player()
            st.rerun()
        else:
            st.session_state.attempts += 1
            if st.session_state.attempts >= 5:
                image_placeholder.image(img, use_container_width=True, caption=f"Cevap: {st.session_state.target_player.title()}")
                st.error(f"❌ Haklarınız bitti. Doğru cevap: {st.session_state.target_player.title()}")
                time.sleep(3)
                st.session_state.current_question += 1
                pick_new_player()
                st.rerun()
            else:
                st.rerun()

if pass_btn:
    image_placeholder.image(img, use_container_width=True, caption=f"Pas geçildi. Cevap: {st.session_state.target_player.title()}")
    st.info(f"⏭️ Pas geçildi. Doğru cevap: {st.session_state.target_player.title()}")
    time.sleep(3)
    st.session_state.current_question += 1
    pick_new_player()
    st.rerun()
