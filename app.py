import streamlit as st
import requests
import io
from PIL import Image
import time

# Configure page
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide"
)

# Use free API without token
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

def generate_image_free(prompt):
    """Generate image using free API (no token needed)"""
    headers = {"Content-Type": "application/json"}
    payload = {"inputs": prompt}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        
        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
            return image, None
        elif response.status_code == 503:
            return None, "🕐 Model is loading. Please wait 2-3 minutes and try again."
        elif response.status_code == 429:
            return None, "⚠️ Too many requests. Please wait 10-15 minutes before trying again."
        elif response.status_code == 401:
            return None, "🔒 Authentication error. Using free tier instead."
        else:
            try:
                error_data = response.json()
                error_msg = error_data.get('error', f'HTTP {response.status_code}')
                return None, f"❌ {error_msg}"
            except:
                return None, f"❌ Error {response.status_code}. Please try again later."
                
    except requests.exceptions.Timeout:
        return None, "⏰ Request timeout. The model might be slow. Try again."
    except Exception as e:
        return None, f"❌ Connection error: {str(e)}"

def main():
    # Header
    st.title("🎨 AI Image Generator")
    st.subheader("สร้างภาพสวยๆ ด้วย AI จาก Text Prompt")
    
    # Info banner
    st.info("🆓 **Free Version** - Using Hugging Face free API (no token required)")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        st.info("🤖 Stable Diffusion v1.5 (Free Tier)")
        
        st.markdown("**Free Tier Limitations:**")
        st.markdown("⏱️ Slower processing (1-2 minutes)")
        st.markdown("🔄 Limited requests per hour")
        st.markdown("⏳ May need to wait if busy")
        
        st.markdown("---")
        st.markdown("**Status:**")
        st.markdown("✅ No token required")
        st.markdown("✅ No server memory usage")
        st.markdown("✅ Works for everyone")
        
        # Wait time info
        st.markdown("---")
        st.markdown("**💡 Tips for Free Tier:**")
        st.markdown("• Be patient - may take 1-3 minutes")
        st.markdown("• Try during off-peak hours")
        st.markdown("• Use simple, clear prompts")
        st.markdown("• Wait between requests")
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Input")
        
        prompt = st.text_area(
            "Enter your prompt:",
            value="a beautiful cat sitting in a garden, digital art",
            height=100,
            help="Describe the image you want to create"
        )
        
        # Generate button
        if st.button("🚀 Generate Image (Free)", type="primary", use_container_width=True):
            if len(prompt.strip()) < 3:
                st.error("Please enter a prompt with at least 3 characters")
            else:
                st.session_state.generate_now = True
                st.session_state.current_prompt = prompt
                st.rerun()
        
        # Example prompts
        st.subheader("💡 Try These Prompts")
        examples = [
            "beautiful sunset over mountains",
            "cute cartoon cat with blue eyes",
            "modern city at night",
            "peaceful forest landscape",
            "colorful abstract art",
            "vintage bicycle in garden",
            "fantasy castle on hill",
            "space astronaut floating"
        ]
        
        for i, example in enumerate(examples):
            if st.button(f"📝 {example}", key=f"ex_{i}"):
                st.session_state.example_prompt = example
                st.rerun()
        
        if 'example_prompt' in st.session_state:
            prompt = st.session_state.example_prompt
            del st.session_state.example_prompt
            st.rerun()
    
    with col2:
        st.header("🖼️ Generated Image")
        
        # Handle generation
        if st.session_state.get('generate_now', False):
            st.session_state.generate_now = False
            
            current_prompt = st.session_state.get('current_prompt', prompt)
            
            # Enhanced prompt for better results
            enhanced_prompt = f"{current_prompt}, high quality, detailed"
            
            with st.expander("🔍 Enhanced prompt:"):
                st.code(enhanced_prompt)
            
            # Generate with longer progress bar for free tier
            with st.spinner("🎨 Generating your image... This may take 1-3 minutes on free tier"):
                progress = st.progress(0)
                status = st.empty()
                
                # Longer progress simulation for free tier
                for i in range(120):
                    progress.progress(min(i + 1, 100))
                    if i < 20:
                        status.text("📡 Connecting to Hugging Face...")
                    elif i < 40:
                        status.text("🕐 Waiting in queue...")
                    elif i < 80:
                        status.text("🎨 AI is creating your image...")
                    elif i < 100:
                        status.text("✨ Finalizing...")
                    else:
                        status.text("⏳ Almost ready...")
                    time.sleep(0.5)  # Slower for free tier
                
                # Actual generation
                image, error = generate_image_free(enhanced_prompt)
                
                progress.empty()
                status.empty()
            
            if image:
                st.image(image, caption=f"Generated: {current_prompt}", use_column_width=True)
                st.success("✅ Image generated successfully!")
                
                # Download
                buf = io.BytesIO()
                image.save(buf, format='PNG')
                buf.seek(0)
                
                st.download_button(
                    "💾 Download Image",
                    data=buf,
                    file_name=f"ai_generated_{int(time.time())}.png",
                    mime="image/png",
                    use_container_width=True
                )
                
                st.session_state.last_image = image
                st.session_state.last_prompt = current_prompt
                
            else:
                st.error(error if error else "Failed to generate image")
                
                # Specific suggestions for free tier
                if "loading" in str(error).lower():
                    st.info("💡 Model is starting up. Wait 2-3 minutes and try again.")
                    st.info("🕐 Free tier models sleep when not used and take time to wake up.")
                elif "requests" in str(error).lower():
                    st.info("💡 Free tier has hourly limits. Try again in 10-15 minutes.")
                    st.info("⏰ Peak hours (9 AM - 6 PM UTC) are busiest.")
                else:
                    st.info("💡 Try a simpler prompt or wait a few minutes.")
                    st.info("🔄 Free tier can be unpredictable during busy times.")
        
        elif 'last_image' in st.session_state:
            st.image(
                st.session_state.last_image,
                caption=f"Last: {st.session_state.last_prompt}",
                use_column_width=True
            )
        else:
            st.info("👆 Enter a prompt and click 'Generate Image'")
            st.image(
                "https://via.placeholder.com/512x512/e8f4f8/2c5282?text=Free+AI+Image+Generator",
                caption="Your AI-generated image will appear here",
                use_column_width=True
            )
    
    # Tips for free tier
    with st.expander("💡 Free Tier Tips & Troubleshooting"):
        st.markdown("""
        **🕐 If generation is slow or fails:**
        - **Model Loading**: Wait 2-3 minutes if you see "Model is loading"
        - **Rate Limits**: Free tier has hourly limits, try again later
        - **Peak Hours**: Avoid 9 AM - 6 PM UTC for faster response
        - **Simple Prompts**: Use clear, simple descriptions for better success
        
        **✅ Best practices for free tier:**
        - Use during off-peak hours (evenings/weekends)
        - Keep prompts under 50 words
        - Wait at least 1 minute between requests
        - Be patient - free tier prioritizes paid users
        
        **🎯 Good prompt examples:**
        - "cat in garden" ✅ Simple and clear
        - "beautiful landscape" ✅ Basic but effective  
        - "cute cartoon robot" ✅ Specific but not complex
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "<p>🆓 <strong>Free AI Image Generator</strong> using Hugging Face</p>"
        "<p>⚡ No registration required | No token needed | Just pure AI magic!</p>"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    if 'generate_now' not in st.session_state:
        st.session_state.generate_now = False
    
    main()
