import streamlit as st
from PIL import Image, ImageDraw

def main():
    st.title("เครื่องมือวาดเส้นบน Nomograph Chart (Auto-Constrain)")
    st.write("อัปโหลดภาพกราฟ แล้วปรับเส้นสีเขียวให้ตรงกับ 'Turning Line' ก่อน จากนั้นจุดสีดำจะล็อกอยู่บนเส้นนั้นโดยอัตโนมัติ")

    # 1. ส่วนอัปโหลดไฟล์
    uploaded_file = st.file_uploader("อัปโหลดรูปภาพกราฟของคุณ", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        width, height = image.size
        img_draw = image.copy()
        draw = ImageDraw.Draw(img_draw)
        
        # =========================================
        # ส่วนที่ 1: กำหนดตำแหน่งเส้นอ้างอิงสีเขียว (Turning Line)
        # =========================================
        st.sidebar.header("1. กำหนดตำแหน่งเส้นสีเขียว (Turning Line)")
        st.sidebar.info("ปรับจุดเริ่มต้นและสิ้นสุดให้เส้นสีเขียวทับกับเส้น Turning Line บนกราฟพอดี")
        
        # จุดเริ่มต้นของเส้นสีเขียว (มุมซ้ายบนของเส้น)
        green_x1 = st.sidebar.slider("Green Line Start X", 0, width, int(width * 0.45), key="gx1")
        green_y1 = st.sidebar.slider("Green Line Start Y", 0, height, int(height * 0.45), key="gy1")
        
        # จุดสิ้นสุดของเส้นสีเขียว (มุมขวาล่างของเส้น)
        green_x2 = st.sidebar.slider("Green Line End X", 0, width, int(width * 0.9), key="gx2")
        green_y2 = st.sidebar.slider("Green Line End Y", 0, height, int(height * 0.9), key="gy2")

        # วาดเส้นสีเขียวอ้างอิง
        draw.line([(green_x1, green_y1), (green_x2, green_y2)], fill="green", width=8)

        # คำนวณความชัน (Slope) ของเส้นสีเขียว เพื่อใช้หาสมการเส้นตรง
        # ป้องกันการหารด้วยศูนย์กรณีเส้นตั้งฉาก (แม้จะไม่น่าเกิดขึ้นกับกราฟนี้)
        if green_x2 - green_x1 == 0:
            slope_green = 0 # หรือจัดการ error ตามเหมาะสม
            st.error("เส้นสีเขียวต้องไม่เป็นเส้นแนวตั้งฉาก")
            return
        else:
            slope_green = (green_y2 - green_y1) / (green_x2 - green_x1)

        # =========================================
        # ส่วนที่ 2: กำหนดเส้นทางการอ่านค่า (แดง -> เหลือง)
        # =========================================
        st.sidebar.header("2. กำหนดเส้นทางการอ่านค่า")
        
        # จุดเริ่มต้น แกน X (MR)
        start_x = st.sidebar.slider("จุดเริ่มต้น แกน X (MR)", 0, width, int(width * 0.25))
        # จุดเริ่มแกน Y (ขอบล่าง)
        start_y_bottom = st.sidebar.slider("จุดเริ่มแกน Y (ขอบล่าง)", 0, height, int(height * 0.85))
        
        # ความสูงจุดตัดที่ 1 (DSB) - นี่คือค่า Y ที่จะกำหนดตำแหน่งจุดสีดำ
        stop_y_1 = st.sidebar.slider("ความสูงจุดตัดที่ 1 (DSB)", 0, height, int(height * 0.3))
        
        # จุดสิ้นสุด แกน X (k) สำหรับเส้นเหลืองแนวตั้ง
        end_x = st.sidebar.slider("จุดสิ้นสุด แกน X (k)", 0, width, int(width * 0.75))

        # =========================================
        # ส่วนที่ 3: คำนวณและวาดเส้น
        # =========================================
        line_width = 5

        # --- 3.1 วาดเส้นสีแดง (Red Lines) ---
        # เส้นตั้งขึ้น (MR -> เส้นโค้ง DSB)
        draw.line([(start_x, start_y_bottom), (start_x, stop_y_1)], fill="red", width=line_width)

        # --- 3.2 คำนวณจุดตัดบนเส้นสีเขียว (The Magic Happens Here!) ---
        # เราทราบค่า Y (คือ stop_y_1) เราต้องการหาค่า X ที่อยู่บนเส้นสีเขียว
        # จากสมการเส้นตรงแบบจุด-ความชัน: y - y1 = m(x - x1)
        # แปลงเพื่อหา x: x = x1 + (y - y1) / m
        
        target_y = stop_y_1
        # คำนวณ X ที่ถูกบังคับให้อยู่บนเส้นสีเขียว
        constrained_x = green_x1 + (target_y - green_y1) / slope_green
        constrained_x = int(constrained_x) # แปลงเป็น integer สำหรับพิกัด

        # --- 3.3 วาดเส้นสีเหลือง (Yellow Lines) ---
        # เส้นนอน (จากเส้นแดง -> ไปหาจุดบนเส้นเขียว)
        # จุดเริ่มต้นคือ (start_x, stop_y_1), จุดสิ้นสุดคือ (constrained_x, stop_y_1)
        draw.line([(start_x, stop_y_1), (constrained_x, stop_y_1)], fill="orange", width=line_width)
        
        # เส้นตั้งลง (จากจุดบนเส้นเขียว -> ลงไปหาแกน k)
        # จุดเริ่มต้นคือ (constrained_x, stop_y_1), จุดสิ้นสุดคือ (constrained_x, end_x?? ไม่ใช่ ต้องเป็นความสูงอื่น)
        # ตามภาพ เส้นเหลืองตั้ง จะลากจากจุดดำ ลงมาที่ความสูงของแกน k
        # เราต้องการ Slider อีกตัวเพื่อบอกว่าแกน k อยู่สูงเท่าไหร่
        k_axis_y = st.sidebar.slider("ความสูงของแกน k (ด้านขวา)", 0, height, int(height * 0.7), key="ky")
        draw.line([(constrained_x, stop_y_1), (constrained_x, k_axis_y)], fill="orange", width=line_width)

        # --- 3.4 วาดจุดและลูกศร ---
        # วาดจุดสีดำตรงจุดตัดที่คำนวณได้
        radius = 10
        draw.ellipse([
            (constrained_x - radius, stop_y_1 - radius), 
            (constrained_x + radius, stop_y_1 + radius)
        ], fill="black", outline="purple", width=3)

        # (Optional) วาดหัวลูกศรสีแดงที่จุดเริ่มต้น
        arrow_size = 15
        draw.polygon([
            (start_x, start_y_bottom),
            (start_x - arrow_size/2, start_y_bottom - arrow_size),
            (start_x + arrow_size/2, start_y_bottom - arrow_size)
        ], fill="red")
        
        # (Optional) วาดหัวลูกศรสีเหลืองที่จุดสิ้นสุดบนแกน k
        draw.polygon([
            (constrained_x, k_axis_y),
            (constrained_x - arrow_size/2, k_axis_y - arrow_size),
            (constrained_x + arrow_size/2, k_axis_y - arrow_size)
        ], fill="orange")

        # แสดงผลรูปภาพ
        st.image(img_draw, caption="ผลลัพธ์: จุดสีดำถูกล็อกบนเส้นสีเขียว", use_column_width=True)
        st.success(f"จุดตัดบนเส้นสีเขียวอยู่ที่พิกัด: ({constrained_x}, {stop_y_1})")

if __name__ == "__main__":
    main()
