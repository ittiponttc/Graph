"""
Streamlit App: โปรแกรมวาดรูปโครงสร้างชั้นทาง (Pavement Structure Graphic Generator)
สามารถกำหนดจำนวนชั้น ความหนา และชนิดวัสดุได้
"""

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib as mpl
from io import BytesIO
import json

# ตั้งค่า font ภาษาไทย (รองรับกรณีไม่มี font)
try:
    mpl.rcParams['font.family'] = 'Garuda'
except:
    pass
mpl.rcParams['axes.unicode_minus'] = False

import matplotlib.font_manager as fm
thai_fonts = ['Garuda', 'TH Sarabun New', 'Sarabun', 'Noto Sans Thai', 'Tahoma']
for font in thai_fonts:
    if font in [f.name for f in fm.fontManager.ttflist]:
        mpl.rcParams['font.family'] = font
        break

# =====================================================
# ตั้งค่าหน้าเว็บ
# =====================================================
st.set_page_config(
    page_title="โปรแกรมวาดโครงสร้างชั้นทาง",
    page_icon="🛣️",
    layout="wide"
)

st.title("🛣️ โปรแกรมวาดรูปโครงสร้างชั้นทาง")
st.markdown("**พัฒนาโดย // รศ.ดร.อิทธิพล มีผล ภาควิชาครุศาสตร์โยธา มจพ.**")
st.markdown("---")

# =====================================================
# วัสดุมาตรฐานที่ใช้บ่อย (Preset Materials)
# =====================================================
PRESET_MATERIALS = {
    "ผิวทางลาดยาง (AC)": {"color": "#1a1a1a", "pattern": "solid"},
    "ผิวทางคอนกรีต (JPCP/JRCP)": {"color": "#a9a9a9", "pattern": "solid"},
    "ผิวทางคอนกรีต (CRCP)": {"color": "#a9a9a9", "pattern": "solid"},
    "รองพื้นทางวัสดุ AC": {"color": "#1a1a1a", "pattern": "solid"},
    "พื้นทาง CTB": {"color": "#d3d3d3", "pattern": "dots"},
    "Lean Concrete Base": {"color": "#c0c0c0", "pattern": "hatch"},
    "หินคลุก (Crushed Rock)": {"color": "#d2b48c", "pattern": "dots"},
    "รองพื้นทางวัสดุมวลรวม": {"color": "#d2a679", "pattern": "solid"},
    "ดินถมคันทาง (Embankment)": {"color": "#f5deb3", "pattern": "solid"},
    "ดินเดิม (Subgrade)": {"color": "#deb887", "pattern": "solid"},
    "ทรายถมคันทาง (Sand Embankment)": {"color": "#f4e4ba", "pattern": "dots"},
    "กำหนดเอง": {"color": "#cccccc", "pattern": "solid"}
}

PATTERN_OPTIONS = {
    "solid": "สีทึบ",
    "dots": "จุดกระจาย",
    "hatch": "เส้นลาย"
}

HATCH_STYLES = {
    "///": "เส้นเอียง ///",
    "\\\\\\": "เส้นเอียง \\\\\\",
    "xxx": "กากบาท xxx",
    "...": "จุด ...",
    "ooo": "วงกลม ooo",
    "+++": "บวก +++"
}

