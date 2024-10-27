import streamlit as st
import random

class ChatbotInterface:
    def __init__(self):
        self.animation_qna = [
            {"q": "How can AI help my business?", "a": "AI can automate customer support, analyze data, and improve efficiency."},
            {"q": "Is it easy to integrate?", "a": "Yes! Our solution integrates seamlessly with your existing systems."},
            {"q": "What makes you different?", "a": "We offer personalized solutions with advanced AI capabilities."}
        ]
        self.privacy_policy_text = """
        ### Privacy Policy
        
        1. **Information Collection**: We collect basic information necessary for service provision.
        2. **Data Usage**: Your data is used to provide and improve our chatbot services.
        3. **Data Protection**: We implement industry-standard security measures.
        4. **User Rights**: You have the right to access and control your data.
        """

    def initialize_session_state(self):
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'current_state' not in st.session_state:
            st.session_state.current_state = 'demo'
        if 'demo_count' not in st.session_state:
            st.session_state.demo_count = 0
        if 'animation_index' not in st.session_state:
            st.session_state.animation_index = 0
        if 'privacy_accepted' not in st.session_state:
            st.session_state.privacy_accepted = False
        if 'user_input' not in st.session_state:
            st.session_state.user_input = ""

    def handle_demo_input(self):
        """Handle demo chat input"""
        if st.session_state.user_input and st.session_state.demo_count < 5:
            st.session_state.messages.append({"role": "user", "content": st.session_state.user_input})
            
            bot_responses = [
                "That's an interesting point! Would you like to know more about our AI capabilities?",
                "Great question! Our AI system is designed to handle such queries efficiently.",
                "I understand your concern. Let me explain how our solution can help.",
                "Thanks for asking! This is exactly the kind of challenge our AI excels at.",
                "Excellent question! Would you like to explore this topic further in our full version?"
            ]
            bot_response = random.choice(bot_responses)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            
            st.session_state.demo_count += 1
            st.session_state.user_input = ""
            
            if st.session_state.demo_count >= 5:
                st.session_state.current_state = 'auth'
                st.rerun()

    def handle_logged_in_input(self):
        if st.session_state.user_input:
            st.session_state.messages.append({"role": "user", "content": st.session_state.user_input})
            
            bot_responses = [
                "Thank you for your message! How can I assist you further?",
                "I understand your request. Let me help you with that.",
                "That's a great question! Here's what I can tell you...",
                "I'm processing your request. Is there anything specific you'd like to know?",
                "I'm here to help! Let me address your query."
            ]
            bot_response = random.choice(bot_responses)
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            
            st.session_state.user_input = ""

    def render_left_column(self):
        st.image("C:/Users/ahmed/Downloads/bot_logo-removebg-preview.png", width=200)
        st.title("Jo3tChatbot")
        
        current_qa = self.animation_qna[st.session_state.animation_index]
        st.markdown("### Example Conversation")
        st.markdown(f"<span style='color:blue;'>You:</span> {current_qa['q']}", unsafe_allow_html=True)
        st.markdown(f"<span style='color:green;'>Bot:</span> {current_qa['a']}", unsafe_allow_html=True)
        
        st.session_state.animation_index = (st.session_state.animation_index + 1) % len(self.animation_qna)
        
        if st.button("Sign Up Now"):
            st.session_state.current_state = 'auth'
            st.rerun()

    def render_right_container(self):
        st.markdown("""
            <style>
                body { 
                    overflow: hidden; /* Prevent scrolling on the entire page */ 
                    background-color: #edebe0; /* Change background color */
                }  
                .block-container { 
                    padding-top: 80px; /* Add padding to push down content */ 
                }  
                .chat-container { 
                    max-height: 500px; 
                    overflow-y: auto; 
                    border: 1px solid #ddd; 
                    border-radius: 5px; 
                    padding: 0.5rem; 
                    background: #f9f9f9;
                }
                .chat-message {
                    margin-bottom: 0.5rem;
                    padding: 0.25rem; /* Added padding for better visibility */
                    border-radius: 4px; /* Slight rounding for messages */
                }
            </style>
        """, unsafe_allow_html=True)

        chat_container = st.container()
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            if st.session_state.current_state == 'demo':
                for msg in st.session_state.messages:
                    role = "User" if msg["role"] == "user" else "Bot"
                    color = "blue" if role == "User" else "green"
                    st.markdown(
                        f'<div class="chat-message" style="color:{color}; font-weight:bold;">{role}: {msg["content"]}</div>',
                        unsafe_allow_html=True
                    )
            elif st.session_state.current_state == 'auth':
                st.markdown("### Demo Complete! Sign up to access the full version.")
                if st.button("Sign Up"):
                    st.session_state.current_state = 'privacy_policy'
                    st.rerun()
            elif st.session_state.current_state == 'privacy_policy':
                st.markdown(self.privacy_policy_text)
                if st.checkbox("I agree to the privacy policy"):
                    st.session_state.privacy_accepted = True
                    if st.button("Continue"):
                        st.session_state.current_state = 'signup_form'
                        st.rerun()
            elif st.session_state.current_state == 'signup_form':
                with st.form("signup_form"):
                    name = st.text_input("Full Name")
                    email = st.text_input("Email Address")
                    if st.form_submit_button("Submit"):
                        st.success("Thank you for signing up!")
                        st.session_state.current_state = 'logged_in_chatbot'
                        st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

            st.text_input("Type your message:", key="user_input", on_change=self.handle_demo_input if st.session_state.current_state == 'demo' else self.handle_logged_in_input)

    def render_logged_in_chatbot(self):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("# Welcome to Jo3tChatbot")
            st.text("You are now logged in. Start chatting!")

    def render_interface(self):
        self.initialize_session_state()
        
        if st.session_state.current_state in ['demo', 'auth', 'privacy_policy', 'signup_form']:
            left_col, right_col = st.columns([1, 2])
            with left_col:
                self.render_left_column()
            with right_col:
                self.render_right_container()
        elif st.session_state.current_state == 'logged_in_chatbot':
            self.render_logged_in_chatbot()

def main():
    st.set_page_config(page_title="Jo3tChatbot", layout="wide")
    chatbot = ChatbotInterface()
    chatbot.render_interface()

if __name__ == "__main__":
    main()
