import streamlit as st
import openai
import ell
from pytubefix import YouTube

# Set up OpenAI client with Streamlit secrets
client = openai.Client(api_key=st.secrets["OPENAI_API_KEY"])

def get_caption_text(url: str) -> str:
    """Extract caption text from a YouTube short URL"""
    try:
        yt = YouTube(url)
        caption = yt.captions['a.en']
        return caption.generate_srt_captions()
    except Exception as e:
        st.error(f"Error getting captions: {str(e)}")
        return None

@ell.simple(model="gpt-4o-mini", client=client)
def summarise_short(caption_text: str) -> str:
    """Generate a summary of the YouTube short using OpenAI"""
    return f"""You are a helpful assistant that summarises YouTube shorts.
    Here's the caption text:
    {caption_text}
    
    Please provide a clear, well-structured summary of the main points discussed in the video."""

def main():
    st.title("YouTube Video Summariser")
    st.write("Enter a YouTube Video URL to get an AI summary of the content!")

    # Input field for YouTube URL
    url = st.text_input("Enter YouTube Video URL:")

    if st.button("Generate Summary"):
        if url:
            with st.spinner("Getting video captions..."):
                caption_text = get_caption_text(url)
                
            if caption_text:
                with st.spinner("Generating summary..."):
                    try:
                        summary = summarise_short(caption_text)
                        st.markdown("### Summary")
                        st.markdown(summary)
                    except Exception as e:
                        st.error(f"Error generating summary: {str(e)}")
        else:
            st.warning("Please enter a YouTube Shorts URL")

if __name__ == "__main__":
    main() 