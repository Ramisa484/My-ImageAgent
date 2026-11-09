import matplotlib
matplotlib.use('Agg')

import streamlit as st
import os
import time
import random
import schemdraw
import schemdraw.elements as elm
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import ollama

# --- تنظیمات اولیه صفحه ---
st.set_page_config(page_title="Ramisa's AI Studio", page_icon="✨", layout="wide", initial_sidebar_state="expanded")

# --- لود کردن استایل ---
def load_css(file_name):
    try:
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        pass

load_css('style.css')

# --- مدیریت حافظه (Session State) ---
if 'history' not in st.session_state:
    st.session_state.history = []
if 'gallery' not in st.session_state:
    st.session_state.gallery = []
if 'circuit_gallery' not in st.session_state:
    st.session_state.circuit_gallery = []
if 'current_image' not in st.session_state:
    st.session_state.current_image = None
if 'uploaded_img_path' not in st.session_state:
    st.session_state.uploaded_img_path = None
if 'bg_style' not in st.session_state:
    st.session_state.bg_style = "light" 

# --- اعمال کلاس پس‌زمینه ---
if st.session_state.bg_style == "nature":
    st.markdown('<div class="bg-nature"></div>', unsafe_allow_html=True)
elif st.session_state.bg_style == "dark":
    st.markdown('<div class="bg-dark"></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="bg-light"></div>', unsafe_allow_html=True)


# --- هدر سایت ---
st.markdown("""
<div class="main-header">
    <h1>✨ Ramisa's AI Studio</h1>
    <p>خلق تصویر، تحلیل و طراحی مدارهای الکتریکی</p>
</div>
""", unsafe_allow_html=True)

# --- داشبورد آمار ---
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    st.markdown(f"<div class='metric-card'>🖼️ تصاویر تولید شده<br><span class='metric-value'>{len(st.session_state.gallery)}</span></div>", unsafe_allow_html=True)
with col_s2:
    st.markdown(f"<div class='metric-card'>⚡ مدارهای طراحی شده<br><span class='metric-value'>{len(st.session_state.circuit_gallery)}</span></div>", unsafe_allow_html=True)
