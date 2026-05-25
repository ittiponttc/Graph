"""
Streamlit App: โปรแกรมวาดรูปโครงสร้างชั้นทาง (Pavement Structure Graphic Generator)
v2.0 - Two-Column Layout, Blue Theme, Live Preview
พัฒนาโดย รศ.ดร.อิทธิพล มีผล ภาควิชาครุศาสตร์โยธา มจพ.
"""

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib as mpl
from io import BytesIO
import json

# =====================================================
# ตั้งค่า Font ภาษาไทย
# =====================================================
import matplotlib.font_manager as fm
thai_fonts = ['Garuda', 'TH Sarabun New', 'Sarabun', 'Noto Sans Thai', 'Tahoma']
for font in thai_fonts:
    if font in [f.name for f in fm.fontManager.ttflist]:
        mpl.rcParams['font.family'] = font
        break
mpl.rcParams['axes.unicode_minus'] = False

# =====================================================
# ตั้งค่าหน้าเว็บ
# =====================================================
st.set_page_config(
    page_title="Pavement Structure Generator",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# CSS Theme — สีฟ้าอ่อน Engineering
# =====================================================
st.markdown("""
<style>
/* ── Base & Background ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #eaf4fb 0%, #f4f9fe 60%, #e8f3fa 100%);
}
[data-testid="stHeader"] {
    background: transparent;
}

/* ── App Header ── */
.app-header {
    background: linear-gradient(135deg, #1565c0 0%, #1976d2 50%, #42a5f5 100%);
    border-radius: 14px;
    padding: 20px 28px 16px 28px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(21,101,192,0.25);
    display: flex;
    align-items: center;
    gap: 16px;
}
.app-header-icon { font-size: 2.4rem; }
.app-header-title {
    font-size: 1.55rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 0.02em;
    line-height: 1.2;
    margin: 0;
}
.app-header-sub {
    font-size: 0.82rem;
    color: rgba(255,255,255,0.82);
    margin: 3px 0 0 0;
}

/* ── Panel Cards ── */
.panel-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 14px;
    box-shadow: 0 2px 10px rgba(21,101,192,0.08);
    border: 1px solid rgba(21,101,192,0.10);
}
.panel-title {
    font-size: 0.92rem;
    font-weight: 700;
    color: #1565c0;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 14px;
    padding-bottom: 8px;
    border-bottom: 2px solid #e3f2fd;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* ── Layer Cards ── */
.layer-card {
    background: #f0f7ff;
    border-left: 4px solid #1976d2;
    border-radius: 0 8px 8px 0;
    padding: 12px 14px;
    margin-bottom: 10px;
}
.layer-badge {
    display: inline-block;
    background: #1976d2;
    color: white;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 2px 9px;
    border-radius: 10px;
    margin-bottom: 8px;
    letter-spacing: 0.05em;
}

/* ── Metric Card ── */
.metric-card {
    background: linear-gradient(135deg, #1565c0, #1e88e5);
    border-radius: 10px;
    padding: 14px 18px;
    text-align: center;
    color: white;
    margin-bottom: 12px;
    box-shadow: 0 3px 12px rgba(21,101,192,0.20);
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
}
.metric-label {
    font-size: 0.78rem;
    opacity: 0.88;
    margin-top: 3px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── Summary Table ── */
.summary-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0 4px;
    font-size: 0.83rem;
}
.summary-table thead tr th {
    background: #1565c0;
    color: white;
    padding: 7px 10px;
    font-weight: 600;
    letter-spacing: 0.04em;
    font-size: 0.78rem;
}
.summary-table thead tr th:first-child { border-radius: 6px 0 0 6px; }
.summary-table thead tr th:last-child  { border-radius: 0 6px 6px 0; }
.summary-table tbody tr td {
    background: #f8fbff;
    padding: 6px 10px;
    border-top: 1px solid #e3f2fd;
    border-bottom: 1px solid #e3f2fd;
    color: #263238;
}
.summary-table tbody tr td:first-child {
    border-left: 1px solid #e3f2fd;
    border-radius: 6px 0 0 6px;
}
.summary-table tbody tr td:last-child {
    border-right: 1px solid #e3f2fd;
    border-radius: 0 6px 6px 0;
}
.summary-table tbody tr:hover td { background: #e8f4fd; }

/* ── Streamlit Widgets Override ── */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    border: 1.5px solid #bbdefb !important;
    border-radius: 7px !important;
    background: #f7fbff !important;
}
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextInput"] input:focus {
    border-color: #1976d2 !important;
    box-shadow: 0 0 0 2px rgba(25,118,210,0.15) !important;
}
div[data-testid="stSelectbox"] > div > div {
    border: 1.5px solid #bbdefb !important;
    border-radius: 7px !important;
    background: #f7fbff !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #1565c0, #1976d2) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.45rem 1rem !important;
    transition: all 0.2s !important;
    box-shadow: 0 2px 8px rgba(21,101,192,0.20) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(21,101,192,0.30) !important;
    background: linear-gradient(135deg, #0d47a1, #1565c0) !important;
}
.stDownloadButton > button {
    background: linear-gradient(135deg, #0277bd, #0288d1) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(2,119,189,0.20) !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(2,119,189,0.30) !important;
}

/* ── Divider ── */
hr { border-color: #bbdefb !important; }

/* ── Expander ── */
details { border: 1px solid #bbdefb !important; border-radius: 8px !important; }
details summary { color: #1565c0 !important; font-weight: 600 !important; }

/* ── Success/Error ── */
div[data-testid="stAlert"] { border-radius: 8px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #e3f2fd; border-radius: 3px; }
::-webkit-scrollbar-thumb { background: #90caf9; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #1976d2; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# App Header
# =====================================================
st.markdown("""
<div class="app-header">
    <div class="app-header-icon">🛣️</div>
    <div>
        <div class="app-header-title">Pavement Structure Generator</div>
        <div class="app-header-sub">รศ.ดร.อิทธิพล มีผล &nbsp;|&nbsp; ภาควิชาครุศาสตร์โยธา มจพ. &nbsp;|&nbsp; AASHTO 1993</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# วัสดุมาตรฐาน (Preset Materials)
# =====================================================
PRESET_MATERIALS = {
    "ผิวทางลาดยาง (AC)":                   {"color": "#1a1a1a", "pattern": "solid"},
    "ผิวทางคอนกรีต (JPCP/JRCP)":           {"color": "#a0a0a0", "pattern": "solid"},
    "ผิวทางคอนกรีต (CRCP)":                {"color": "#a0a0a0", "pattern": "solid"},
    "รองพื้นทางวัสดุ AC":                  {"color": "#2a2a2a", "pattern": "solid"},
    "พื้นทาง CTB":                          {"color": "#c8c8c8", "pattern": "hatch"},
    "Lean Concrete Base":                   {"color": "#b8b8b8", "pattern": "hatch"},
    "หินคลุก (Crushed Rock)":              {"color": "#c8a96e", "pattern": "dots"},
    "หินคลุกผสมซีเมนต์ (MOD.Crushed Rock)":    {"color": "#b0c4a0", "pattern": "hatch"},
    "รองพื้นทางวัสดุมวลรวม":              {"color": "#d4a06a", "pattern": "solid"},
    "ดินถมคันทาง (Embankment)":            {"color": "#e8d4a0", "pattern": "solid"},
    "ดินเดิม (Subgrade)":                  {"color": "#c8a87a", "pattern": "solid"},
    "ทรายถมคันทาง (Sand Embankment)":      {"color": "#f0dca0", "pattern": "dots"},
    "กำหนดเอง":                            {"color": "#cccccc", "pattern": "solid"},
}

PATTERN_OPTIONS = {
    "solid": "สีทึบ",
    "dots":  "จุดกระจาย",
    "hatch": "เส้นลาย",
}

HATCH_STYLES = {
    "///":  "เส้นเอียง ///",
    "\\\\\\": "เส้นเอียง \\\\\\",
    "xxx":  "กากบาท xxx",
    "...":  "จุด ...",
    "ooo":  "วงกลม ooo",
    "+++":  "บวก +++",
}

# =====================================================
# ฟังก์ชันวาดโครงสร้างชั้นทาง
# =====================================================
def draw_pavement_structure(layers, figsize=(10,6), title="โครงสร้างชั้นทาง"):
    """
    วาดรูปโครงสร้างชั้นทาง (ขนาดกะทัดรัด)
    """
    # คำนวณความหนารวม
    total_thickness = sum(layer['thickness'] for layer in layers)
    # ปรับ figsize ตามความหนารวม (ให้สั้นลง)
    fig_height = max(4, min(8, total_thickness / 30))
    fig, ax = plt.subplots(figsize=(figsize[0], fig_height))
    
    # กำหนดขนาดของรูป - ใช้ scale factor เพื่อให้รูปกะทัดรัด
    scale = 100 / max(total_thickness, 100)  # normalize ให้ความสูงไม่เกิน 100 units
    layer_width = 6
    x_start = 2
    
    # วาดแต่ละชั้นจากบนลงล่าง
    current_y = total_thickness * scale
    
    for i, layer in enumerate(layers):
        thickness = layer['thickness'] * scale
        color = layer.get('color', 'gray')
        pattern = layer.get('pattern', 'solid')
        hatch_style = layer.get('hatch_style', '///')
        name = layer.get('name', f'Layer {i+1}')
        
        # คำนวณตำแหน่ง y
        y_bottom = current_y - thickness
        
        # สร้าง rectangle
        if pattern == 'dots':
            rect = patches.Rectangle(
                (x_start, y_bottom), layer_width, thickness,
                linewidth=1.5, edgecolor='black', facecolor=color
            )
            ax.add_patch(rect)
            
            # เพิ่มจุด pattern
            np.random.seed(i * 42)
            n_dots = int(thickness * layer_width * 0.5)
            if n_dots > 0 and thickness > 2:
                dot_x = np.random.uniform(x_start + 0.2, x_start + layer_width - 0.2, n_dots)
                dot_y = np.random.uniform(y_bottom + thickness*0.1, y_bottom + thickness*0.9, n_dots)
                ax.scatter(dot_x, dot_y, s=10, c='gray', alpha=0.5)
                
        elif pattern == 'hatch':
            rect = patches.Rectangle(
                (x_start, y_bottom), layer_width, thickness,
                linewidth=1, edgecolor='black', facecolor=color,
                hatch=hatch_style
            )
            ax.add_patch(rect)
        else:
            rect = patches.Rectangle(
                (x_start, y_bottom), layer_width, thickness,
                linewidth=1, edgecolor='black', facecolor=color
            )
            ax.add_patch(rect)
        
        # เพิ่มเส้นบอกขนาด (dimension line) ด้านซ้าย - แสดงความหนาจริง
        dim_x = x_start - 1.5
        ax.annotate('', xy=(dim_x, y_bottom), xytext=(dim_x, current_y),
                   arrowprops=dict(arrowstyle='<->', color='black', lw=0.1))
        ax.text(dim_x - 5, (y_bottom + current_y) / 2, f'{int(layer["thickness"])} cm',
               ha='center', va='center', fontsize=8, rotation=0)
        
        # เพิ่มชื่อวัสดุด้านขวา
        ax.text(x_start + layer_width + 0.7, (y_bottom + current_y) / 2, name,
               ha='left', va='center', fontsize=8)
        
        current_y = y_bottom
    
    # ตั้งค่าแกน
    ax.set_xlim(-0.5, 14)
    ax.set_ylim(-8, total_thickness * scale + 12)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # เพิ่มหัวข้อ
    ax.text(x_start + layer_width/2, total_thickness * scale + 6, title,
           ha='center', va='center', fontsize=10, fontweight='bold')
    
    # เพิ่ม "Not to Scale"
    ax.text(x_start + layer_width, -4, 'Not to Scale',
           ha='right', va='center', fontsize=5, style='italic')
    
    plt.tight_layout()
    return fig

# =====================================================
# Session State Helpers
# =====================================================
def get_ss(key, default):
    return st.session_state.get(key, default)

# =====================================================
# MAIN LAYOUT — Two-Column Split
# col_left (40%) = Input   |   col_right (60%) = Output
# =====================================================
col_left, col_right = st.columns([4, 6], gap="large")

# ─────────────────────────────────────────────────────
# LEFT COLUMN — Input Panel
# ─────────────────────────────────────────────────────
with col_left:

    # ── โหลด JSON ──
    st.markdown('<div class="panel-card">'
                '<div class="panel-title">📂 โหลด / บันทึกข้อมูล</div>',
                unsafe_allow_html=True)

    uploaded_json = st.file_uploader("โหลดข้อมูลจากไฟล์ JSON",
                                     type=['json'], label_visibility="collapsed")

    if uploaded_json is not None:
        try:
            loaded_data = json.load(uploaded_json)
            file_id = f"{uploaded_json.name}_{uploaded_json.size}"
            if get_ss('last_uploaded_file', '') != file_id:
                st.session_state['last_uploaded_file'] = file_id
                st.session_state['input_chart_title'] = loaded_data.get(
                    'chart_title', "โครงสร้างชั้นทาง โครงการ......")
                layers_data = loaded_data.get('layers', [])
                st.session_state['input_num_layers'] = len(layers_data)
                for i, ld in enumerate(layers_data):
                    st.session_state[f'input_material_{i}']  = ld.get('name', 'กำหนดเอง')
                    st.session_state[f'input_thickness_{i}'] = ld.get('thickness', 20)
                    st.session_state[f'input_color_{i}']     = ld.get('color', '#cccccc')
                    st.session_state[f'input_pattern_{i}']   = ld.get('pattern', 'solid')
                    st.session_state[f'input_hatch_{i}']     = ld.get('hatch_style', '///')
                st.success("✅ โหลดข้อมูลสำเร็จ!")
                st.rerun()
        except Exception as e:
            st.error(f"❌ ไม่สามารถอ่านไฟล์ได้: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

    # ── ตั้งค่าทั่วไป ──
    st.markdown('<div class="panel-card">'
                '<div class="panel-title">⚙️ ตั้งค่าทั่วไป</div>',
                unsafe_allow_html=True)

    chart_title = st.text_input(
        "หัวข้อรูป",
        value=get_ss('input_chart_title', "โครงสร้างชั้นทาง โครงการ......"),
        key="input_chart_title",
        placeholder="ระบุชื่อโครงการ..."
    )

    col_n, col_p = st.columns([1, 2])
    with col_n:
        num_layers = st.number_input(
            "จำนวนชั้น", min_value=1, max_value=10,
            value=get_ss('input_num_layers', 4), step=1,
            key="input_num_layers"
        )
    with col_p:
        preset_options = ["-- กำหนดเอง --", "ทางลาดยาง (Flexible)", "ทางคอนกรีต (Rigid)"]
        preset_choice = st.selectbox(
            "โหลดตัวอย่าง", preset_options,
            index=0, key="input_preset_choice"
        )

    if st.button("⚡ โหลดตัวอย่าง", use_container_width=True):
        if preset_choice == "ทางลาดยาง (Flexible)":
            preset = [
                {"name": "ผิวทางลาดยาง (AC)",            "thickness": 20, "color": "#1a1a1a", "pattern": "solid"},
                {"name": "พื้นทาง CTB",                   "thickness": 35, "color": "#c8c8c8", "pattern": "hatch"},
                {"name": "รองพื้นทางวัสดุมวลรวม",        "thickness": 30, "color": "#d4a06a", "pattern": "solid"},
                {"name": "ดินถมคันทาง (Embankment)",      "thickness": 100,"color": "#e8d4a0", "pattern": "solid"},
            ]
        elif preset_choice == "ทางคอนกรีต (Rigid)":
            preset = [
                {"name": "ผิวทางคอนกรีต (JPCP/JRCP)",   "thickness": 28, "color": "#a0a0a0", "pattern": "solid"},
                {"name": "Lean Concrete Base",             "thickness": 15, "color": "#b8b8b8", "pattern": "hatch"},
                {"name": "หินคลุก (Crushed Rock)",        "thickness": 20, "color": "#c8a96e", "pattern": "dots"},
                {"name": "ดินเดิม (Subgrade)",            "thickness": 50, "color": "#c8a87a", "pattern": "solid"},
            ]
        else:
            preset = None

        if preset:
            st.session_state['input_num_layers'] = len(preset)
            for i, p in enumerate(preset):
                st.session_state[f'input_material_{i}']  = p['name']
                st.session_state[f'input_thickness_{i}'] = p['thickness']
                st.session_state[f'input_color_{i}']     = p['color']
                st.session_state[f'input_pattern_{i}']   = p['pattern']
                st.session_state[f'input_hatch_{i}']     = p.get('hatch_style', '///')
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # ── รายละเอียดแต่ละชั้น ──
    st.markdown('<div class="panel-card">'
                '<div class="panel-title">📋 รายละเอียดชั้นทาง</div>',
                unsafe_allow_html=True)

    layers = []
    material_list = list(PRESET_MATERIALS.keys())

    for i in range(int(num_layers)):
        st.markdown(f'<div class="layer-badge">ชั้นที่ {i + 1}</div>', unsafe_allow_html=True)

        # Material
        saved_mat = get_ss(f'input_material_{i}', None)
        default_mat_idx = material_list.index(saved_mat) if saved_mat in material_list else 0
        material = st.selectbox(
            "ประเภทวัสดุ", material_list,
            index=default_mat_idx, key=f"input_material_{i}",
            label_visibility="collapsed"
        )

        c1, c2, c3 = st.columns([3, 2, 2])
        with c1:
            default_t = get_ss(f'input_thickness_{i}', 20)
            thickness = st.number_input(
                "ความหนา (cm)", min_value=1, max_value=500,
                value=int(default_t), step=5, key=f"input_thickness_{i}"
            )
        with c2:
            default_col = get_ss(f'input_color_{i}', None) or PRESET_MATERIALS[material]['color']
            color = st.color_picker("สี", value=default_col, key=f"input_color_{i}")
        with c3:
            default_pat = get_ss(f'input_pattern_{i}', None) or PRESET_MATERIALS[material]['pattern']
            pat_keys = list(PATTERN_OPTIONS.keys())
            def_pat_idx = pat_keys.index(default_pat) if default_pat in pat_keys else 0
            pattern = st.selectbox(
                "รูปแบบ", pat_keys,
                format_func=lambda x: PATTERN_OPTIONS[x],
                index=def_pat_idx, key=f"input_pattern_{i}"
            )

        # Hatch style
        hatch_style = "///"
        if pattern == "hatch":
            default_h = get_ss(f'input_hatch_{i}', '///')
            h_keys = list(HATCH_STYLES.keys())
            def_h_idx = h_keys.index(default_h) if default_h in h_keys else 0
            hatch_style = st.selectbox(
                "รูปแบบเส้น", h_keys,
                format_func=lambda x: HATCH_STYLES[x],
                index=def_h_idx, key=f"input_hatch_{i}"
            )

        layers.append({
            'name':        material,
            'thickness':   thickness,
            'color':       color,
            'pattern':     pattern,
            'hatch_style': hatch_style,
        })

        if i < int(num_layers) - 1:
            st.markdown("<hr style='margin:8px 0; border-color:#bbdefb'>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────
# RIGHT COLUMN — Output Panel
# ─────────────────────────────────────────────────────
with col_right:

    # ── รูปโครงสร้างชั้นทาง ──
    st.markdown('<div class="panel-card">'
                '<div class="panel-title">📊 รูปโครงสร้างชั้นทาง</div>',
                unsafe_allow_html=True)

    if layers:
        fig = draw_pavement_structure(layers, title=chart_title)
        st.pyplot(fig, use_container_width=True)

        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=300, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        buf.seek(0)
        plt.close(fig)

        st.download_button(
            label="📥 ดาวน์โหลดรูป (PNG, 300 dpi)",
            data=buf,
            file_name="pavement_structure.png",
            mime="image/png",
            use_container_width=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # ── สรุปข้อมูล ──
    st.markdown('<div class="panel-card">'
                '<div class="panel-title">📋 สรุปข้อมูลชั้นทาง</div>',
                unsafe_allow_html=True)

    if layers:
        total_thickness = sum(layer['thickness'] for layer in layers)

        # Metric card
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_thickness} <span style="font-size:1.1rem">cm</span></div>
            <div class="metric-label">ความหนารวมทั้งหมด</div>
        </div>
        """, unsafe_allow_html=True)

        # Summary table
        rows_html = ""
        for i, layer in enumerate(layers):
            swatch = (f"<span style='display:inline-block;width:16px;height:14px;"
                      f"background:{layer['color']};border:1px solid #888;"
                      f"border-radius:3px;vertical-align:middle;margin-right:5px'></span>")
            rows_html += f"""
            <tr>
                <td style="text-align:center;font-weight:700;color:#1565c0">{i+1}</td>
                <td>{layer['name']}</td>
                <td style="text-align:center">{layer['thickness']} cm</td>
                <td style="text-align:center">{PATTERN_OPTIONS[layer['pattern']]}</td>
                <td style="text-align:center">{swatch}</td>
            </tr>"""

        st.markdown(f"""
        <table class="summary-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>วัสดุ</th>
                    <th>หนา</th>
                    <th>รูปแบบ</th>
                    <th>สี</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── บันทึก JSON ──
    st.markdown('<div class="panel-card">'
                '<div class="panel-title">💾 บันทึกข้อมูล JSON</div>',
                unsafe_allow_html=True)

    export_data = {
        'chart_title': chart_title,
        'num_layers':  int(num_layers),
        'layers':      layers,
    }
    json_str = json.dumps(export_data, ensure_ascii=False, indent=2)

    st.download_button(
        label="💾 Download ข้อมูล (JSON)",
        data=json_str,
        file_name="pavement_structure_data.json",
        mime="application/json",
        use_container_width=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# Footer
# =====================================================
st.markdown("""
<div style='text-align:center;color:#90a4ae;font-size:11px;padding:12px 0 4px;'>
    Pavement Structure Generator &nbsp;|&nbsp;
    พัฒนาสำหรับงานวิศวกรรมทาง &nbsp;|&nbsp;
    ภาควิชาครุศาสตร์โยธา มจพ.
</div>
""", unsafe_allow_html=True)
