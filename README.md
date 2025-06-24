# 💧 Hydration Tracker Agent(HydroMind)

<div align="center">

![LangChain](https://img.shields.io/badge/LangChain-Powered-green?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-AI-purple?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge)

**AI-powered hydration tracking system built with LangChain and Groq**

[🌐 Live Demo](#-live-deployment) • [🚀 Quick Start](#-quick-start) • [🤖 AI Features](#-ai-features)

</div>

---

## 📋 Project Overview

HydroMind is an agentic AI–powered hydration tracking system that leverages LangChain agents and Groq’s ultra-fast LLMs to deliver personalized, real-time hydration coaching. Unlike traditional static apps, HydroMind acts as an autonomous AI agent that perceives user behavior, reasons over their hydration data, and proactively responds with tailored suggestions and actionable feedback.



### 🎯 **Key Problem Solved**
- Manual water intake tracking is tedious and often forgotten
- Generic hydration advice doesn't account for individual needs
- No intelligent feedback system for hydration habits

### 💡 **Solution Approach**
- **LangChain agents** with custom tools for dynamic data retrieval
- **Groq AI** for fast, personalized hydration coaching
- **Multi-user support** with individual tracking and goals

---

## 🛠️ Technical Architecture of Agentic-AI

```
User Request → LangChain Agent → Custom Tools → Database → AI Response
                     ↓
               Groq LLM (Fast Inference)
```

### **Core Components:**

| Component | Technology | Purpose |
|-----------|------------|---------|
| **AI Agent** | LangChain | Orchestrates tools and generates responses |
| **LLM Provider** | Groq (LLaMA3-70B) | Fast AI inference for coaching |
| **Custom Tools** | Python Functions | Fetch user data, calculate goals |
| **Database** | SQLite | Store user intake data |
| **API** | FastAPI | RESTful backend service |
| **Frontend** | Streamlit | User interface |

---

## 🗂️ Project Structure

```
hydration-tracker/
├── app.py                   # Main application entry point
├── tools.py                 # LangChain custom tools definition
├── backend/
│   └── db.py               # Database operations (get_today_total)
├── requirements.txt         # Python dependencies
└── README.md               # Documentation
```

---

## ⚡ Quick Start

### 1. **Clone Repository**
```bash
git clone https://github.com/rushikdumpala/hydration-tracker.git
cd hydration-tracker
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Setup Groq API Key**
```bash
# Get your free API key from: https://console.groq.com/keys
export GROQ_API_KEY="your_api_key_here"
```

### 4. **Run Application**
```bash
python app.py
```

---

## 🤖 AI Features

### **LangChain Agent Capabilities:**

✅ **Smart Data Retrieval**
- Fetches real-time user water intake using custom tools
- Calculates progress against personalized hydration goals

✅ **Intelligent Coaching**
- Provides contextual advice based on current intake
- Suggests optimal drinking schedules and amounts

✅ **Multi-User Support**
- Handles multiple users with dynamic `user_id` parameter
- Maintains separate tracking for each user

### **Example AI Interactions:**

```
🤖 User: "How much water should I drink now?"
💧 AI: "You've consumed 1.2L out of your 2.5L daily goal. 
       I recommend drinking 250ml now and setting reminders 
       for every 2 hours to stay on track."

🤖 User: "Did I meet my hydration goal today?"
💧 AI: "You're at 80% of your daily goal with 2.0L consumed. 
       Great progress! Just 500ml more to reach your target."
```

---

## 🌐 Live Deployment

| Service | URL | Status |
|---------|-----|--------|
| **Main App** | [hydration-tracker.streamlit.app](https://hydromind-kws2qtsnyyigqrssbkrxjn.streamlit.app/) | 🟢 Live |
| **API Backend** | [hydration-api.onrender.com](https://hydromind.onrender.com) | 🟢 Live |
| **Documentation** | [GitHub Repository](https://github.com/rushikram/HydroMind) | 🟢 Active |

---

## 🔧 Technical Implementation

### **Custom LangChain Tools:**

```python
# Example tool implementation
@tool
def get_user_hydration_data(user_id: str) -> dict:
    """Retrieves current water intake for a specific user"""
    total_intake = get_today_total(user_id)  # From db.py
    goal = get_user_goal(user_id)
    return {
        "current_intake": total_intake,
        "daily_goal": goal,
        "progress_percentage": (total_intake/goal) * 100
    }
```

### **Agent Configuration:**
- **Model**: Groq LLaMA3-70B (Ultra-fast inference)
- **Tools**: Custom hydration tracking functions
- **Memory**: Conversation context for personalized responses

---

## 📊 Key Features

| Feature | Description | Technical Benefit |
|---------|-------------|-------------------|
| **Real-time Tracking** | Live water intake monitoring | Immediate data retrieval via custom tools |
| **Personalized Goals** | Individual hydration targets | Dynamic calculation based on user profile |
| **AI Coaching** | Intelligent recommendations | Context-aware responses using LangChain |
| **Multi-user Support** | Scalable user management | Efficient database queries with user_id |
| **Fast Responses** | Quick AI inference | Groq's optimized hardware acceleration |

---

## 🚀 Why This Project Stands Out

### **For Interviewers:**

1. **Modern AI Stack**: Demonstrates proficiency in cutting-edge AI tools (LangChain, Groq)

2. **Practical Application**: Solves a real-world problem with measurable impact

3. **Clean Architecture**: Well-structured code with separation of concerns

4. **Scalable Design**: Multi-user support shows understanding of production systems

5. **Full-Stack Implementation**: Frontend, backend, database, and AI integration

### **Technical Highlights:**

- ⚡ **Performance**: Groq provides 10x faster inference than traditional APIs
- 🔧 **Flexibility**: Custom LangChain tools allow easy feature expansion  
- 📈 **Scalability**: Database design supports thousands of users
- 🛠️ **Maintainability**: Modular codebase with clear responsibilities

---

## 🔑 Groq AI Integration

### **Setup Process:**

1. **Get API Key**: Visit [console.groq.com/keys](https://console.groq.com/keys)
2. **Add to Environment**: `export GROQ_API_KEY="your_key"`
3. **Configure in App**: Automatic detection and initialization

### **Why Groq?**
- **Speed**: 500+ tokens/second inference
- **Cost-effective**: Competitive pricing for high-volume usage
- **Reliability**: 99.9% uptime with global infrastructure

---

## 👨‍💻 Author

**Rushik Dumpala**  
🔗 GitHub: [@rushikdumpala](https://github.com/rushikram)  