# =====================================================
# ฟังก์ชันวาดโครงสร้างชั้นทาง (ปรับขนาดให้เล็กลง)
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
# Sidebar: ตั้งค่าทั่วไป
# =====================================================
with st.sidebar:
    st.header("⚙️ ตั้งค่าทั่วไป")
    
    # =====================================================
    # Upload JSON
    # =====================================================
    st.markdown("---")
    st.subheader("📂 โหลด/บันทึกข้อมูล")
    
    uploaded_json = st.file_uploader("📂 โหลดข้อมูลจากไฟล์ JSON", type=['json'])
    
    if uploaded_json is not None:
        try:
            loaded_data = json.load(uploaded_json)
            
            # ตรวจสอบว่าเป็นไฟล์ใหม่
            file_id = f"{uploaded_json.name}_{uploaded_json.size}"
            if st.session_state.get('last_uploaded_file') != file_id:
                st.session_state['last_uploaded_file'] = file_id
                
                # อัพเดท session_state สำหรับ chart_title
                st.session_state['input_chart_title'] = loaded_data.get('chart_title', "โครงสร้างชั้นทาง โครงการ......")
                
                # อัพเดท session_state สำหรับ num_layers
                st.session_state['input_num_layers'] = loaded_data.get('num_layers', 4)
                
                # อัพเดท session_state สำหรับ layers
                if 'layers' in loaded_data:
                    num_layers_loaded = len(loaded_data['layers'])
                    st.session_state['input_num_layers'] = num_layers_loaded
                    
                    for i, layer_data in enumerate(loaded_data['layers']):
                        st.session_state[f'input_material_{i}'] = layer_data.get('name', 'กำหนดเอง')
                        st.session_state[f'input_thickness_{i}'] = layer_data.get('thickness', 20)
                        st.session_state[f'input_color_{i}'] = layer_data.get('color', '#cccccc')
                        st.session_state[f'input_pattern_{i}'] = layer_data.get('pattern', 'solid')
                        st.session_state[f'input_hatch_{i}'] = layer_data.get('hatch_style', '///')
                
                st.success("✅ โหลดข้อมูลสำเร็จ!")
                st.rerun()
                
        except Exception as e:
            st.error(f"❌ ไม่สามารถอ่านไฟล์ได้: {e}")
    
    st.markdown("---")
    
    chart_title = st.text_input(
        "หัวข้อรูป", 
        value=st.session_state.get('input_chart_title', "โครงสร้างชั้นทาง โครงการ......"),
        key="input_chart_title"
    )
    
    num_layers = st.number_input(
        "จำนวนชั้น",
        min_value=1,
        max_value=10,
        value=st.session_state.get('input_num_layers', 4),
        step=1,
        key="input_num_layers"
    )
    
    st.markdown("---")
    st.header("📥 โหลดตัวอย่าง")
    
    preset_options = ["-- กำหนดเอง --", "ทางลาดยาง (Flexible)", "ทางคอนกรีต (Rigid)"]
    current_preset = st.session_state.get('input_preset_choice', "-- กำหนดเอง --")
    default_preset_idx = preset_options.index(current_preset) if current_preset in preset_options else 0
    
    preset_choice = st.selectbox(
        "เลือกตัวอย่างโครงสร้าง",
        preset_options,
        index=default_preset_idx,
        key="input_preset_choice"
    )
    
    if st.button("โหลดตัวอย่าง", use_container_width=True):
        if preset_choice == "ทางลาดยาง (Flexible)":
            st.session_state['preset_layers'] = [
                {"name": "ผิวทางลาดยาง (AC)", "thickness": 20, "color": "#1a1a1a", "pattern": "solid"},
                {"name": "พื้นทาง CTB", "thickness": 35, "color": "#d3d3d3", "pattern": "dots"},
                {"name": "รองพื้นทางวัสดุมวลรวม", "thickness": 30, "color": "#d2a679", "pattern": "solid"},
                {"name": "ดินถม (Fill Material)", "thickness": 100, "color": "#f5deb3", "pattern": "solid"}
            ]
            st.rerun()
        elif preset_choice == "ทางคอนกรีต (Rigid)":
            st.session_state['preset_layers'] = [
                {"name": "ผิวทางคอนกรีต (JPCP/JRCP)", "thickness": 28, "color": "#a9a9a9", "pattern": "solid"},
                {"name": "Lean Concrete Base", "thickness": 15, "color": "#c0c0c0", "pattern": "hatch"},
                {"name": "หินคลุก (Crushed Rock)", "thickness": 20, "color": "#d2b48c", "pattern": "dots"},
                {"name": "ดินเดิม (Subgrade)", "thickness": 50, "color": "#deb887", "pattern": "solid"}
            ]
            st.rerun()

# =====================================================
# Main Content: กำหนดชั้นทาง
# =====================================================
st.header("📋 กำหนดรายละเอียดชั้นทาง")

# Initialize layers
layers = []

# สร้าง columns สำหรับแต่ละชั้น
cols_per_row = 2
rows_needed = (int(num_layers) + cols_per_row - 1) // cols_per_row

