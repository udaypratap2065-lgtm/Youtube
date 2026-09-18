import streamlit as st
import yt_dlp
import os

try:
    from moviepy.editor import VideoFileClip
except ImportError:
    from moviepy.video.io.VideoFileClip import VideoFileClip

st.set_page_config(page_title="YouTube Auto-Clipper", page_icon="🎬", layout="centered")

st.title("🎬 YouTube Auto-Clipper Web App")
st.write("YouTube link paste karo, clips vertical (9:16) format mein cut hongi aur aap yahin se direct download kar sakoge!")

url = st.text_input("YouTube Video Link:")
clip_duration = st.slider("Har clip ki length (seconds mein):", 15, 60, 30)

if st.button("Process & Generate Clips"):
    if url:
        with st.spinner("Video download aur process ho rahi hai... Thoda wait karein."):
            try:
                # 1. Video Download
                ydl_opts = {
                    'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
                    'outtmpl': 'temp_video.mp4'
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # 2. Cut & Display Download Buttons
                with VideoFileClip("temp_video.mp4") as video:
                    total_duration = int(video.duration)
                    
                    for i, start in enumerate(range(0, total_duration, clip_duration)):
                        end = min(start + clip_duration, total_duration)
                        if end - start < 10:
                            break
                            
                        output_name = f"clip_{i+1}.mp4"
                        
                        # 9:16 Vertical Crop (Shorts format)
                        w, h = video.size
                        new_w = int(h * (9/16))
                        x1 = (w - new_w) // 2
                        
                        clipped = video.subclip(start, end).crop(x1=x1, y1=0, x2=x1 + new_w, y2=h)
                        clipped.write_videofile(output_name, codec="libx264", audio_codec="aac", logger=None)
                        
                        st.subheader(f"Clip {i+1} ({start}s - {end}s)")
                        st.video(output_name)
                        
                        with open(output_name, "rb") as f:
                            st.download_button(
                                label=f"📥 Download Clip {i+1}",
                                data=f,
                                file_name=output_name,
                                mime="video/mp4",
                                key=f"download_{i}"
                            )
                st.success("Sabhi clips taiyar hain, aap unhe upar se download kar sakte hain!")
            except Exception as e:
                st.error(f"Koi error aa gaya: {e}")
    else:
        st.warning("Pehle koi valid YouTube link toh daalo bhai!")
      
