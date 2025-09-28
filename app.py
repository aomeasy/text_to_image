import streamlit as st
import torch
from diffusers import DiffusionPipeline
from PIL import Image
import io
import time
import os

# Configure page
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide"
)

# Use smaller, faster model for Streamlit Cloud
MODEL_ID = "stabilityai/stable-diffusion-2-1-base"  # Smaller than openjourney
# Alternative lighter models:
# "runwayml/stable-diffusion-v1-5"
# "CompVis/stable-diffusion-v1-4"

@st.cache_resource
def load_model():
    """Load and cache the Stable Diffusion model with optimization for Streamlit Cloud"""
    try:
        # Force CPU usage for Streamlit Cloud compatibility
        device = "cpu"
        torch_dtype = torch.float32
        
        # Use low memory mode and optimizations
        pipe = DiffusionPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=torch_dtype,
            safety_checker=None,
            requires_safety_checker=False,
            low_cpu_mem_usage=True,
            use_auth_token=False
        )
        
        # Enable memory efficient attention
        pipe.enable_attention_slicing()
        
        # Move to CPU
        pipe = pipe.to(device)
        
        return pipe, device
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None

def generate_image(pipe, prompt, num_inference_steps=20, guidance_scale=7.5, width=512, height=512):
    """Generate image with memory optimization"""
    try:
        # Lower settings for Streamlit Cloud
        if width > 512 or height > 512:
            width, height = 512, 512
        
        if num_inference_steps > 30:
            num_inference_steps = 30
            
        # Generate with optimizations
        with torch.no_grad():
            image = pipe(
                prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                width=width,
                height=height,
                generator=torch.Generator().manual_seed(42)  # For reproducibility
            ).images[0]
        
        return image
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None

# Main app
def main():
    # Header
    st.title("🎨 AI Image Generator")
    st.subheader("สร้างภาพสวยๆ ด้วย AI จาก Text Prompt")
    
    # Warning for Streamlit Cloud limitations
    st.warning("⚠️ รันบน Streamlit Cloud: การสร้างภาพอาจใช้เวลา 2-5 นาที และอาจมี memory limitations")
    
    # Sidebar for settings
    st.sidebar.header("⚙️ Settings")
    st.sidebar.info("💡 ใช้ prompt ภาษาอังกฤษสำหรับผลลัพธ์ที่ดีที่สุด")
    
    # Model loading with better error handling
    if 'model_loaded' not in st.session_state:
        st.session_state.model_loaded = False
        st.session_state.pipe = None
        st.session_state.device = None
    
    if not st.session_state.model_loaded:
        with st.spinner("กำลังโหลด AI Model... (อาจใช้เวลา 2-3 นาที)"):
            pipe, device = load_model()
            if pipe is not None:
                st.session_state.pipe = pipe
                st.session_state.device = device
                st.session_state.model_loaded = True
                st.success(f"✅ Model โหลดเสร็จแล้ว (Device: {device})")
                st.rerun()
            else:
                st.error("❌ ไม่สามารถโหลด Model ได้ กรุณา refresh หน้าเว็บ")
                st.stop()
    
    # Main interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Input")
        
        # Text input
        prompt = st.text_area(
            "Enter your prompt (English recommended):",
            value="a beautiful cat sitting in a garden, digital art",
            height=80,
            help="อธิบายภาพที่คุณต้องการให้ AI สร้าง (ภาษาอังกฤษแนะนำ)"
        )
        
        # Simplified settings for Streamlit Cloud
        st.subheader("🔧 Settings")
        num_steps = st.slider(
            "Quality (inference steps)", 
            10, 30, 20, 5,
            help="ขั้นตอนการสร้าง: มากขึ้น = คุณภาพดีขึ้น แต่ช้าขึ้น"
        )
        guidance_scale = st.slider(
            "Prompt strength", 
            5.0, 15.0, 7.5, 0.5,
            help="ความแม่นยำตาม prompt"
        )
        
        # Fixed size for Streamlit Cloud
        st.info("📏 ขนาดภาพ: 512x512 (ปรับให้เหมาะกับ Streamlit Cloud)")
        
        # Generate button
        generate_btn = st.button(
            "🚀 Generate Image", 
            type="primary", 
            use_container_width=True,
            disabled=not st.session_state.model_loaded
        )
        
        # Example prompts
        st.subheader("💡 Example Prompts")
        example_prompts = [
            "a beautiful sunset over mountains, digital art",
            "cute cartoon robot, colorful, digital art",
            "peaceful forest with river, nature photography",
            "modern city skyline at night, urban photography",
            "abstract geometric patterns, vibrant colors"
        ]
        
        for i, example in enumerate(example_prompts):
            if st.button(f"📋 {example}", key=f"example_{i}"):
                st.session_state.selected_prompt = example
                st.rerun()
        
        # Use example prompt if selected
        if 'selected_prompt' in st.session_state:
            prompt = st.session_state.selected_prompt
            del st.session_state.selected_prompt
    
    with col2:
        st.header("🖼️ Generated Image")
        
        if generate_btn and prompt and st.session_state.model_loaded:
            if len(prompt.strip()) < 3:
                st.warning("กรุณาใส่ prompt ที่ยาวกว่า 3 ตัวอักษร")
            else:
                with st.spinner(f"กำลังสร้างภาพ... (ประมาณ {num_steps * 3}-{num_steps * 5} วินาที)"):
                    start_time = time.time()
                    
                    # Progress indicator
                    progress_container = st.empty()
                    for i in range(20):
                        progress_container.text(f"กำลังประมวลผล... {i*5}%")
                        time.sleep(0.1)
                    
                    image = generate_image(
                        st.session_state.pipe, 
                        prompt, 
                        num_inference_steps=num_steps,
                        guidance_scale=guidance_scale,
                        width=512,
                        height=512
                    )
                    
                    progress_container.empty()
                    end_time = time.time()
                    generation_time = end_time - start_time
                
                if image:
                    st.image(image, caption=f"Prompt: {prompt}", use_column_width=True)
                    st.success(f"✨ สร้างภาพเสร็จแล้ว! (ใช้เวลา {generation_time:.1f} วินาที)")
                    
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
                    st.session_state.last_generated_image = image
                    st.session_state.last_prompt = prompt
                else:
                    st.error("❌ เกิดข้อผิดพลาดในการสร้างภาพ กรุณาลองใหม่อีกครั้ง")
        
        elif 'last_generated_image' in st.session_state:
            # Show last generated image
            st.image(
                st.session_state.last_generated_image, 
                caption=f"Last generated: {st.session_state.last_prompt}", 
                use_column_width=True
            )
        else:
            st.info("👆 ใส่ prompt และกด Generate เพื่อสร้างภาพ")
            st.image(
                "https://via.placeholder.com/512x512/f0f0f0/cccccc?text=Your+AI+Image+Here", 
                caption="รอการสร้างภาพ...", 
                use_column_width=True
            )
    
    # Technical info
    with st.expander("🔧 Technical Information"):
        st.markdown(f"""
        - **Model**: {MODEL_ID}
        - **Device**: {st.session_state.device if st.session_state.model_loaded else 'Not loaded'}
        - **Memory Optimization**: Enabled
        - **Max Resolution**: 512x512 (optimized for Streamlit Cloud)
        - **Recommended Steps**: 15-25 for balance of speed/quality
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🤖 Powered by <strong>Stable Diffusion</strong> | Optimized for Streamlit Cloud</p>
        <p>⚡ <strong>Note:</strong> รันบน Streamlit Cloud อาจช้ากว่าเครื่อง local</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