for row in range(rows_needed):
    cols = st.columns(cols_per_row)
    for col_idx in range(cols_per_row):
        layer_idx = row * cols_per_row + col_idx
        if layer_idx < num_layers:
            with cols[col_idx]:
                st.subheader(f"ชั้นที่ {layer_idx + 1}")
                
                # ตรวจสอบว่ามี preset หรือไม่
                preset_data = None
                if 'preset_layers' in st.session_state and layer_idx < len(st.session_state['preset_layers']):
                    preset_data = st.session_state['preset_layers'][layer_idx]
                
                # เลือกวัสดุ preset
                material_list = list(PRESET_MATERIALS.keys())
                
                # หา default material จาก session_state หรือ preset
                default_material = st.session_state.get(f'input_material_{layer_idx}', None)
                if default_material is None and preset_data:
                    default_material = preset_data['name']
                if default_material is None:
                    default_material = material_list[0]
                
                default_material_idx = material_list.index(default_material) if default_material in material_list else 0
                
                material = st.selectbox(
                    "ประเภทวัสดุ",
                    material_list,
                    index=default_material_idx,
                    key=f"input_material_{layer_idx}"
                )
                
                # ใช้ชื่อวัสดุที่เลือกเป็นป้ายกำกับอัตโนมัติ
                name = material
                
                # ความหนา
                default_thickness = st.session_state.get(f'input_thickness_{layer_idx}', None)
                if default_thickness is None and preset_data:
                    default_thickness = preset_data['thickness']
                if default_thickness is None:
                    default_thickness = 20
                
                thickness = st.number_input(
                    "ความหนา (cm)",
                    min_value=1,
                    max_value=500,
                    value=int(default_thickness),
                    step=5,
                    key=f"input_thickness_{layer_idx}"
                )
                
                # สี
                default_color = st.session_state.get(f'input_color_{layer_idx}', None)
                if default_color is None:
                    default_color = PRESET_MATERIALS[material]['color']
                
                color = st.color_picker(
                    "สี",
                    value=default_color,
                    key=f"input_color_{layer_idx}"
                )
                
                # Pattern
                default_pattern = st.session_state.get(f'input_pattern_{layer_idx}', None)
                if default_pattern is None:
                    default_pattern = PRESET_MATERIALS[material]['pattern']
                
                pattern_keys = list(PATTERN_OPTIONS.keys())
                default_pattern_idx = pattern_keys.index(default_pattern) if default_pattern in pattern_keys else 0
                
                pattern = st.selectbox(
                    "รูปแบบ",
                    pattern_keys,
                    format_func=lambda x: PATTERN_OPTIONS[x],
                    index=default_pattern_idx,
                    key=f"input_pattern_{layer_idx}"
                )
                
                # Hatch style (ถ้าเลือก hatch)
                default_hatch = st.session_state.get(f'input_hatch_{layer_idx}', '///')
                hatch_keys = list(HATCH_STYLES.keys())
                default_hatch_idx = hatch_keys.index(default_hatch) if default_hatch in hatch_keys else 0
                
                hatch_style = "///"
                if pattern == "hatch":
                    hatch_style = st.selectbox(
                        "รูปแบบเส้น",
                        hatch_keys,
                        format_func=lambda x: HATCH_STYLES[x],
                        index=default_hatch_idx,
                        key=f"input_hatch_{layer_idx}"
                    )
                
                # เก็บข้อมูลชั้น
                layers.append({
                    'name': name,
                    'thickness': thickness,
                    'color': color,
                    'pattern': pattern,
                    'hatch_style': hatch_style
                })
                
                st.markdown("---")

# =====================================================
# แสดงผลรูป
# =====================================================
st.header("📊 ผลลัพธ์")

col1, col2 = st.columns([2, 1])

with col1:
    if layers:
        fig = draw_pavement_structure(layers, title=chart_title)
        st.pyplot(fig)
        
        # สร้างปุ่มดาวน์โหลด
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        buf.seek(0)
        
        st.download_button(
            label="📥 ดาวน์โหลดรูป (PNG)",
            data=buf,
            file_name="pavement_structure.png",
            mime="image/png",
            use_container_width=True
        )
        
        plt.close(fig)

with col2:
    st.subheader("📋 สรุปข้อมูล")
    
    total_thickness = sum(layer['thickness'] for layer in layers)
    st.metric("ความหนารวม", f"{total_thickness} cm")
    
    st.markdown("**รายละเอียดแต่ละชั้น:**")
    for i, layer in enumerate(layers):
        with st.expander(f"ชั้นที่ {i+1}: {layer['name']}"):
            st.write(f"- ความหนา: {layer['thickness']} cm")
            st.write(f"- รูปแบบ: {PATTERN_OPTIONS[layer['pattern']]}")
            st.markdown(f"- สี: <span style='background-color:{layer['color']}; padding: 2px 10px; border-radius: 3px;'>&nbsp;&nbsp;&nbsp;</span> {layer['color']}", unsafe_allow_html=True)

# =====================================================
# Download JSON
# =====================================================
st.markdown("---")
st.subheader("💾 บันทึกข้อมูล")

# สร้างข้อมูลสำหรับ export
export_data = {
    'chart_title': chart_title,
    'num_layers': int(num_layers),
    'layers': layers
}

json_str = json.dumps(export_data, ensure_ascii=False, indent=2)

st.download_button(
    label="💾 Download Input (JSON)",
    data=json_str,
    file_name="pavement_structure_data.json",
    mime="application/json",
    use_container_width=True
)

# =====================================================
# Footer
# =====================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    พัฒนาสำหรับงานวิศวกรรมทาง | Pavement Structure Graphic Generator<br>
    สามารถปรับแต่งจำนวนชั้น ความหนา และวัสดุได้ตามต้องการ
</div>
""", unsafe_allow_html=True)
