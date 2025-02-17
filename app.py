# Cell 1: Setup
import streamlit as st
from openai import OpenAI
import os
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator import Authenticate  # Explicitly import Authenticate

# Load configuration from YAML file
with open('config.yaml') as file:  # Use correct relative path
    config = yaml.load(file, Loader=SafeLoader)

# Create the authenticator
authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
authenticator.login(location='sidebar')


if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar')
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')

    # Get your OpenAI API key from environment variables 
    api_key = os.getenv("OPENAI_API_KEY") 
    client = OpenAI(api_key=api_key)

    # Cell 2: Title & Description
    st.title('🤖 AI Content Assistant')
    st.markdown('I was made to help you craft interesting Social media posts.')

    # Cell 3: Function to generate text using OpenAI
    def analyze_text(text):
        if not api_key:
            st.error("OpenAI API key is not set. Please set it in your environment variables.")
            return
        
        client = OpenAI(api_key=api_key)
        model = "gpt-4o"  # Using the GPT-3.5 model

        # Instructions for the AI (adjust if needed)
        messages = [
            {"role": "system", "content": "You are an assistant who helps craft social media posts."},
            {"role": "user", "content": f"Please help me write a social media post based on the following:\n{text}"}
        ]

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0  # Lower temperature for less random responses
        )
        return response.choices[0].message.content


    # Cell 4: Function to generate the image
    def generate_image(text):
        if not api_key:
            st.error("OpenAI API key is not set. Please set it in your environment variables.")
            return

        response = client.images.generate(
            model="dall-e-3",
            prompt=text,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        # Assuming the API returns an image URL; adjust based on actual response structure
        return response.data[0].url

    # Cell 4: Streamlit UI 
    # Ensure session state variable exists
    if "image_generated" not in st.session_state:
        st.session_state.image_generated = False  # Default to False

    user_input = st.text_area("Enter a brief for your post:", "How should you maintain a deployed model?")

    if st.button('Generate Post Content'):
        with st.spinner('Generating Text...'):
            post_text = analyze_text(user_input)
            st.write(post_text)

        with st.spinner('Generating Thumbnail...'):
            thumbnail_url = generate_image(user_input)  # Consider adjusting the prompt for image generation if needed
            st.image(thumbnail_url, caption='Generated Thumbnail')
            # ✅ Update session state **AFTER** image is generated
        st.session_state.image_generated = True

    # ✅ Show feedback **only after the image has been displayed**
    if st.session_state.image_generated:
        st.write("### Feedback")

        # Feedback selection
        feedback = st.radio("Did you find this helpful?", ["👍 Thumbs Up", "👎 Thumbs Down"], index=None)

        # Show confirmation message based on feedback
        if feedback == "👍 Thumbs Up":
            st.success("Thank you for your positive feedback! ✅")
        elif feedback == "👎 Thumbs Down":
            st.error("Sorry to hear that! We'll improve. ❌")
        
elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
