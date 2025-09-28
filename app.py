import streamlit as st
import requests
import io
from PIL import Image
import time
import base64

# Configure page
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide"
)

# Hugging Face API configuration
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
# Alternative models:
# "stabilityai/stable-diffusion-2-1"
# "prompthero/openjourney"

def query_huggingface_api(payload, api_token=None):
    """Query Hugging Face Inference API"""
    headers = {}
    if api_token:
        headers["Authorization"] = f"Bearer {api_token}"
    
    response = requests.post(API_URL, headers=headers, json=payload)
    return response

def generate_image_api(prompt, api_token=None):
    """Generate image using Hugging Face API"""
    try:
        payload = {
            "inputs": prompt,
            "parameters": {
                "num_inference_steps": 20,
                "guidance_scale": 7.5,
                "width": 512,
                "height": 512
            }
        }
        
        response = query_huggingface_api(payload, api_token)
        
        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
            return image, None
        elif response.status_code == 503:
            return None, "Model is loading, please wait a few minutes and try again."
        else:
            try:
                error_msg = response.json().get('error', 'Unknown error')
                return None, f"Error: {error_msg}"
            except:
                return None, f"HTTP Error: {response.status_code}"
                
    except Exception as e:
        return None, f"Request failed: {str(e)}"

# Main app
def main():
    # Header
    st.title("🎨 AI Image Generator")
    st.subheader("สร้างภาพสวยๆ ด้วย AI จาก Text Prompt")
    
    # API Token input (optional)
    with st.sidebar:
        st.header("⚙️ Settings")
        st.info("💡 ใช้ Hugging Face API - รวดเร็วและไม่กิน memory")
        
        api_token = st.text_input(
            "🔑 Hugging Face API Token (Optional)", 
            type="password",
            help="ใส่ token เพื่อการใช้งานที่เร็วขึ้น และไม่มี rate limit"
        )
        
        if st.button("🔗 Get Free API Token"):
            st.markdown("[สมัครฟรีที่ Hugging Face](https://huggingface.co/settings/tokens)")
        
        st.markdown("---")
        st.markdown("**ข้อดีของการใช้ API:**")
        st.markdown("✅ ไม่กิน memory ของ server")
        st.markdown("✅ รวดเร็วกว่า")
        st.markdown("✅ ไม่ต้องรอโหลด model")
        st.markdown("✅ Stable และเชื่อถือได้")
    
    # Main interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Input")
        
        # Text input
        prompt = st.text_area(
            "Enter your prompt:",
            value="a beautiful cat sitting in a garden, digital art, high quality",
            height=100,
            help="อธิบายภาพที่คุณต้องการให้ AI สร้าง"
        )
        
        # Quality settings
        st.subheader("🎯 Quality Settings")
        
        col_a, col_b = st.columns(2)
        with col_a:
            add_quality = st.checkbox("✨ Auto enhance quality", value=True)
        with col_b:
            add_style = st.selectbox(
                "🎨 Art Style",
                ["None", "digital art", "realistic", "cartoon", "anime", "oil painting", "watercolor"]
            )
        
        # Generate button
        generate_btn = st.button("🚀 Generate Image", type="primary", use_container_width=True)
        
        # Example prompts
        st.subheader("💡 Example Prompts")
        example_prompts = [
            "beautiful sunset over mountains, digital art",
            "cute cartoon robot, colorful, high quality",
            "professional headshot, business attire, clean background",
            "fantasy landscape, magical forest, detailed",
            "modern city skyline at night, cinematic",
            "abstract geometric art, vibrant colors",
            "vintage car in retro style, detailed",
            "space astronaut, cosmic background, realistic"
        ]
        
        for i, example in enumerate(example_prompts):
            if st.button(f"📋 {example[:40]}...", key=f"example_{i}"):
                st.session_state.selected_prompt = example
                st.rerun()
        
        # Use example prompt if selected
        if 'selected_prompt' in st.session_state:
            prompt = st.session_state.selected_prompt
            del st.session_state.selected_prompt
    
    with col2:
        st.header("🖼️ Generated Image")
        
        if generate_btn and prompt:
            if len(prompt.strip()) < 3:
                st.warning("กรุณาใส่ prompt ที่ยาวกว่า 3 ตัวอักษร")
            else:
                # Enhance prompt
                enhanced_prompt = prompt
                
                if add_quality:
                    enhanced_prompt += ", high quality, detailed, beautiful"
                
                if add_style != "None":
                    enhanced_prompt += f", {add_style}"
                
                # Show enhanced prompt
                with st.expander("🔍 Enhanced Prompt"):
                    st.code(enhanced_prompt)
                
                with st.spinner("กำลังสร้างภาพ... (15-30 วินาที)"):
                    start_time = time.time()
                    
                    # Progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i in range(100):
                        progress_bar.progress(i + 1)
                        if i < 30:
                            status_text.text("🚀 กำลังส่ง request...")
                        elif i < 70:
                            status_text.text("🎨 AI กำลังสร้างภาพ...")
                        else:
                            status_text.text("✨ เกือบเสร็จแล้ว...")
                        time.sleep(0.1)
                    
                    # Generate image
                    image, error = generate_image_api(enhanced_prompt, api_token if api_token else None)
                    
                    progress_bar.empty()
                    status_text.empty()
                    end_time = time.time()
                    generation_time = end_time - start_time
                
                if image:
                    st.image(image, caption=f"Prompt: {prompt}", use_column_width=True)
                    st.success(f"✨ สร้างภาพเสร็จแล้ว! (ใช้เวลา {generation_time:.1f} วินาที)")
                    
                    # Image info
                    st.info(f"📏 ขนาด: {image.size[0]}x{image.size[1]} pixels")
                    
                    # Download button
                    img_buffer = io.BytesIO()
                    image.save(img_buffer, format='PNG')
                    img_buffer.seek(0)
                    
                    st.download_button(
                        label="💾 Download Image",
                        data=img_buffer,
                        file_name=f"ai_generated_{int(time.time())}.png",
                        mime="image/png",
                        use_container_width=True
                    )
                    
                    # Store in session state
                    st.session_state.last_image = image
                    st.session_state.last_prompt = prompt
                    
                elif error:
                    st.error(f"❌ {error}")
                    
                    if "loading" in error.lower():
                        st.info("💡 Model กำลังโหลด รอ 2-3 นาทีแล้วลองใหม่")
                    elif "rate limit" in error.lower() or "quota" in error.lower():
                        st.warning("⚠️ Rate limit exceeded. ใช้ API token หรือรอสักครู่")
                    else:
                        st.info("💡 ลองปรับ prompt หรือลองใหม่ในอีกสักครู่")
        
        elif 'last_image' in st.session_state:
            # Show last generated image
            st.image(
                st.session_state.last_image, 
                caption=f"Last generated: {st.session_state.last_prompt}", 
                use_column_width=True
            )
        else:
            st.info("👆 ใส่ prompt และกด Generate เพื่อสร้างภาพ")
            
            # Sample image
            st.image(
                "https://via.placeholder.com/512x512/f0f0f0/cccccc?text=Your+AI+Generated+Image+Will+Appear+Here", 
                caption="รอการสร้างภาพ...", 
                use_column_width=True
            )
    
    # Tips section
    with st.expander("💡 Tips สำหรับ Prompt ที่ดี"):
        st.markdown("""
        **เทคนิคการเขียน Prompt:**
        - ใช้คำอธิบายที่ชัดเจน: "red sports car" แทน "car"
        - เพิ่มคำคุณภาพ: "high quality", "detailed", "beautiful"
        - ระบุสไตล์: "digital art", "realistic", "cartoon"
        - เพิ่มอารมณ์: "cheerful", "mysterious", "dramatic"
        - ระบุแสง: "bright lighting", "sunset", "dramatic shadows"
        
        **ตัวอย่างการปรับปรุง:**
        - ❌ "cat"
        - ✅ "cute orange cat sitting in sunny garden, digital art, high quality"
        """)
    
    # Technical info
    with st.expander("🔧 Technical Information"):
        st.markdown(f"""
        - **API Endpoint**: Hugging Face Inference API
        - **Model**: runwayml/stable-diffusion-v1-5
        - **Resolution**: 512x512 pixels
        - **Inference Steps**: 20 (optimized for speed)
        - **Status**: {"🟢 API Token Connected" if api_token else "🟡 Using Free Tier"}
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🤖 Powered by <strong>Hugging Face</strong> | ⚡ API-based for better performance</p>
        <p>💡 <strong>Tip:</strong> ใช้ API token เพื่อความเร็วและไม่มี rate limit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
