import streamlit as st
import requests
import pandas as pd

# 🌐 Use your deployed FastAPI Render URL
API_BASE = "https://hydromind.onrender.com"

st.set_page_config(page_title="HydroMind", layout="centered", page_icon="💧")
st.title("💧 HydroMind: Your AI Hydration Coach")

st.sidebar.title("⚙️ Preferences")

# NEW: User ID input
user_id = st.sidebar.text_input("Enter your name or user ID", value="guest")

user_goal = st.sidebar.number_input("Set your daily goal (ml)", min_value=500, step=100, value=2000)
groq_key = st.sidebar.text_input("Enter your Groq API key", type="password")

# DB reset button
if st.sidebar.button("🔄 Reset Today's Log"):
    try:
        r = requests.post(f"{API_BASE}/reset/")
        if r.status_code == 200:
            st.success("✅ Log reset for today.")
            st.rerun()
        else:
            st.error("❌ Failed to reset log.")
    except Exception as e:
        st.error(f"🚫 Reset failed: {e}")

# Log form
with st.form("log_form"):
    amount = st.number_input("Water Intake (ml)", min_value=50, step=50)
    submitted = st.form_submit_button("Add Entry")
    if submitted:
        try:
            payload = {"user_id": user_id, "amount_ml": amount}
            response = requests.post(f"{API_BASE}/add-entry/", json=payload)
            if response.status_code == 200:
                st.success("✅ Water logged successfully!")
                st.rerun()
            else:
                st.error(f"❌ Failed to log water: {response.status_code}")
        except Exception as e:
            st.error(f"🚫 Request error: {e}")

# History chart
st.subheader("📈 Hydration History")
try:
    response = requests.get(f"{API_BASE}/history/{user_id}")
    if response.ok:
        raw_data = response.json()
        if raw_data:  # ✅ Prevent DataFrame error on empty list
            data = pd.DataFrame(raw_data)
            data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
            st.line_chart(data.set_index("timestamp")["amount_ml"])
            st.dataframe(data.rename(columns={"timestamp": "Time", "amount_ml": "Amount (ml)"}))
        else:
            st.info("📭 No records yet. Start by logging your first entry.")
    else:
        st.error("❌ Failed to load data.")
except Exception as e:
    st.error(f"🚫 Error loading history: {e}")

# Ask AI
st.subheader("🤖 Ask Your Hydration Coach")
question = st.text_input("Ask something like: 'Did I drink enough today?'")
if st.button("Ask"):
    if not groq_key:
        st.warning("⚠️ Please enter your Groq API key.")
    else:
        try:
            full_prompt = f"{question.strip()} (Today’s hydration goal: {user_goal} ml)"
            response = requests.post(
                f"{API_BASE}/ask-agent/",
                json={"question": full_prompt, "groq_key": groq_key, "goal_ml": user_goal}
            )
            if response.ok:
                st.markdown(f"**🧠 Coach says:** {response.json().get('response')}")
            else:
                st.error(f"❌ Error: {response.status_code}")
        except Exception as e:
            st.error(f"🚫 Error talking to agent: {e}")
