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

# Simple, working model that's always available
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

def generate_image_simple(prompt, api_token=None):
    """Simple image generation that works"""
    headers = {"Content-Type": "application/json"}
    if api_token:
        headers["Authorization"] = f"Bearer {api_token}"
    
    payload = {"inputs": prompt}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
            return image, None
        elif response.status_code == 503:
            return None, "🕐 Model is loading. Please wait 1-2 minutes and try again."
        elif response.status_code == 429:
            return None, "⚠️ Too many requests. Please wait a moment or use API token."
        else:
            return None, f"❌ Error {response.status_code}. Try again in a few minutes."
    except requests.exceptions.Timeout:
        return None, "⏰ Request timeout. Please try again."
    except Exception as e:
        return None, f"❌ Network error: {str(e)}"

def main():
    # Header
    st.title("🎨 AI Image Generator")
    st.subheader("สร้างภาพสวยๆ ด้วย AI จาก Text Prompt")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        st.info("🤖 Using Stable Diffusion v1.5")
        
        api_token = st.text_input(
            "🔑 API Token (Optional)", 
            type="password",
            help="Paste your Hugging Face token here"
        )
        
        if st.button("🔗 Get API Token"):
            st.markdown("[Get free token](https://huggingface.co/settings/tokens)")
        
        st.markdown("---")
        st.markdown("**Status:**")
        st.markdown("✅ Fast API-based generation")
        st.markdown("✅ No server memory usage")
        st.markdown("✅ Reliable and stable")
    
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
        
        # Simple quality enhancement
        enhance_quality = st.checkbox("✨ Enhance prompt automatically", value=True)
        
        # Generate button
        if st.button("🚀 Generate Image", type="primary", use_container_width=True):
            if len(prompt.strip()) < 3:
                st.error("Please enter a prompt with at least 3 characters")
            else:
                # Store in session state to trigger generation
                st.session_state.generate_request = True
                st.session_state.current_prompt = prompt
                st.session_state.enhance_quality = enhance_quality
                st.rerun()
        
        # Example prompts
        st.subheader("💡 Try These Prompts")
        examples = [
            "beautiful landscape with mountains and trees",
            "cute cartoon robot with colorful design",
            "professional business portrait, modern style",
            "fantasy castle in magical forest",
            "modern city skyline at sunset",
            "abstract art with vibrant colors"
        ]
        
        for i, example in enumerate(examples):
            if st.button(f"📝 {example[:35]}...", key=f"ex_{i}"):
                st.session_state.selected_example = example
                st.rerun()
        
        # Apply selected example
        if 'selected_example' in st.session_state:
            prompt = st.session_state.selected_example
            del st.session_state.selected_example
            st.rerun()
    
    with col2:
        st.header("🖼️ Generated Image")
        
        # Handle generation request
        if st.session_state.get('generate_request', False):
            st.session_state.generate_request = False
            
            current_prompt = st.session_state.get('current_prompt', prompt)
            enhance = st.session_state.get('enhance_quality', True)
            
            # Enhance prompt if requested
            if enhance:
                enhanced_prompt = f"{current_prompt}, high quality, detailed, beautiful"
            else:
                enhanced_prompt = current_prompt
            
            # Show what we're generating
            with st.expander("🔍 Generating with prompt:"):
                st.code(enhanced_prompt)
            
            # Generate image
            with st.spinner("🎨 Creating your image... (30-60 seconds)"):
                progress = st.progress(0)
                status = st.empty()
                
                # Simulate progress
                for i in range(100):
                    progress.progress(i + 1)
                    if i < 20:
                        status.text("📡 Sending request...")
                    elif i < 80:
                        status.text("🎨 AI is creating your image...")
                    else:
                        status.text("✨ Almost done...")
                    time.sleep(0.2)
                
                # Actual generation
                image, error = generate_image_simple(enhanced_prompt, api_token)
                
                progress.empty()
                status.empty()
            
            if image:
                st.image(image, caption=f"Generated: {current_prompt}", use_column_width=True)
                st.success("✅ Image generated successfully!")
                
                # Download button
                buf = io.BytesIO()
                image.save(buf, format='PNG')
                buf.seek(0)
                
                st.download_button(
                    "💾 Download Image",
                    data=buf,
                    file_name=f"ai_image_{int(time.time())}.png",
                    mime="image/png",
                    use_container_width=True
                )
                
                # Store for persistence
                st.session_state.last_image = image
                st.session_state.last_prompt = current_prompt
                
            else:
                st.error(error if error else "Failed to generate image")
                
                # Helpful suggestions
                if "loading" in str(error).lower():
                    st.info("💡 The AI model is starting up. Please wait 2-3 minutes and try again.")
                elif "requests" in str(error).lower():
                    st.info("💡 Try using an API token for unlimited generations.")
                else:
                    st.info("💡 Try a simpler prompt or wait a moment before trying again.")
        
        # Show last generated image if available
        elif 'last_image' in st.session_state:
            st.image(
                st.session_state.last_image, 
                caption=f"Last generated: {st.session_state.last_prompt}", 
                use_column_width=True
            )
        else:
            st.info("👆 Enter a prompt above and click 'Generate Image'")
            st.image(
                "https://via.placeholder.com/512x512/f0f0f0/cccccc?text=Your+AI+Image+Here",
                caption="Your generated image will appear here",
                use_column_width=True
            )
    
    # Tips
    with st.expander("💡 Tips for Better Results"):
        st.markdown("""
        **Good prompt examples:**
        - "Beautiful sunset over ocean waves, digital art"
        - "Cute cartoon cat wearing glasses, colorful"
        - "Modern architecture building, minimalist design"
        - "Fantasy dragon in mystical forest, detailed"
        
        **Tips:**
        - Be specific about what you want
        - Add style keywords like "digital art", "realistic", "cartoon"
        - Include quality words like "detailed", "beautiful", "high quality"
        - Describe colors, lighting, and mood
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "<p>🤖 Powered by Stable Diffusion via Hugging Face API</p>"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    # Initialize session state
    if 'generate_request' not in st.session_state:
        st.session_state.generate_request = False
    
    main()
