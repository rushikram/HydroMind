import streamlit as st
import requests
import pandas as pd

# 🌐 Backend API Base URL
API_BASE = "https://hydromind.onrender.com"

# === Streamlit Page Config ===
st.set_page_config(page_title="HydroMind", layout="centered", page_icon="💧")
st.title("💧 HydroMind: Your AI Hydration Coach")

# === Sidebar Configuration ===
st.sidebar.title("⚙️ Preferences")

user_id = st.sidebar.text_input("Enter your name or user ID", value="guest")
user_goal = st.sidebar.number_input("Set your daily goal (ml)", min_value=500, step=100, value=2000)
groq_key = st.sidebar.text_input("Enter your Groq API key", type="password")

# === Reset Log Button ===
if st.sidebar.button("🔄 Reset Today's Log"):
    try:
        r = requests.post(f"{API_BASE}/reset/", json={"user_id": user_id})
        if r.status_code == 200:
            st.success("✅ Log reset for today.")
            st.rerun()
        else:
            st.error("❌ Failed to reset log.")
    except Exception as e:
        st.error(f"🚫 Reset failed: {e}")

# === Water Logging Form ===
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

# === Hydration History ===
# === Hydration History ===
st.subheader("📈 Hydration History")

try:
    response = requests.get(f"{API_BASE}/history/{user_id}")
    
    if response.ok:
        raw_data = response.json()

        if not raw_data:
            st.info("📭 No records yet. Start by logging your first entry.")
        else:
            # Ensure it's a list of records
            if isinstance(raw_data, dict):
                raw_data = [raw_data]

            data = pd.DataFrame(raw_data)

            # Validate necessary columns
            if "timestamp" in data.columns and "amount_ml" in data.columns:
                # Parse timestamp column
                data["timestamp"] = pd.to_datetime(data["timestamp"], errors="coerce")
                data = data.dropna(subset=["timestamp"])  # drop bad timestamps

                # Sort by time
                data = data.sort_values("timestamp")

                if not data.empty:
                    st.line_chart(data.set_index("timestamp")["amount_ml"])
                    st.dataframe(data.rename(columns={
                        "timestamp": "Time",
                        "amount_ml": "Amount (ml)"
                    }))
                else:
                    st.info("📭 No valid entries to visualize yet.")
            else:
                st.warning("⚠️ Data format issue: Missing required fields.")
    else:
        st.error(f"❌ Failed to load data: {response.status_code}")
except Exception as e:
    st.error(f"🚫 Error loading history: {e}")


# === AI Hydration Coach ===
st.subheader("🤖 Ask Your Hydration Coach")
question = st.text_input("Ask something like: 'Did I drink enough today?'")

if st.button("Ask"):
    if not groq_key:
        st.warning("⚠️ Please enter your Groq API key.")
    elif not question.strip():
        st.warning("⚠️ Please ask a question.")
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
