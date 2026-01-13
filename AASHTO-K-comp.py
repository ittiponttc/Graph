"""
AASHTO 1993 Nomograph - Figure 3.3
Chart for Estimating Composite Modulus of Subgrade Reaction, k∞
Assuming a Semi-Infinite Subgrade Depth

พัฒนาสำหรับการเรียนการสอนวิศวกรรมถนนและผิวทาง
"""

import streamlit as st
import math
import plotly.graph_objects as go

# =====================================================
# ตั้งค่าหน้าเว็บ
# =====================================================
st.set_page_config(
    page_title="AASHTO 1993 - Figure 3.3 Nomograph",
    page_icon="🛣️",
    layout="wide"
)

# =====================================================
# CSS สำหรับ UI
# =====================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #1a365d 0%, #2c5282 50%, #2b6cb0 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        color: white;
        font-family: 'Sarabun', sans-serif;
        font-size: 1.8rem;
        margin: 0;
        font-weight: 700;
    }
    
    .main-header p {
        color: #bee3f8;
        font-family: 'Sarabun', sans-serif;
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
    }
    
    .result-box {
        background: linear-gradient(145deg, #2d3748, #1a202c);
        border: 2px solid #4299e1;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 25px rgba(66, 153, 225, 0.3);
    }
    
    .result-label {
        color: #a0aec0;
        font-family: 'Sarabun', sans-serif;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .result-value {
        color: #f6e05e;
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 0 0 20px rgba(246, 224, 94, 0.5);
    }
    
    .result-unit {
        color: #63b3ed;
        font-family: 'Sarabun', sans-serif;
        font-size: 1.2rem;
    }
    
    .input-section {
        background: #f7fafc;
        border-radius: 10px;
        padding: 1.2rem;
        border-left: 4px solid #4299e1;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# Header
# =====================================================
st.markdown("""
<div class="main-header">
    <h1>🛣️ AASHTO 1993 Nomograph - Figure 3.3</h1>
    <p>Chart for Estimating Composite Modulus of Subgrade Reaction (k∞)</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# สูตรการคำนวณ k∞ ตาม AASHTO 1993
# =====================================================
def calculate_k_inf(M_R, D_SB, E_SB):
    """
    คำนวณ Composite Modulus of Subgrade Reaction (k∞)
    ตาม AASHTO 1993 Guide for Design of Pavement Structures
    """
    k_roadbed = M_R / 19.4
    
    if D_SB > 0 and E_SB > 0:
        ratio = (E_SB / M_R) ** (1/3)
        factor = 1 + (D_SB / 38) * ratio
        k_inf = k_roadbed * (factor ** 2.32)
    else:
        k_inf = k_roadbed
    
    return k_inf

def calculate_intermediate_k(M_R, D_SB, E_SB):
    k_from_MR = M_R / 19.4
    k_inf = calculate_k_inf(M_R, D_SB, E_SB)
    return k_from_MR, k_inf

# =====================================================
# Layout: Input และ Output
# =====================================================
col_input, col_chart = st.columns([1, 2.5])

with col_input:
    st.markdown("### 📊 ข้อมูลนำเข้า (Input Parameters)")
    
    # Subbase Thickness
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown("**1️⃣ Subbase Thickness (D_SB)**")
    D_SB = st.slider(
        "ความหนาชั้น Subbase (inches)",
        min_value=4.0,
        max_value=18.0,
        value=8.0,
        step=0.5,
        key="dsb"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Subbase Elastic Modulus
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown("**2️⃣ Subbase Elastic Modulus (E_SB)**")
    E_SB_options = [15000, 20000, 25000, 30000, 40000, 50000, 75000, 100000, 
                   150000, 200000, 300000, 400000, 500000, 750000, 1000000]
    E_SB = st.select_slider(
        "โมดูลัสยืดหยุ่นชั้น Subbase (psi)",
        options=E_SB_options,
        value=75000,
        format_func=lambda x: f"{x:,}",
        key="esb"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Roadbed Soil Resilient Modulus
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown("**3️⃣ Roadbed Soil Resilient Modulus (M_R)**")
    M_R_options = list(range(1000, 21000, 500))
    M_R = st.select_slider(
        "โมดูลัสความยืดหยุ่นดินคันทาง (psi)",
        options=M_R_options,
        value=5000,
        format_func=lambda x: f"{x:,}",
        key="mr"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # คำนวณผลลัพธ์
    k_from_MR, k_inf = calculate_intermediate_k(M_R, D_SB, E_SB)
    
    # แสดงผลลัพธ์
    st.markdown("---")
    st.markdown("### 🎯 ผลการคำนวณ")
    
    st.markdown(f"""
    <div class="result-box">
        <div class="result-label">Composite Modulus of Subgrade Reaction</div>
        <div class="result-value">{k_inf:.0f}</div>
        <div class="result-unit">pci (k∞)</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(f"📌 **k จาก M_R (ไม่มี Subbase):** {k_from_MR:.1f} pci")
    
    # สูตรที่ใช้
    with st.expander("📐 สูตรการคำนวณ"):
        st.markdown("""
        **AASHTO 1993 Composite k-value Formula:**
        
        ```
        k_roadbed = M_R / 19.4
        
        k∞ = k_roadbed × [1 + (D_SB/38) × (E_SB/M_R)^(1/3)]^2.32
        ```
        
        **โดยที่:**
        - M_R = Roadbed Soil Resilient Modulus (psi)
        - D_SB = Subbase Thickness (inches)
        - E_SB = Subbase Elastic Modulus (psi)
        - k∞ = Composite Modulus of Subgrade Reaction (pci)
        
        **หมายเหตุ:** สูตรนี้สมมติ Semi-Infinite Subgrade Depth 
        (ความลึก > 10 ft จากผิว Subgrade)
        """)

# =====================================================
# วาด Nomograph ด้วย Plotly
# =====================================================
with col_chart:
    st.markdown("### 📈 AASHTO 1993 Nomograph - Figure 3.3")
    
    # กำหนดขอบเขต
    E_SB_log_min = math.log10(15000)
    E_SB_log_max = math.log10(1000000)
    D_SB_min, D_SB_max = 6, 18
    M_R_log_min = math.log10(1000)
    M_R_log_max = math.log10(20000)
    k_log_min = math.log10(50)
    k_log_max = math.log10(2000)
    
    # สร้าง Figure
    fig = go.Figure()
    
    # =====================================================
    # วาดเส้น Grid พื้นฐาน (สีเทา)
    # =====================================================
    
    # Grid สำหรับ E_SB (แนวนอน ส่วนบน)
    E_SB_values = [15000, 30000, 50000, 100000, 200000, 400000, 1000000]
    for E in E_SB_values:
        y_pos = 50 + 50 * (math.log10(E) - E_SB_log_min) / (E_SB_log_max - E_SB_log_min)
        fig.add_trace(go.Scatter(
            x=[0, 35], y=[y_pos, y_pos],
            mode='lines',
            line=dict(color='lightgray', width=0.5),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Grid สำหรับ D_SB (แนวตั้ง)
    D_SB_values = [6, 8, 10, 12, 14, 16, 18]
    for D in D_SB_values:
        x_pos = 35 * (D - D_SB_min) / (D_SB_max - D_SB_min)
        fig.add_trace(go.Scatter(
            x=[x_pos, x_pos], y=[25, 75],
            mode='lines',
            line=dict(color='lightgray', width=0.5),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Grid สำหรับ M_R (แนวนอน ส่วนล่าง)
    M_R_values = [1000, 2000, 5000, 10000, 20000]
    for M in M_R_values:
        y_pos = 25 - 25 * (math.log10(M) - M_R_log_min) / (M_R_log_max - M_R_log_min)
        fig.add_trace(go.Scatter(
            x=[0, 100], y=[y_pos, y_pos],
            mode='lines',
            line=dict(color='lightgray', width=0.5),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Grid สำหรับ k∞ (แนวตั้ง ส่วนขวา)
    k_values = [50, 100, 200, 300, 500, 800, 1000, 1500, 2000]
    for k in k_values:
        x_pos = 70 + 30 * (math.log10(k) - k_log_min) / (k_log_max - k_log_min)
        fig.add_trace(go.Scatter(
            x=[x_pos, x_pos], y=[0, 100],
            mode='lines',
            line=dict(color='lightgray', width=0.5),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # =====================================================
    # วาด Turning Line (เส้นทแยงมุมหลัก)
    # =====================================================
    fig.add_trace(go.Scatter(
        x=[35, 70], y=[50, 25],
        mode='lines',
        line=dict(color='black', width=3),
        name='Turning Line',
        hoverinfo='name'
    ))
    
    # Label สำหรับ Turning Line
    fig.add_annotation(
        x=52, y=40,
        text="Turning Line",
        showarrow=False,
        font=dict(size=12, color='black'),
        textangle=-33
    )
    
    # =====================================================
    # วาดเส้นเฉียงจาก E_SB (Fan Lines)
    # =====================================================
    for E in [15000, 50000, 100000, 300000, 1000000]:
        y_start = 50 + 50 * (math.log10(E) - E_SB_log_min) / (E_SB_log_max - E_SB_log_min)
        y_end = 50 + (y_start - 50) * 0.2
        fig.add_trace(go.Scatter(
            x=[0, 35], y=[y_start, y_end],
            mode='lines',
            line=dict(color='gray', width=0.8),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # =====================================================
    # คำนวณตำแหน่งสำหรับเส้นสีแดง (User Input)
    # =====================================================
    
    # 1. ตำแหน่ง E_SB บนแกน Y (ส่วนบน)
    y_E_SB = 50 + 50 * (math.log10(E_SB) - E_SB_log_min) / (E_SB_log_max - E_SB_log_min)
    
    # 2. ตำแหน่ง D_SB บนแกน X
    x_D_SB = 35 * (D_SB - D_SB_min) / (D_SB_max - D_SB_min)
    
    # 3. จุดบน Turning Line
    t_ratio = x_D_SB / 35
    x_turning = 35 + t_ratio * 35
    y_turning = 50 - t_ratio * 25
    
    # 4. ตำแหน่ง M_R บนแกน Y (ส่วนล่าง)
    y_M_R = 25 - 25 * (math.log10(M_R) - M_R_log_min) / (M_R_log_max - M_R_log_min)
    
    # 5. ตำแหน่ง k∞ บนแกน X (ส่วนขวา)
    k_inf_clipped = max(50, min(k_inf, 2000))
    x_k_inf = 70 + 30 * (math.log10(k_inf_clipped) - k_log_min) / (k_log_max - k_log_min)
    
    # =====================================================
    # วาดเส้นสีแดง (User Path)
    # =====================================================
    line_color = 'red'
    line_width = 3
    
    # เส้นที่ 1: E_SB → D_SB (แนวนอน)
    fig.add_trace(go.Scatter(
        x=[0, x_D_SB], y=[y_E_SB, y_E_SB],
        mode='lines',
        line=dict(color=line_color, width=line_width),
        name='User Path',
        legendgroup='user',
        showlegend=True,
        hoverinfo='skip'
    ))
    
    # เส้นที่ 2: D_SB → Turning Line (แนวตั้งลง)
    fig.add_trace(go.Scatter(
        x=[x_D_SB, x_D_SB], y=[y_E_SB, y_turning],
        mode='lines',
        line=dict(color=line_color, width=line_width),
        legendgroup='user',
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # เส้นที่ 3: Turning Line → M_R (แนวเฉียง)
    fig.add_trace(go.Scatter(
        x=[x_turning, 70], y=[y_turning, y_M_R],
        mode='lines',
        line=dict(color=line_color, width=line_width),
        legendgroup='user',
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # เส้นที่ 4: M_R → k∞ (แนวนอนไปขวา)
    fig.add_trace(go.Scatter(
        x=[70, x_k_inf], y=[y_M_R, y_M_R],
        mode='lines',
        line=dict(color=line_color, width=line_width),
        legendgroup='user',
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # เส้นที่ 5: k∞ ขึ้นไปด้านบน
    fig.add_trace(go.Scatter(
        x=[x_k_inf, x_k_inf], y=[y_M_R, 100],
        mode='lines',
        line=dict(color=line_color, width=line_width),
        legendgroup='user',
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # =====================================================
    # วาดจุดที่สำคัญ (Markers)
    # =====================================================
    points_x = [0, x_D_SB, x_turning, 70, x_k_inf]
    points_y = [y_E_SB, y_E_SB, y_turning, y_M_R, y_M_R]
    points_text = [
        f'E_SB = {E_SB:,} psi',
        f'D_SB = {D_SB:.1f}"',
        'Turning Point',
        f'M_R = {M_R:,} psi',
        f'k∞ = {k_inf:.0f} pci'
    ]
    
    fig.add_trace(go.Scatter(
        x=points_x, y=points_y,
        mode='markers+text',
        marker=dict(color=line_color, size=14, line=dict(color='white', width=2)),
        text=points_text,
        textposition=['middle right', 'top center', 'bottom right', 'bottom center', 'top center'],
        textfont=dict(size=10, color='darkred'),
        name='Intersection Points',
        hoverinfo='text'
    ))
    
    # =====================================================
    # Labels สำหรับแกนต่างๆ
    # =====================================================
    
    # E_SB labels (ซ้ายบน)
    for E in [15000, 50000, 100000, 400000, 1000000]:
        y_pos = 50 + 50 * (math.log10(E) - E_SB_log_min) / (E_SB_log_max - E_SB_log_min)
        label = f'{E//1000}k' if E >= 1000 else str(E)
        fig.add_annotation(x=-2, y=y_pos, text=label, showarrow=False, 
                          font=dict(size=9), xanchor='right')
    
    # D_SB labels (กลาง)
    for D in D_SB_values:
        x_pos = 35 * (D - D_SB_min) / (D_SB_max - D_SB_min)
        fig.add_annotation(x=x_pos, y=48, text=str(int(D)), showarrow=False, 
                          font=dict(size=9), yanchor='top')
    
    # M_R labels (ซ้ายล่าง)
    for M in [1000, 2000, 5000, 10000, 20000]:
        y_pos = 25 - 25 * (math.log10(M) - M_R_log_min) / (M_R_log_max - M_R_log_min)
        label = f'{M//1000}k'
        fig.add_annotation(x=-2, y=y_pos, text=label, showarrow=False, 
                          font=dict(size=9), xanchor='right')
    
    # k∞ labels (ขวาบน)
    for k in [50, 100, 200, 500, 1000, 2000]:
        x_pos = 70 + 30 * (math.log10(k) - k_log_min) / (k_log_max - k_log_min)
        fig.add_annotation(x=x_pos, y=102, text=str(k), showarrow=False, 
                          font=dict(size=9), textangle=-45)
    
    # =====================================================
    # Axis Labels
    # =====================================================
    fig.add_annotation(x=-8, y=75, text="E_SB (psi)", showarrow=False,
                      font=dict(size=11, color='darkblue'), textangle=-90)
    fig.add_annotation(x=17, y=46, text="D_SB (inches)", showarrow=False,
                      font=dict(size=11, color='darkblue'))
    fig.add_annotation(x=-8, y=12, text="M_R (psi)", showarrow=False,
                      font=dict(size=11, color='darkblue'), textangle=-90)
    fig.add_annotation(x=85, y=105, text="k∞ (pci)", showarrow=False,
                      font=dict(size=11, color='darkblue'))
    
    # =====================================================
    # Layout
    # =====================================================
    fig.update_layout(
        title=dict(
            text='<b>AASHTO 1993 - Figure 3.3: Composite k-value</b>',
            font=dict(size=16, color='#1a365d'),
            x=0.5
        ),
        xaxis=dict(
            range=[-15, 105],
            showgrid=False,
            showticklabels=False,
            zeroline=False
        ),
        yaxis=dict(
            range=[-5, 110],
            showgrid=False,
            showticklabels=False,
            zeroline=False
        ),
        plot_bgcolor='white',
        paper_bgcolor='#f8f9fa',
        height=700,
        legend=dict(
            x=0.7,
            y=0.98,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='lightgray',
            borderwidth=1
        ),
        margin=dict(l=80, r=20, t=60, b=20)
    )
    
    # แสดงกราฟ
    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# ตารางสรุป
# =====================================================
st.markdown("---")
st.markdown("### 📋 สรุปการคำนวณ")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🔹 E_SB (Subbase Modulus)",
        value=f"{E_SB:,} psi"
    )

with col2:
    st.metric(
        label="🔹 D_SB (Subbase Thickness)",
        value=f"{D_SB:.1f} inches"
    )

with col3:
    st.metric(
        label="🔹 M_R (Roadbed Modulus)",
        value=f"{M_R:,} psi"
    )

with col4:
    st.metric(
        label="🎯 k∞ (Composite k-value)",
        value=f"{k_inf:.0f} pci",
        delta=f"+{(k_inf/k_from_MR - 1)*100:.1f}% from base k"
    )

# =====================================================
# คำอธิบายเพิ่มเติม
# =====================================================
with st.expander("📚 ทฤษฎีและหลักการ"):
    st.markdown("""
    ### Composite Modulus of Subgrade Reaction (k∞)
    
    **k∞** คือ ค่าโมดูลัสปฏิกิริยาของดินใต้ทางแบบผสม (Composite) ที่รวมผลของ:
    1. ความแข็งแรงของดินคันทาง (Roadbed Soil)
    2. ความแข็งแรงของชั้น Subbase
    3. ความหนาของชั้น Subbase
    
    ### สมมติฐานของ Figure 3.3
    
    - **Semi-Infinite Subgrade Depth:** ความลึกของ Subgrade มากกว่า 10 ฟุต จากผิว Subgrade
    - ใช้หลักการ Odemark's Equivalent Thickness Method
    
    ### ขั้นตอนการอ่าน Nomograph
    
    1. เริ่มจากค่า **E_SB** ที่แกนซ้ายบน
    2. ลากเส้นแนวนอนไปตัดเส้นความหนา **D_SB**
    3. จากจุดตัด ลากเส้นลงไปยัง **Turning Line**
    4. จาก Turning Line ลากเส้นไปตัดค่า **M_R** ที่แกนซ้ายล่าง
    5. จากจุดตัด M_R ลากเส้นแนวนอนไปอ่านค่า **k∞**
    
    ### Reference
    
    - AASHTO Guide for Design of Pavement Structures, 1993
    - Part II, Chapter 3: Rigid Pavement Design
    """)

# =====================================================
# Footer
# =====================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #718096; font-size: 0.85rem;'>
    <p>🛣️ AASHTO 1993 Nomograph Calculator | Figure 3.3</p>
    <p>พัฒนาสำหรับการเรียนการสอนวิศวกรรมถนนและผิวทาง</p>
    <p>ภาควิชาครุศาสตร์โยธา มหาวิทยาลัยเทคโนโลยีพระจอมเกล้าพระนครเหนือ</p>
</div>
""", unsafe_allow_html=True)
