import streamlit as st
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import io
import time

# Configure page
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide"
)

# Cache the model loading to avoid reloading on every run
@st.cache_resource
def load_model():
    """Load and cache the Stable Diffusion model"""
    try:
        model_id = "prompthero/openjourney"
        
        # Check if CUDA is available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if device == "cuda" else torch.float32
        
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id, 
            torch_dtype=torch_dtype,
            safety_checker=None,
            requires_safety_checker=False
        )
        pipe = pipe.to(device)
        
        return pipe, device
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None

def generate_image(pipe, prompt, num_inference_steps=50, guidance_scale=7.5, width=512, height=512):
    """Generate image from text prompt"""
    try:
        with torch.autocast("cuda" if torch.cuda.is_available() else "cpu"):
            image = pipe(
                prompt,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                width=width,
                height=height
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
    
    # Sidebar for settings
    st.sidebar.header("⚙️ Settings")
    st.sidebar.info("💡 เพิ่ม 'mdjrny-v4 style' ใน prompt เพื่อผลลัพธ์ที่ดีขึ้น")
    
    # Model loading
    with st.spinner("กำลังโหลด AI Model..."):
        pipe, device = load_model()
    
    if pipe is None:
        st.error("ไม่สามารถโหลด Model ได้ กรุณาลองใหม่อีกครั้ง")
        return
    
    st.success(f"✅ Model โหลดเสร็จแล้ว (Device: {device})")
    
    # Main interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Input")
        
        # Text input
        prompt = st.text_area(
            "Enter your prompt:",
            value="retro serie of different cars with different colors and shapes, mdjrny-v4 style",
            height=100,
            help="อธิบายภาพที่คุณต้องการให้ AI สร้าง"
        )
        
        # Advanced settings
        with st.expander("🔧 Advanced Settings"):
            num_steps = st.slider("Number of inference steps", 20, 100, 50, 10)
            guidance_scale = st.slider("Guidance scale", 1.0, 20.0, 7.5, 0.5)
            
            col_w, col_h = st.columns(2)
            with col_w:
                width = st.selectbox("Width", [256, 512, 768, 1024], index=1)
            with col_h:
                height = st.selectbox("Height", [256, 512, 768, 1024], index=1)
        
        # Generate button
        generate_btn = st.button("🚀 Generate Image", type="primary", use_container_width=True)
        
        # Example prompts
        st.subheader("💡 Example Prompts")
        example_prompts = [
            "beautiful landscape with mountains and lake, mdjrny-v4 style",
            "cute cartoon cat wearing sunglasses, mdjrny-v4 style",
            "futuristic city at sunset, mdjrny-v4 style",
            "delicious pizza with lots of toppings, mdjrny-v4 style",
            "space astronaut floating in colorful nebula, mdjrny-v4 style"
        ]
        
        for i, example in enumerate(example_prompts):
            if st.button(f"📋 {example[:50]}...", key=f"example_{i}"):
                st.session_state.example_prompt = example
                st.rerun()
        
        # Use example prompt if clicked
        if 'example_prompt' in st.session_state:
            prompt = st.session_state.example_prompt
            del st.session_state.example_prompt
    
    with col2:
        st.header("🖼️ Generated Image")
        
        if generate_btn and prompt:
            if len(prompt.strip()) < 3:
                st.warning("กรุณาใส่ prompt ที่ยาวกว่า 3 ตัวอักษร")
            else:
                with st.spinner(f"กำลังสร้างภาพ... (ใช้เวลาประมาณ {num_steps//10}-{num_steps//5} วินาที)"):
                    start_time = time.time()
                    
                    # Add progress bar
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    image = generate_image(
                        pipe, 
                        prompt, 
                        num_inference_steps=num_steps,
                        guidance_scale=guidance_scale,
                        width=width,
                        height=height
                    )
                    
                    end_time = time.time()
                    generation_time = end_time - start_time
                
                if image:
                    st.image(image, caption=f"Prompt: {prompt}", use_column_width=True)
                    st.success(f"✨ สร้างภาพเสร็จแล้ว! (ใช้เวลา {generation_time:.2f} วินาที)")
                    
                    # Download button
                    img_buffer = io.BytesIO()
                    image.save(img_buffer, format='PNG')
                    img_buffer.seek(0)
                    
                    st.download_button(
                        label="💾 Download Image",
                        data=img_buffer,
                        file_name=f"generated_image_{int(time.time())}.png",
                        mime="image/png",
                        use_container_width=True
                    )
                else:
                    st.error("เกิดข้อผิดพลาดในการสร้างภาพ กรุณาลองใหม่อีกครั้ง")
        
        elif 'generated_image' not in st.session_state:
            st.info("👆 ใส่ prompt และกด Generate เพื่อสร้างภาพ")
            st.image("https://via.placeholder.com/512x512/f0f0f0/cccccc?text=Your+Generated+Image+Will+Appear+Here", 
                    caption="รอการสร้างภาพ...", use_column_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🤖 Powered by <strong>Openjourney</strong> from Hugging Face | Made with ❤️ using Streamlit</p>
        <p>💡 <strong>Tips:</strong> เพิ่ม "mdjrny-v4 style" ใน prompt เพื่อผลลัพธ์ที่ดีขึ้น</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
