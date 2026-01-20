import streamlit as st
from PIL import Image, ImageDraw

def main():
    st.title("เครื่องมือวาดเส้นบน Nomograph Chart")

    # 1. ส่วนอัปโหลดไฟล์
    uploaded_file = st.file_uploader("อัปโหลดรูปภาพกราฟของคุณ", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        # เปิดรูปภาพด้วย Pillow
        image = Image.open(uploaded_file).convert("RGB")
        width, height = image.size

        st.sidebar.header("กำหนดพิกัดเส้น (Pixels)")
        
        # 2. สร้าง Sliders เพื่อกำหนดจุดต่างๆ (จำลองตาม Logic ในภาพ)
        # Start X: จุดเริ่มต้นแกน X ด้านล่าง (MR)
        start_x = st.sidebar.slider("จุดเริ่มต้น แกน X (MR)", 0, width, int(width * 0.25))
        
        # Height 1: ความสูงของเส้นแรกที่จะลากขึ้นไป (DSB)
        stop_y_1 = st.sidebar.slider("ความสูงจุดตัดที่ 1 (DSB)", 0, height, int(height * 0.3))
        
        # Width 1: ลากไปทางขวาถึงจุดไหน (ESB)
        stop_x_2 = st.sidebar.slider("จุดตัดที่ 2 แนวนอน (ESB)", 0, width, int(width * 0.65))
        
        # Height 2: ลากลงมาถึง Turning Line
        stop_y_2 = st.sidebar.slider("ความสูงจุดตัดที่ 3 (Turning Line)", 0, height, int(height * 0.6))
        
        # End X: ลากไปขวาสุด (k infinity)
        end_x = st.sidebar.slider("จุดสิ้นสุด แกน X (k)", 0, width, int(width * 0.75))

        # จุดเริ่มต้น Y (สมมติว่าเริ่มจากขอบล่างของกราฟ หรือให้ user ปรับ)
        start_y_bottom = st.sidebar.slider("จุดเริ่มแกน Y (ขอบล่าง)", 0, height, int(height * 0.85))

        # 3. เตรียมวาดภาพ
        # สร้างสำเนาภาพเพื่อวาดทับ (เพื่อไม่ให้ภาพต้นฉบับเสีย)
        img_draw = image.copy()
        draw = ImageDraw.Draw(img_draw)

        # กำหนดสีและความหนา
        line_color = "red"
        line_width = 5

        # 4. วาดเส้นตาม Step (ขึ้น -> ขวา -> ลง -> ขวา)
        
        # เส้นที่ 1: จากด้านล่าง ขึ้นไปหา DSB
        # (start_x, start_y_bottom) -> (start_x, stop_y_1)
        draw.line([(start_x, start_y_bottom), (start_x, stop_y_1)], fill=line_color, width=line_width)
        
        # เส้นที่ 2: เลี้ยวขวาไปหา ESB
        # (start_x, stop_y_1) -> (stop_x_2, stop_y_1)
        draw.line([(start_x, stop_y_1), (stop_x_2, stop_y_1)], fill=line_color, width=line_width)

        # เส้นที่ 3: เลี้ยวลงไปหา Turning Line
        # (stop_x_2, stop_y_1) -> (stop_x_2, stop_y_2)
        draw.line([(stop_x_2, stop_y_1), (stop_x_2, stop_y_2)], fill=line_color, width=line_width)

        # เส้นที่ 4: เลี้ยวขวาไปหา k infinity
        # (stop_x_2, stop_y_2) -> (end_x, stop_y_2)
        draw.line([(stop_x_2, stop_y_2), (end_x, stop_y_2)], fill=line_color, width=line_width)

        # (Optional) วาดหัวลูกศรที่ปลายทาง
        # การวาดหัวลูกศรใน PIL ต้องวาด Polygon เอง
        arrow_size = 15
        draw.polygon([
            (end_x, stop_y_2), 
            (end_x - arrow_size, stop_y_2 - arrow_size/2), 
            (end_x - arrow_size, stop_y_2 + arrow_size/2)
        ], fill=line_color)

        # 5. แสดงผลรูปภาพ
        st.image(img_draw, caption="รูปภาพพร้อมเส้นที่วาด", use_column_width=True)
        
        st.info("ลองปรับค่า Slider ด้านซ้ายเพื่อให้เส้นตรงกับจุดที่คุณต้องการบนกราฟ")

if __name__ == "__main__":
    main()