with col_s3:
    st.markdown("<div class='metric-card'>🟢 وضعیت سیستم<br><span class='metric-value'>آنلاین</span></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- سایدبار (پنل کاربری و تنظیمات) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #0D6EFD;'>Ramisa's Panel</h2>", unsafe_allow_html=True)
    st.divider()
    
    st.subheader("🎨 پس‌زمینه سایت")
    bg_choice = st.radio("انتخاب تم پس‌زمینه:", ["روشن (Light)", "تیره (Dark)"])
    if bg_choice == "روشن (Light)":
        st.session_state.bg_style = "light"
    else:
        st.session_state.bg_style = "dark"
        
    st.divider()

    st.subheader("📤 آپلود عکس برای تحلیل")
    uploaded_file = st.file_uploader("یک عکس انتخاب کنید (JPG/PNG)", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="عکس آپلود شده", use_column_width=True)
        
        os.makedirs("gallery", exist_ok=True)
        save_path = f"gallery/upload_{int(time.time())}.png"
        image.save(save_path)
        st.session_state.uploaded_img_path = save_path
        st.success("عکس آپلود شد. برای تحلیل، از کادر چت پایین استفاده کنید.")

    st.divider()
    
    # --- جایگاه اسم شما ---
    st.markdown("<div style='text-align: center; padding: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6C757D; font-size: 12px;'>Designed & Developed by</p>", unsafe_allow_html=True)
    st.markdown("<p style='color: #0D6EFD; font-size: 16px; font-weight: bold;'>Ramisa Fakhr Rasouli</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- چیدمان اصلی (تب‌ها) ---
tab1, tab2, tab3 = st.tabs(["🎨 تولید تصویر", "⚡ طراحی مدار", "💬 چت و تحلیل"])

# ----------------- تب ۱: تولید تصویر -----------------
with tab1:
    col_main, col_side = st.columns([2.5, 1.5])
    with col_main:
        st.markdown("<h3 class='section-title'>🎨 خلق تصویر جدید</h3>", unsafe_allow_html=True)
        prompt = st.text_area("توصیف تصویر خود را بنویسید:", height=100, placeholder="مثال: A majestic dragon flying over a neon cyberpunk city...")
        
        if st.button("🚀 شروع تولید تصویر", use_container_width=True):
            if prompt:
                progress_text = "در حال طراحی و تولید تصویر..."
                my_bar = st.progress(0, text=progress_text)
                
                try:
                    for percent in range(100):
                        time.sleep(0.01)
                        my_bar.progress(percent + 1, text=f"{progress_text} ({percent+1}%)")
                    
                    image = Image.new('RGB', (1024, 1024), color=(240, 242, 245))
                    draw = ImageDraw.Draw(image)
                    
                    color1 = (random.randint(100, 200), random.randint(150, 220), random.randint(200, 255))
                    color2 = (random.randint(200, 255), random.randint(150, 200), random.randint(100, 150))
                    
                    for y in range(1024):
                        r = int(color1[0] + (color2[0] - color1[0]) * y / 1024)
                        g = int(color1[1] + (color2[1] - color1[1]) * y / 1024)
                        b = int(color1[2] + (color2[2] - color1[2]) * y / 1024)
                        draw.line([(0, y), (1024, y)], fill=(r, g, b))
                    
                    for _ in range(10):
                        x, y = random.randint(0, 1024), random.randint(0, 1024)
                        radius = random.randint(50, 300)
                        outline = (random.randint(0, 100), random.randint(100, 200), random.randint(200, 255))
                        draw.ellipse([x-radius, y-radius, x+radius, y+radius], outline=outline, width=random.randint(5, 15))

                    try:
                        font = ImageFont.truetype("arial.ttf", 60)
                        draw.text((50, 850), "AI Generated", font=font, fill=(33, 37, 41))
                    except:
                        pass
                    
                    os.makedirs("gallery", exist_ok=True)
                    img_name = f"gallery/img_{len(st.session_state.gallery)}_{int(time.time())}.png"
                    image.save(img_name)
                    
                    st.session_state.current_image = img_name
                    st.session_state.gallery.append({"path": img_name, "prompt": prompt, "time": datetime.now().strftime("%Y-%m-%d %H:%M")})
                    st.session_state.history.append({"time": datetime.now().strftime("%H:%M"), "text": prompt})
                    
                    my_bar.progress(100, text="تصویر با موفقیت تولید شد!")
                    time.sleep(0.5)
                    my_bar.empty()
                    st.success("✅ تصویر شما با موفقیت ساخته شد!")
                    st.rerun()
                    
                except Exception as e:
                    my_bar.empty()
                    st.error(f"❌ خطا: {e}")
            else:
                st.warning("⚠️ لطفا ابتدا پرامپت خود را بنویسید.")

        st.divider()
        st.markdown("<h3 class='section-title'>🖼️ پیش‌نمایش تصویر</h3>", unsafe_allow_html=True)
        if st.session_state.current_image:
            st.image(st.session_state.current_image, use_column_width=True)
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🗑️ حذف از صفحه", use_container_width=True):
                    st.session_state.current_image = None
                    st.rerun()
            with c2:
                with open(st.session_state.current_image, "rb") as file:
                    st.download_button(label="💾 دانلود عکس", data=file, file_name="ai_image.png", mime="image/png", use_container_width=True)
        else:
            st.info("هنوز تصویری تولید نکرده‌اید.")

# ----------------- تب ۲: طراحی مدار -----------------
with tab2:
    st.markdown("<h3 class='section-title'>⚡ طراحی و تحلیل مدارهای الکتریکی</h3>", unsafe_allow_html=True)
    st.info("در این بخش می‌توانید مدارهای منطقی و الکتریکی را طراحی یا تحلیل کنید.")
    
    circuit_mode = st.radio("حالت کار با مدار:", 
                            ["۱. کشیدن مدار از روی توضیحات (متن به مدار)", 
                             "۲. تحلیل عکس مدار (عکس به توضیحات)"],
                            horizontal=True)
    
    st.divider()
    
    if circuit_mode.startswith("۱"):
        st.subheader("📝 توضیحات مدار را بنویسید")
        circuit_prompt = st.text_area("مثال: یک مدار ساده با باتری، مقاومت و LED", height=100)
        
        if st.button("⚡ رسم مدار", use_container_width=True):
            if circuit_prompt:
                with st.spinner("در حال ترسیم مدار..."):
                    try:
                        d = schemdraw.Drawing()
                        d += elm.Battery().label('9V')
                        d += elm.Resistor().label('1kΩ')
                        d += elm.LED().label('LED')
                        d += elm.Line().down()
                        d += elm.Line().left()
                        
                        os.makedirs("circuits", exist_ok=True)
                        circuit_path = f"circuits/circuit_{int(time.time())}.png"
                        d.save(circuit_path, dpi=150)
                        
                        st.session_state.circuit_gallery.append({"path": circuit_path, "prompt": circuit_prompt, "time": datetime.now().strftime("%H:%M")})
                        st.success("مدار با موفقیت ترسیم شد!")
                        st.image(circuit_path, caption=f"مدار: {circuit_prompt}")
                        
                    except Exception as e:
                        st.error(f"خطا در ترسیم مدار: {e}")
    
    elif circuit_mode.startswith("۲"):
        st.subheader("📸 عکس مدار خود را آپلود کنید")
        st.write("این بخش به شما اجازه می‌دهد عکسی از یک مدار را آپلود کنید تا ایجنت آن را تحلیل کند.")
        
        circuit_image = st.file_uploader("آپلود عکس مدار (JPG/PNG)", type=["jpg", "png", "jpeg"], key="circuit_upload")
        
        if circuit_image is not None:
            img = Image.open(circuit_image)
            st.image(img, caption="مدار آپلود شده", use_column_width=True)
            
            os.makedirs("circuits", exist_ok=True)
            img_path = f"circuits/uploaded_{int(time.time())}.png"
            img.save(img_path)
            
            if st.button("📝 توضیحات مدار را استخراج کن", use_container_width=True):
                with st.spinner("ایجنت در حال تحلیل مدار است..."):
                    try:
                        # استفاده از مدل جدید llava-vision
                        response = ollama.chat(
                            model='llava-vision', 
                            messages=[{'role': 'user', 'content': 'این مدار الکتریکی را تحلیل کن و اجزای آن (مقاومت، خازن، باتری و...) را به فارسی توضیح بده.', 'images': [img_path]}],
                            options={'num_gpu': 0}
                        )
                        st.success("تحلیل ایجنت:")
                        st.write(response['message']['content'])
                    except Exception as e:
                        st.error(f"خطا: {e}")

    st.divider()
    st.subheader("🖼️ گالری مدارها")
    if not st.session_state.circuit_gallery:
        st.write("هنوز مداری طراحی نشده است.")
    else:
        cols = st.columns(3)
        for idx, item in enumerate(reversed(st.session_state.circuit_gallery)):
            with cols[idx % 3]:
                st.image(item['path'], caption=item['prompt'])
                st.caption(f"⏱️ {item.get('time', '')}")

# ----------------- تب ۳: چت و تحلیل -----------------
with tab3:
    st.markdown("<h3 class='section-title'>💬 چت با ایجنت هوش مصنوعی</h3>", unsafe_allow_html=True)
    user_chat = st.text_input("پیام خود را بنویسید:")
    if st.button("ارسال پیام"):
        if user_chat:
            with st.spinner("ایجنت در حال پردازش است..."):
                try:
                    messages = [{'role': 'user', 'content': user_chat}]
                    if st.session_state.uploaded_img_path and os.path.exists(st.session_state.uploaded_img_path):
                        messages[0]['images'] = [st.session_state.uploaded_img_path]
                    
                    # استفاده از مدل جدید llava-vision
                    res = ollama.chat(model='llava-vision', messages=messages, options={'num_gpu': 0})
                    st.success("پاسخ ایجنت:")
                    st.write(res['message']['content'])
                except Exception as e:
                    st.error(f"خطا: {e}")

# --- بخش گالری تصاویر در سایدبار ---
with st.sidebar:
    st.divider()
    st.subheader("📋 تاریخچه تصاویر")
    if st.session_state.history:
        for item in reversed(st.session_state.history):
            st.write(f"- {item['time']}: {item['text'][:20]}...")