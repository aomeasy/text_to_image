# 🎨 AI Image Generator

เว็บแอปพลิเคชันสำหรับสร้างภาพด้วย AI โดยใช้ Text-to-Image model จาก Hugging Face

## ✨ Features

- 🖼️ สร้างภาพจาก text prompt ด้วย AI
- 🎨 ใช้ Openjourney model (fine-tuned จาก Stable Diffusion)
- ⚙️ ปรับแต่งค่า parameters ได้
- 💾 ดาウน์โหลดภาพที่สร้างได้
- 📱 Responsive design ใช้งานได้ทั้งมือถือและคอมพิวเตอร์

## 🚀 Quick Start

### วิธีการ Deploy บน GitHub + Streamlit Community Cloud

1. **Clone หรือ Fork repository นี้**
   ```bash
   git clone <your-repo-url>
   cd ai-image-generator
   ```

2. **Push ไฟล์ขึ้น GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

3. **Deploy บน Streamlit Community Cloud**
   - ไปที่ [share.streamlit.io](https://share.streamlit.io)
   - เข้าสู่ระบบด้วย GitHub account
   - คลิก "New app"
   - เลือก repository และ branch
   - ตั้งค่า Main file path: `app.py`
   - คลิก "Deploy!"

### วิธีการรันแบบ Local

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**
   ```bash
   streamlit run app.py
   ```

3. **เปิดเบราว์เซอร์ไปที่** `http://localhost:8501`

## 📝 การใช้งาน

1. **ใส่ Prompt**: อธิบายภาพที่ต้องการสร้าง
2. **ปรับแต่งการตั้งค่า** (ถ้าต้องการ):
   - Number of inference steps: ขั้นตอนการสร้างภาพ (มากขึ้น = คุณภาพดีขึ้น แต่ช้าขึ้น)
   - Guidance scale: ความแม่นยำตาม prompt (7.5 แนะนำ)
   - ขนาดภาพ: 512x512 แนะนำ
3. **คลิก Generate Image**
4. **ดาวน์โหลดภาพ** ที่สร้างแล้ว

## 💡 Tips สำหรับ Prompt ที่ดี

- **เพิ่ม "mdjrny-v4 style"** ใน prompt เพื่อผลลัพธ์ที่ดีขึ้น
- ใช้คำอธิบายที่ชัดเจนและเฉพาะเจาะจง
- เพิ่มคำว่า "high quality", "detailed", "beautiful" เพื่อคุณภาพที่ดีขึ้น
- ระบุสี style หรือ mood ที่ต้องการ

### ตัวอย่าง Prompt ที่ดี:
```
beautiful landscape with mountains and lake, mdjrny-v4 style
cute cartoon cat wearing sunglasses, mdjrny-v4 style  
futuristic city at sunset, mdjrny-v4 style
delicious pizza with lots of toppings, mdjrny-v4 style
```

## 🔧 Technical Details

- **Model**: [prompthero/openjourney](https://huggingface.co/prompthero/openjourney)
- **Framework**: Streamlit
- **AI Library**: Hugging Face Diffusers
- **Deployment**: Streamlit Community Cloud
- **GPU Support**: รองรับทั้ง CUDA และ CPU

## 📁 Project Structure

```
ai-image-generator/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies  
├── README.md          # Documentation
└── .gitignore         # Git ignore file
```

## 🚨 System Requirements

- **RAM**: อย่างน้อย 8GB (แนะนำ 16GB)
- **Storage**: อย่างน้อย 10GB ว่าง
- **GPU**: ไม่จำเป็น แต่จะทำให้เร็วขึ้นมาก
- **Internet**: สำหรับดาวน์โหลด model ครั้งแรก (~5GB)

## 🔒 Privacy & Security

- ไม่เก็บภาพหรือ prompt ของผู้ใช้
- การประมวลผลทั้งหมดทำในเครื่อง/server
- ไม่ส่งข้อมูลไปยัง third-party

## 🐛 Troubleshooting

### Model โหลดช้า
- เชื่อมต่อ internet ที่เร็วสำหรับดาวน์โหลดครั้งแรก
- รอสักครู่ model จะถูก cache ไว้

### Memory Error
- ลดขนาดภาพ (เป็น 256x256)
- ลด inference steps
- ปิดแอปอื่นๆ

### CUDA Out of Memory
- ลดขนาดภาพ
- App จะใช้ CPU แทน GPU อัตโนมัติ

## 📚 Learn More

- [Stable Diffusion Documentation](https://huggingface.co/docs/diffusers/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Openjourney Model](https://huggingface.co/prompthero/openjourney)

## 🤝 Contributing

Pull requests are welcome! สำหรับการเปลี่ยนแปลงใหญ่ กรุณาเปิด issue เพื่อคุยกันก่อน

## 📄 License

MIT License - ใช้งานได้อย่างอิสระ

---

Made with ❤️ using Streamlit and Hugging Face
