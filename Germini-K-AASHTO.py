import streamlit as st
from PIL import Image, ImageDraw

def main():
    st.title("เครื่องมือวาดเส้นบน Nomograph Chart")
    st.write("อัปโหลดภาพกราฟ แล้วปรับเส้นสีเขียวให้ตรงกับ 'Turning Line' ก่อน")

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
        st.sidebar.header("1. Calibration (เส้นสีเขียว)")
        st.sidebar.info("ปรับให้เส้นสีเขียวทับเส้น Turning Line ในกราฟ")
        
        # ปรับ Default ให้ใกล้เคียงกราฟทั่วไปมากขึ้น
        green_x1 = st.sidebar.slider("Green Start X", 0, width, int(width * 0.53), key="gx1")
        green_y1 = st.sidebar.slider("Green Start Y", 0, height, int(height * 0.48), key="gy1")
        green_x2 = st.sidebar.slider("Green End X", 0, width, int(width * 0.95), key="gx2")
        green_y2 = st.sidebar.slider("Green End Y", 0, height, int(height * 0.95), key="gy2")

        # วาดเส้นสีเขียวอ้างอิง
        draw.line([(green_x1, green_y1), (green_x2, green_y2)], fill="green", width=6)

        # คำนวณความชัน (Slope)
        if green_x2 - green_x1 == 0:
            slope_green = 0
        else:
            slope_green = (green_y2 - green_y1) / (green_x2 - green_x1)

        # =========================================
        # ส่วนที่ 2: กำหนดค่าตามที่คุณระบุ (เปลี่ยนชื่อตามภาพ)
        # =========================================
        st.sidebar.header("2. กำหนดเส้นทางการอ่านค่า")
        
        # เปลี่ยนชื่อ: จุดเริ่มต้น แกน X -> กำหนดความหนา
        start_x = st.sidebar.slider("กำหนดความหนา", 0, width, int(width * 0.25))
        
        # เปลี่ยนชื่อ: จุดเริ่มแกน Y -> กำหนด E equivalent
        start_y_bottom = st.sidebar.slider("กำหนด E equivalent", 0, height, int(height * 0.85))
        
        # เปลี่ยนชื่อ: ความสูงจุดตัดที่ 1 -> กำหนด Mr ดินคันทาง 1500 CBR
        # (ตัวแปรนี้คือ stop_y_1 ซึ่งควบคุมความสูงของเส้นแนวนอน)
        stop_y_1 = st.sidebar.slider("กำหนด Mr ดินคันทาง 1500 CBR", 0, height, int(height * 0.3))
        
        # ส่วนที่เหลือ (แกน k)
        st.sidebar.markdown("---")
        st.sidebar.caption("ส่วนแสดงผลลัพธ์ (แกน k)")
        # ใช้ label เดิม หรือเปลี่ยนถ้าต้องการ
        # ในที่นี้ซ่อน slider end_x ไว้คำนวณอัตโนมัติ หรือปล่อยไว้ปรับละเอียดได้
        # เพื่อความสะอาดของหน้าจอ ผมจะคงไว้แต่แยกส่วนให้ชัดเจน
        
        k_axis_y = st.sidebar.slider("ความสูงของแกน k (จุดสิ้นสุดลูกศร)", 0, height, int(height * 0.7), key="ky")

        # =========================================
        # ส่วนที่ 3: คำนวณและวาดเส้น
        # =========================================
        line_width = 5
        arrow_size = 15

        # --- 3.1 วาดเส้นสีแดง (Red Lines) ---
        # เส้นตั้ง (จาก E equivalent ขึ้นไปหา Mr)
        draw.line([(start_x, start_y_bottom), (start_x, stop_y_1)], fill="red", width=line_width)
        # หัวลูกศรสีแดง (จุดเริ่ม)
        draw.polygon([
            (start_x, start_y_bottom),
            (start_x - arrow_size/2, start_y_bottom - arrow_size),
            (start_x + arrow_size/2, start_y_bottom - arrow_size)
        ], fill="red")


        # --- 3.2 คำนวณจุดตัดบนเส้นสีเขียว (Auto-Constrain) ---
        target_y = stop_y_1
        constrained_x = green_x1 + (target_y - green_y1) / slope_green
        constrained_x = int(constrained_x)

        # --- 3.3 วาดเส้นสีเหลือง (Yellow Lines) ---
        # เส้นนอน (จากเส้นแดง -> ไปหาจุดบนเส้นเขียว)
        draw.line([(start_x, stop_y_1), (constrained_x, stop_y_1)], fill="orange", width=line_width)
        
        # เส้นตั้งลง (จากจุดบนเส้นเขียว -> ลงไปหาแกน k)
        draw.line([(constrained_x, stop_y_1), (constrained_x, k_axis_y)], fill="orange", width=line_width)

        # --- 3.4 วาดจุดและลูกศร ---
        # จุดสีดำ (จุดหมุน)
        radius = 10
        draw.ellipse([
            (constrained_x - radius, stop_y_1 - radius), 
            (constrained_x + radius, stop_y_1 + radius)
        ], fill="black", outline="purple", width=3)

        # หัวลูกศรสีเหลือง (ปลายทาง)
        draw.polygon([
            (constrained_x, k_axis_y),
            (constrained_x - arrow_size/2, k_axis_y - arrow_size),
            (constrained_x + arrow_size/2, k_axis_y - arrow_size)
        ], fill="orange")

        # แสดงผลรูปภาพ
        st.image(img_draw, caption="รูปภาพพร้อมเส้นที่วาด", use_column_width=True)
        
        # แสดงค่าพิกัดให้ดูง่ายๆ
        st.success(f"จุดตัด (Turning Point): X={constrained_x}, Y={stop_y_1}")

if __name__ == "__main__":
    main()
