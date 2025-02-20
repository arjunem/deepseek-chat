import streamlit as st
import requests
import json
import os
import time
from typing import Iterator

# Page config definition
st.set_page_config(
        page_title="DeepSeek Chat",
        page_icon="🤖",
        layout="wide"
    )

st.markdown("""
    <style>
        /* Hide the Streamlit header */
        header { display: none !important; }
        
        /* Hide the default hamburger menu */
        .st-emotion-cache-1wrcr25 { display: none !important; } 

        /* Hide the footer */
        footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

OLLAMA_API_BASE = "http://localhost:11434"

# def load_models() -> list[str]:
    # try:
        # with open('models.txt', 'r') as f:
            # return [line.strip() for line in f if line.strip()]
    # except FileNotFoundError:
        # return ["deepseek-r1:1.5b"]

# history file 
HISTORY_FILE = "chat_history.json"

#Tone selection
selected_tone_option_id = st.session_state.get("selected_tone_id",0) 

# save chat history at this point
def save_chat_history():
    with open(HISTORY_FILE, "w") as f:
        json.dump(st.session_state.messages, f)

def load_chat_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            st.session_state.messages = json.load(f)
    else:
        st.session_state.messages = []
        
# loading from the apis
def load_models() -> list[str]:
    response = requests.get(f"{OLLAMA_API_BASE}/api/tags")
    return [model["name"] for model in response.json()["models"]]

def generate_stream(prompt: str, model: str) -> Iterator[str]:
    response = requests.post(
        f"{OLLAMA_API_BASE}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": True
        },
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            json_response = json.loads(line)
            if 'response' in json_response:
                yield json_response['response']
            if json_response.get('done', False):
                break

def extract_thinking_and_response(text: str) -> tuple[str, str]:
    think_start = text.find("<think>")
    think_end = text.find("</think>")
    
    if think_start != -1 and think_end != -1:
        thinking = text[think_start + 7:think_end].strip()
        response = text[think_end + 8:].strip()
        return thinking, response
    
    return "", text

def get_suggested_prompts(tone: str):
    """Return a list of suggested prompts based on the selected tone."""
    prompts = {
        "Casual": [
            "What’s something I should try this weekend",
            "Tell me something random!",
            "Teach me something new!",
            "Recommend a good book 📚"
        ],
        "Formal": [
            "Explain quantum computing in simple terms.",
            "Give a brief history of the internet",
            "What are the key principles of effective leadership?",
            "Discuss the impact of AI on modern industries."
        ],
        "Sarcastic": [
            "Oh sure, tell me why Mondays are so amazing. 🙄",
            "Why is pineapple on pizza the best idea ever? 🍍🍕",
            "Explain quantum physics like I'm five... and clueless. 🧠",
            "Give me life advice in the most sarcastic way possible."
        ],
        "Minimalist": [
            "Summarize AI in one sentence.",
            "Best productivity hack?",
            "One book everyone should read?",
            "How to learn Python fast?"
        ]
    }
    return prompts.get(tone, ["Ask me anything! 😊"])  # Default if tone is missing

def main():
    
    load_chat_history()
    
    col1, col2, col3 = st.columns([3, 2, 1])

    with col2:
        option_map = {
        0: "Casual",
        1: "Formal",
        2: "Sarcastic",
        3: "Minimalist",
        }
        selection = st.pills(
            "Tone",
        options=option_map.keys(),
        format_func=lambda option: option_map[option],
        selection_mode="single",
        label_visibility="collapsed",
        default=0
        )
        st.session_state["selected_tone"] = option_map[selected_tone_option_id]

        # Check if selection has changed
        if selection != st.session_state.get("selected_tone_id"):
            st.session_state["selected_tone_id"]  = selection  # Update the session state with the new selection
            st.session_state["selected_tone"] = option_map[selection]
            st.rerun() 

    with col3:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = []
            save_chat_history()
            st.rerun()    

    with col1:
        available_models = load_models()
        selected_model = st.selectbox("Choose a model", available_models, index=0,label_visibility='collapsed',)

    # Check if a suggested prompt was selected
    if "selected_prompt" in st.session_state:
        pre_filled_prompt = st.session_state["selected_prompt"]
        del st.session_state["selected_prompt"]  # Clear it after pre-filling
    else:
        pre_filled_prompt = ""

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and "thinking" in message and message["thinking"]:
                with st.expander("Show reasoning", expanded=False):
                    st.markdown(message["thinking"])
            st.markdown(message["content"])
    
    if prompt := st.chat_input("What would you like to ask?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            # thinking_placeholder = st.empty()
            with st.spinner("🤔 Reasoning..."):
                progress_bar = st.progress(0)  # Start progress at 0%
        
                full_response = ""
                last_thinking = ""
                progress_value = 0  # Start progress at 0%
                try:
                    # with thinking_placeholder.container():
                    #     thinking_expander = st.expander("Show reasoning", expanded=False)
                    for i, response_chunk in enumerate(generate_stream(prompt, selected_model)):
                        full_response += response_chunk
                        thinking, response = extract_thinking_and_response(full_response)
                        # if thinking and thinking != last_thinking:
                        #     with thinking_expander:
                        #         st.markdown(thinking)
                        #         last_thinking = thinking
                
                        # Update progress bar dynamically
                        progress_value = (progress_value + 5) % 100  # Loops 0 → 100 → 0
                        progress_bar.progress(progress_value / 100)  # Normalize to 0.0 - 1.0
                        time.sleep(0.1)  # Smooth animation effect
                        # progress = min(1.0, i / total_chunks)
                        # progress_bar.progress(progress)  # Simulate progress
                
                        message_placeholder.markdown(response + "▌")
            
                    progress_bar.empty()  # Remove progress bar when done
                    message_placeholder.markdown(response)  # Display final response
            
                    st.session_state.messages.append({
                                "role": "assistant",
                                "content": response,
                                "thinking": thinking
                        })
                    save_chat_history()
                except requests.exceptions.RequestException:
                    st.error("Error: Could not connect to Ollama server")
                    st.info("Make sure Ollama is running and accessible at localhost:11434")
                    progress_bar.empty()  # Remove progress bar in case of error
    else :
        if pre_filled_prompt :
            prompt = pre_filled_prompt
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
            # thinking_placeholder = st.empty()
                with st.spinner("🤔 Reasoning..."):
                    progress_bar = st.progress(0)  # Start progress at 0%
        
                    full_response = ""
                    last_thinking = ""
                    progress_value = 0  # Start progress at 0%
                    try:
                        for i, response_chunk in enumerate(generate_stream(prompt, selected_model)):
                            full_response += response_chunk
                            thinking, response = extract_thinking_and_response(full_response)
                      
                            # Update progress bar dynamically
                            progress_value = (progress_value + 5) % 100  # Loops 0 → 100 → 0
                            progress_bar.progress(progress_value / 100)  # Normalize to 0.0 - 1.0
                            time.sleep(0.1)  # Smooth animation effect
                
                            message_placeholder.markdown(response + "▌")
            
                        progress_bar.empty()  # Remove progress bar when done
                        message_placeholder.markdown(response)  # Display final response
            
                        st.session_state.messages.append({
                                "role": "assistant",
                                "content": response,
                                "thinking": thinking
                        })
                        save_chat_history()
                    except requests.exceptions.RequestException:
                        st.error("Error: Could not connect to Ollama server")
                        st.info("Make sure Ollama is running and accessible at localhost:11434")
                        progress_bar.empty()  # Remove progress bar in case of error        
        


if __name__ == "__main__":
    main()

st.markdown("**💡 Try one of these prompts:**")
suggested_prompts = get_suggested_prompts(st.session_state["selected_tone"])

cols = st.columns(len(suggested_prompts))  # Create a horizontal layout
for i, prompt in enumerate(suggested_prompts):
    if cols[i].button(prompt, use_container_width=True,type="tertiary"):  
        st.session_state["selected_prompt"] = prompt
        st.rerun()  # Refresh to fill input    