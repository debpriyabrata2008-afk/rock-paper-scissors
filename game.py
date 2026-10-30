
import streamlit as st
import random
import io
import wave
import math
import struct

st.set_page_config(
    page_title="RPS ARENA",
    page_icon="🎮",
    layout="wide"
)

# SOUND GENERATOR
def create_sound(notes):
    sample_rate = 22050
    audio = io.BytesIO()

    with wave.open(audio, "wb") as sound:
        sound.setnchannels(1)
        sound.setsampwidth(2)
        sound.setframerate(sample_rate)

        for frequency in notes:
            duration = 0.15
            total_samples = int(sample_rate * duration)

            for i in range(total_samples):
                t = i / sample_rate
                envelope = min(1, i / 300, (total_samples-i) / 500)
                value = int(
                    12000 * envelope *
                    math.sin(2 * math.pi * frequency * t)
                )
                sound.writeframesraw(struct.pack("<h", value))

    return audio.getvalue()


WIN_SOUND = create_sound([523, 659, 784, 1047])
LOSE_SOUND = create_sound([392, 330, 262])
DRAW_SOUND = create_sound([440, 440])

# DESIGN
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#101020,#171333,#101020);
    color: white;
}
h1 {
    text-align: center;
    color: #a78bfa;
    text-shadow: 0 0 15px #8b5cf6;
}
.stButton > button {
    width: 100%;
    height: 75px;
    border-radius: 15px;
    background: linear-gradient(135deg,#6d28d9,#2563eb);
    color: white;
    font-size: 22px;
    font-weight: bold;
    transition: 0.25s;
}
.stButton > button:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 20px #8b5cf6;
    color: white;
}
.card {
    background: #211b3b;
    border: 1px solid #7053bb;
    border-radius: 18px;
    padding: 22px;
    text-align: center;
}
.result {
    font-size: 25px;
    text-align: center;
    color: #c4b5fd;
    font-weight: bold;
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

# GAME DATA
defaults = {
    "player_score": 0,
    "computer_score": 0,
    "rounds": 0,
    "result": "Choose your move!",
    "player_choice": None,
    "computer_choice": None,
    "history": [],
    "match_over": False,
    "sound_data": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# GAME LOGIC
def play(player):

    if st.session_state.match_over:
        return

    computer = random.choice(["Rock", "Paper", "Scissors"])

    st.session_state.player_choice = player
    st.session_state.computer_choice = computer
    st.session_state.rounds += 1

    if player == computer:
        result = "🤝 IT'S A DRAW!"
        st.session_state.sound_data = DRAW_SOUND

    elif (
        (player == "Rock" and computer == "Scissors")
        or (player == "Paper" and computer == "Rock")
        or (player == "Scissors" and computer == "Paper")
    ):
        result = "🏆 YOU WIN THIS ROUND!"
        st.session_state.player_score += 1
        st.session_state.sound_data = WIN_SOUND

    else:
        result = "🤖 COMPUTER WINS THIS ROUND!"
        st.session_state.computer_score += 1
        st.session_state.sound_data = LOSE_SOUND

    st.session_state.result = result

    st.session_state.history.insert(
        0, f"Round {st.session_state.rounds}: {player} vs {computer} — {result}"
    )

    if st.session_state.player_score == 3:
        st.session_state.match_over = True
        st.balloons()

    elif st.session_state.computer_score == 3:
        st.session_state.match_over = True


# TITLE
st.markdown("<h1>⚔️ RPS ARENA ⚔️</h1>", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center;color:#c4b5fd;'>"
    "THE ULTIMATE ROCK PAPER SCISSORS BATTLE"
    "</p>",
    unsafe_allow_html=True
)

st.divider()

# SCOREBOARD
st.subheader("🏆 LIVE SCOREBOARD")

c1, c2, c3 = st.columns(3)

c1.metric("👑 YOU", st.session_state.player_score)
c2.metric("🤖 COMPUTER", st.session_state.computer_score)
c3.metric("🎯 ROUNDS", st.session_state.rounds)

st.caption("First to 3 wins takes the match!")

st.divider()

# CHOICES
st.subheader("🎮 CHOOSE YOUR WEAPON")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🪨 ROCK", disabled=st.session_state.match_over):
        play("Rock")

with col2:
    if st.button("📄 PAPER", disabled=st.session_state.match_over):
        play("Paper")

with col3:
    if st.button("✂️ SCISSORS", disabled=st.session_state.match_over):
        play("Scissors")

# SHOW MOVES
if st.session_state.player_choice:

    icons = {
        "Rock": "🪨",
        "Paper": "📄",
        "Scissors": "✂️"
    }

    a, b = st.columns(2)

    with a:
        st.markdown(f"""
        <div class="card">
        <h3>👑 YOUR MOVE</h3>
        <div style="font-size:65px">{icons[st.session_state.player_choice]}</div>
        <h2>{st.session_state.player_choice}</h2>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown(f"""
        <div class="card">
        <h3>🤖 COMPUTER MOVE</h3>
        <div style="font-size:65px">{icons[st.session_state.computer_choice]}</div>
        <h2>{st.session_state.computer_choice}</h2>
        </div>
        """, unsafe_allow_html=True)

# RESULT
st.markdown(
    f'<div class="result">{st.session_state.result}</div>',
    unsafe_allow_html=True
)

# SOUND
if st.session_state.sound_data:
    st.audio(
        st.session_state.sound_data,
        format="audio/wav",
        autoplay=True
    )
    st.session_state.sound_data = None

# MATCH WINNER
if st.session_state.match_over:

    if st.session_state.player_score == 3:
        st.success("🎉 CHAMPION! YOU WON THE MATCH!")
    else:
        st.error("🤖 COMPUTER WON THE MATCH! TRY AGAIN!")

# HISTORY
with st.expander("📜 MATCH HISTORY"):
    if st.session_state.history:
        for item in st.session_state.history:
            st.write(item)
    else:
        st.write("No rounds played yet.")

st.divider()

# RESET
if st.button("🔄 RESTART MATCH", use_container_width=True):

    for key, value in defaults.items():
        st.session_state[key] = value

    st.rerun()

st.markdown(
    "<p style='text-align:center;color:#a78bfa;'>"
    "BUILT WITH PYTHON ❤️ | RPS ARENA"
    "</p>",
    unsafe_allow_html=True
)

