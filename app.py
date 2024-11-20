import streamlit as st
from openai import OpenAI
from pytubefix import YouTube

def get_caption_text(url: str) -> str:
    """Extract caption text from a YouTube short URL"""
    try:
        yt = YouTube(url)
        caption = yt.captions['a.en']
        return caption.generate_srt_captions()
    except Exception as e:
        st.error(f"Error getting captions: {str(e)}")
        return None


def summarise_video(caption_text: str) -> str:
    prompt = f"""You are a helpful assistant that summarises YouTube shorts.
    Here's the caption text:
    {caption_text}
    
    Please provide a clear, well-structured summary of the main points discussed in the video.
    Format your response in md syntax. Highlight the most important words, phrases and sentences in the body of the summary."""
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarises YouTube video content."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2500,  # Adjust as needed to get close to 500 words
        n=1,
        temperature=0.1,
    )

    return response.choices[0].message.content.strip()

def main():
    st.title("YouTube Video Summariser 🍀")
    st.write("Enter a YouTube Video URL to get an AI summary of the content! 🤖")

    # Input field for YouTube URL
    url = st.text_input("Enter YouTube Video URL:")

    if st.button("🎯 Generate Summary"):
        if url:
            with st.spinner("📝 Getting video captions..."):
                caption_text = get_caption_text(url)
                
            if caption_text:
                with st.spinner("Generating summary..."):
                    try:
                        summary = summarise_video(caption_text)
                        st.markdown("### Summary")
                        st.markdown(summary)
                    except Exception as e:
                        st.error(f"Error generating summary: {str(e)}")
        else:
            st.warning("Please enter a YouTube Shorts URL")

if __name__ == "__main__":
    main() 