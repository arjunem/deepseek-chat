# 🤖 **Streamlit Chatbot with Ollama & DeepSeek Models**  
A dynamic **AI-powered chatbot** built with **Streamlit**, integrating the **Ollama API** and **DeepSeek AI models** for real-time, conversational interactions. Customize your experience with multiple **AI models** and **conversation tones**!  

🚀 **Features** | 🎨 **Custom UI** | 🎭 **Tone Selection** | ⚡ **Real-Time AI Responses**  

---

## ✨ **Features**  

### 🎨 **User Interface & Customization**  
- 🚀 **Minimalist design** – Hides Streamlit’s default header, footer, and menu.  
- 📏 **Wide layout** for enhanced readability and user experience.  

### 🧠 **AI Model & Tone Selection**  
- 🔄 **Dynamically fetches AI models** from the **Ollama API** (`/api/tags`).  
- 🎭 Choose from **four conversation tones**:  
  - 🗣️ Casual  
  - 🎓 Formal  
  - 😏 Sarcastic  
  - ⚡ Minimalist  
- 💡 **Suggested prompts** tailored to the selected tone.  

### 💬 **Chat Interaction & History**  
- 💾 **Saves & loads chat history** (`chat_history.json`) for seamless conversations.  
- 🔥 **Real-time AI response streaming** for a smooth experience.  
- 🧐 Displays **AI reasoning separately** (if available).  
- ⏳ **Progress indicator** while generating responses.  

### 🔥 **Suggested Prompts**  
- 📝 **Dynamic prompts** appear based on the selected tone.  
- ⚡ Click to **auto-fill** the chat input for quick responses.  

### 🛠 **Error Handling & Stability**  
- 🚧 Detects **server connection issues** and provides troubleshooting tips.  
- 🔄 **Manages session state** efficiently to avoid inconsistencies.  

---

## 🚀 **How It Works**  
1️⃣ **Loads chat history** and fetches available AI models upon startup.  
2️⃣ Displays UI elements for **model selection, tone selection, and chat input**.  
3️⃣ When a user sends a message:  
   - 📨 **Request is sent** to the Ollama API for **streaming response generation**.  
   - ⏳ **Progress bar animates** while waiting for the response.  
   - 🔍 If available, **AI reasoning can be expanded**.  
   - 💾 **Messages are saved** in `chat_history.json`.  
4️⃣ **Suggested prompts** dynamically update based on the chosen tone.  

---

## 🛠 **Installation & Setup**  

### **1️⃣ Install Ollama**  
Ollama is required to run the chatbot. Install it using the steps below:  

#### 🖥 **For macOS**  
```bash
brew install ollama
```
#### 🖥 **For Linux**  
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
#### 🖥 **For Windows**  
- Download and install Ollama from [ollama.com](https://ollama.com).  

🔄 **Start Ollama** (Ensure it's running before using the chatbot):  
```bash
ollama serve
```
By default, the API will be available at **`http://localhost:11434`**.  

---

### **2️⃣ Install & Run the Chatbot**  

#### **Prerequisites**  
Ensure you have the following installed:  
- **Python 3.8+**  
- **Streamlit** (`pip install streamlit`)  
- **Requests** (`pip install requests`)  

#### **Run the App**  
```bash
# Clone the repository
git clone https://github.com/your-username/streamlit-chatbot-ollama.git

# Navigate into the project folder
cd streamlit-chatbot-ollama

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```
🚀 Open your browser and navigate to **`http://localhost:8501`**  

---

### **3️⃣ Install DeepSeek Model for Ollama**  
This chatbot supports **DeepSeek AI models**, which you need to install manually.  

#### **Install DeepSeek Models in Ollama**  
```bash
ollama run deepseek-r1:1.5b
```
or for a specific version:  
```bash
ollama run deepseek-r1:1.5b
```
Check if the model is available:  
```bash
ollama list
```
Once installed, **restart Ollama** and the chatbot will automatically detect the model.  

---

## 🎯 **Customization**  

### **Modify Available AI Models**  
The app dynamically fetches models from Ollama, but you can manually edit them by modifying:  
```python
def load_models() -> list[str]:
    return ["deepseek-chat", "deepseek-chat:67b", "custom-model:latest"]
```

### **Customize Conversation Tones**  
Modify the tones and suggested prompts in:  
```python
prompts = {
    "Casual": ["What's something fun to do this weekend?"],
    "Formal": ["Explain quantum computing in simple terms."],
    "Sarcastic": ["Oh sure, tell me why Mondays are amazing. 🙄"],
    "Minimalist": ["Best productivity hack?"]
}
```

---

## 🛠 **Troubleshooting**  
### **Ollama API Connection Issues**  
- Ensure Ollama is running:  
  ```bash
  ollama serve
  ```
- Check if the API is accessible at `http://localhost:11434`.  
- Restart the Streamlit app and try again.  

### **DeepSeek Model Not Found?**  
- Run `ollama list` to check if **DeepSeek** is installed.  
- If missing, install it using:  
  ```bash
  ollama pull deepseek-chat
  ```
- Restart Ollama and rerun the chatbot.  

---

## 📜 **License**  
This project is licensed under the **MIT License**.  

📢 **Have suggestions or improvements?** Feel free to submit a PR or open an issue!  

🚀 **Happy Chatting!** 🎉  

---

Now your **README** includes **DeepSeek model installation** and **troubleshooting steps**! 🚀 Let me know if you want more refinements. 😊
