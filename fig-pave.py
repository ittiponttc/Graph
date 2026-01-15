 # แสดงรูปโครงสร้างชั้นทาง
        st.markdown("**📐 รูปโครงสร้างชั้นทาง**")
        
        # สร้างรูป
        fig_structure = create_pavement_structure_figure(layers_data, concrete_thickness_cm=None)
        
        if fig_structure:
            st.pyplot(fig_structure)
            
            # ปุ่มดาวน์โหลดรูป
            img_buffer = save_figure_to_bytes(fig_structure)
            st.download_button(
                label="📥 ดาวน์โหลดรูปโครงสร้างชั้นทาง",
                data=img_buffer,
                file_name=f"pavement_structure_{datetime.now().strftime('%Y%m%d_%H%M')}.png",
                mime="image/png"
            )
            plt.close(fig_structure)
        
        st.markdown("---")
        
        # 1. ESAL ที่ต้องการรองรับ
        st.subheader("1️⃣ ปริมาณจราจร")
        
        # แสดงตัวช่วยประมาณ ESAL
        with st.expander("📊 ตัวช่วยประมาณ ESAL ตามประเภทถนน"):
            st.markdown("""
            | ประเภทถนน | ESAL (20 ปี) |
            |-----------|--------------|
            | ถนนในหมู่บ้าน | 50,000 - 200,000 |
            | ถนนเทศบาล | 200,000 - 500,000 |
            | ถนน อบจ. / ทางหลวงชนบท | 500,000 - 2,000,000 |
            | ทางหลวงแผ่นดิน (2 ช่องจราจร) | 2,000,000 - 10,000,000 |
            | ทางหลวงแผ่นดิน (4 ช่องจราจร) | 10,000,000 - 50,000,000 |
            """)
        
        w18_design = st.number_input(
            "ESAL ที่ต้องการรองรับ (W₁₈)",
            min_value=10_000,
            max_value=500_000_000,
            value=500_000,
            step=100_000,
            format="%d",
            help="จำนวน Equivalent Single Axle Load (18 kip) ตลอดอายุการใช้งาน"
        )
        
        st.markdown("---")
        
        # 2. Serviceability
        st.subheader("2️⃣ Serviceability")
        pt = st.slider(
            "Terminal Serviceability (Pt)",
            min_value=1.5,
            max_value=3.0,
            value=2.0,
            step=0.1,
            help="ค่า Serviceability ที่ยอมรับได้ต่ำสุด (มาตรฐาน = 2.0)"
        )
        
        # คำนวณ ΔPSI
        delta_psi = 4.5 - pt
        st.info(f"ΔPSI = 4.5 - {pt:.1f} = **{delta_psi:.1f}**")
        
        st.markdown("---")
        
        # 3. Reliability
        st.subheader("3️⃣ ความเชื่อมั่นในการออกแบบ")
        reliability = st.select_slider(
            "Reliability (R)",
            options=[80, 85, 90, 95],
            value=90,
            help="ระดับความเชื่อมั่นในการออกแบบ (%)"
        )
        
        # หาค่า ZR
        zr = get_zr_value(reliability)
        st.info(f"ZR = **{zr:.3f}** (จากตาราง AASHTO)")
        
        # Standard Deviation
        so = st.number_input(
            "Overall Standard Deviation (So)",
            min_value=0.30,
            max_value=0.45,
            value=0.35,
            step=0.01,
            format="%.2f",
            help="ค่าเบี่ยงเบนมาตรฐานรวม (มาตรฐาน = 0.35 สำหรับ Rigid Pavement)"
        )
        
        st.markdown("---")
        
        # 4. คุณสมบัติดินฐานราก
        st.subheader("4️⃣ คุณสมบัติดินฐานราก")
        
        with st.expander("📊 ตารางประมาณค่า k จาก CBR"):
            st.markdown("""
            | CBR (%) | k (pci) | คำอธิบาย |
            |---------|---------|----------|
            | 2-3 | 75-100 | ดินเหนียวอ่อน |
            | 4-5 | 100-130 | ดินเหนียวแข็ง |
            | 6-10 | 130-170 | ดินทรายปนดินเหนียว |
            | 10-20 | 170-230 | ดินทรายอัดแน่น |
            | 20-50 | 230-350 | หินคลุก/ลูกรัง |
            | > 50 | 350-500+ | ชั้น Base คุณภาพดี |
            
            **หมายเหตุ:** ค่า k_eff รวมผลของชั้น Subbase แล้ว
            """)
        
        k_eff = st.number_input(
            "Effective Modulus of Subgrade Reaction (k_eff)",
            min_value=50,
            max_value=1000,
            value=200,
            step=25,
            format="%d",
            help="ค่า k จากการทดสอบ Plate Bearing Test หรือประมาณจาก CBR (หน่วย: pci)"
        )
        
        # Loss of Support (LS)
        st.markdown("**Loss of Support (LS)**")
        
        with st.expander("📊 ตารางค่า Loss of Support แนะนำ (AASHTO 1993)"):
            st.markdown("""
            | ประเภทวัสดุ | Loss of Support (LS) |
            |------------|---------------------|
            | Cement Treated Granular Base | 0.0 - 1.0 |
            | Cement Aggregate Mixtures | 0.0 - 1.0 |
            | Asphalt Treated Base | 0.0 - 1.0 |
            | Bituminous Stabilized Mixtures | 0.0 - 1.0 |
            | Lime Stabilized | 1.0 - 3.0 |
            | Unbound Granular Materials | 1.0 - 3.0 |
            | Fine Grained or Natural Subgrade | 2.0 - 3.0 |
            
            **หมายเหตุ:** ค่า LS ใช้ปรับลดค่า k_eff เพื่อคำนึงถึงการสูญเสียการรองรับจากการกัดเซาะ
            """)
        
        ls_value = st.number_input(
            "ค่า Loss of Support (LS)",
            min_value=0.0,
            max_value=3.0,
            value=1.0,
            step=0.5,
            format="%.1f",
            help="ค่า LS สำหรับปรับลด k_eff (0.0-3.0)"
        )
        
        st.markdown("---")
        
        # 5. คุณสมบัติคอนกรีต
        st.subheader("5️⃣ คุณสมบัติคอนกรีต")
        
        fc_cube = st.number_input(
            "กำลังอัดคอนกรีต (Cube) - f'c",
            min_value=200,
            max_value=600,
            value=350,
            step=10,
            format="%d",
            help="กำลังอัดคอนกรีตที่ 28 วัน ทดสอบด้วย Cube 15×15×15 ซม. (หน่วย: ksc)"
        )
        
        # แปลง Cube เป็น Cylinder
        fc_cylinder = convert_cube_to_cylinder(fc_cube)
        st.info(f"f'c (Cylinder) = 0.8 × {fc_cube} = **{fc_cylinder:.0f} ksc**")
        
        # คำนวณ Ec
        ec = calculate_concrete_modulus(fc_cylinder)
        st.info(f"Ec = 57,000 × √({fc_cylinder * 14.223:.0f}) = **{ec:,.0f} psi**")
        
        # Modulus of Rupture
        st.markdown("**Modulus of Rupture (Sc)**")
        
        # คำนวณค่า Sc อัตโนมัติ
        sc_auto = estimate_modulus_of_rupture(fc_cylinder)
        st.info(f"ค่าประมาณ: Sc = 10 × √({fc_cylinder * 14.223:.0f}) = **{sc_auto:.0f} psi**")
        
        # ให้ผู้ใช้ป้อนค่าที่ต้องการใช้
        sc = st.number_input(
            "ค่า Sc ที่ใช้ในการคำนวณ (psi)",
            min_value=400,
            max_value=1000,
            value=int(round(sc_auto)),
            step=10,
            format="%d",
            help="ค่าเริ่มต้นคำนวณจาก 10×√f'c สามารถแก้ไขได้ตามผลทดสอบจริง"
        )
        
        st.markdown("---")
        
        # 6. Load Transfer และ Drainage
        st.subheader("6️⃣ Load Transfer และ Drainage")
        
        # แสดงค่า J อัตโนมัติตามประเภทถนน
        j_auto = J_VALUES[pavement_type]
        st.info(f"ค่าแนะนำสำหรับ {pavement_type}: **J = {j_auto}**")
        
        # ตารางอ้างอิงค่า J
        with st.expander("📊 ตารางค่า Load Transfer Coefficient (J)"):
            st.markdown("""
            | ประเภทถนน | J (Tied Shoulder) | J (AC Shoulder) |
            |-----------|-------------------|-----------------|
            | JPCP + Dowel Bar | 2.7 | 3.2 |
            | JPCP ไม่มี Dowel | 3.2 | 3.8-4.4 |
            | CRCP | 2.3 | 2.9 |
            
            **หมายเหตุ:** ค่า J ต่ำ = การถ่ายแรงดี = รองรับ ESAL ได้มากขึ้น
            """)
        
        # ให้ผู้ใช้ป้อนค่าที่ต้องการใช้
        j_value = st.number_input(
            "ค่า J ที่ใช้ในการคำนวณ",
            min_value=2.0,
            max_value=4.5,
            value=j_auto,
            step=0.1,
            format="%.1f",
            help="ค่าเริ่มต้นตามประเภทถนนที่เลือก สามารถแก้ไขได้"
        )
        
        cd = st.number_input(
            "Drainage Coefficient (Cd)",
            min_value=0.7,
            max_value=1.3,
            value=1.0,
            step=0.05,
            format="%.2f",
            help="สัมประสิทธิ์การระบายน้ำ (1.0 = การระบายน้ำปานกลาง)"
        )
        
        st.markdown("---")
        
        # 7. ความหนาคอนกรีต
        st.subheader("7️⃣ ความหนาคอนกรีตที่ต้องการตรวจสอบ")
        d_selected = st.slider(
            "ความหนาคอนกรีต D (นิ้ว)",
            min_value=8,
            max_value=16,
            value=12,
            step=1,
            help="ความหนาแผ่นพื้นคอนกรีต"
        )
        st.info(f"D = {d_selected} นิ้ว = **{d_selected * 2.54:.1f} ซม.**")
    
    # ============================================================
    # ส่วนแสดงผลการคำนวณ
    # ============================================================
    
    with col2:
        st.header("📊 ผลการคำนวณ (Output)")
        
        # เก็บผลการคำนวณสำหรับความหนาต่างๆ
        comparison_results = []
        thicknesses = [8, 9, 10, 11, 12, 13, 14, 15, 16]
        
        # คำนวณสำหรับแต่ละความหนา
        st.subheader("📋 ตารางเปรียบเทียบความหนาต่างๆ")
        
        # สร้างตาราง
        table_data = []
        for d in thicknesses:
            log_w18, w18_capacity = calculate_aashto_rigid_w18(
                d_inch=d,
                delta_psi=delta_psi,
                pt=pt,
                zr=zr,
                so=so,
                sc_psi=sc,
                cd=cd,
                j=j_value,
                ec_psi=ec,
                k_pci=k_eff
            )
            passed, ratio = check_design(w18_design, w18_capacity)
            
            comparison_results.append({
                'd': d,
                'log_w18': log_w18,
                'w18': w18_capacity,
                'passed': passed,
                'ratio': ratio
            })
            
            table_data.append({
                'D (นิ้ว)': d,
                'D (ซม.)': f"{d * 2.54:.1f}",
                'log₁₀(W₁₈)': f"{log_w18:.4f}",
                'W₁₈ รองรับได้': f"{w18_capacity:,.0f}",
                'อัตราส่วน': f"{ratio:.2f}",
                'ผล': "✅ ผ่าน" if passed else "❌ ไม่ผ่าน"
            })
        
        # แสดงตาราง
        import pandas as pd
        df = pd.DataFrame(table_data)
        
        # จัดรูปแบบตาราง
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("---")
        
        # ผลการคำนวณสำหรับความหนาที่เลือก
        st.subheader(f"🎯 ผลการตรวจสอบ D = {d_selected} นิ้ว")
        
        log_w18_selected, w18_selected = calculate_aashto_rigid_w18(
            d_inch=d_selected,
            delta_psi=delta_psi,
            pt=pt,
            zr=zr,
            so=so,
            sc_psi=sc,
            cd=cd,
            j=j_value,
            ec_psi=ec,
            k_pci=k_eff
        )
        passed_selected, ratio_selected = check_design(w18_design, w18_selected)
        
        # แสดงผลด้วยสี
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.metric(
                label="log₁₀(W₁₈)",
                value=f"{log_w18_selected:.4f}"
            )
            st.metric(
                label="W₁₈ รองรับได้",
                value=f"{w18_selected:,.0f}",
                delta=f"{w18_selected - w18_design:+,.0f}"
            )
        
        with col_b:
            st.metric(
                label="W₁₈ ที่ต้องการ",
                value=f"{w18_design:,.0f}"
            )
            st.metric(
                label="อัตราส่วน (Capacity/Required)",
                value=f"{ratio_selected:.2f}"
            )
        
        # แสดงผลผ่าน/ไม่ผ่าน
        if passed_selected:
            st.success(f"""
            ✅ **ผ่านเกณฑ์การออกแบบ**
            
            ความหนา D = {d_selected} นิ้ว ({d_selected * 2.54:.1f} ซม.) 
            สามารถรองรับ ESAL ได้ {w18_selected:,.0f} ESALs
            ซึ่งมากกว่า ESAL ที่ต้องการ {w18_design:,.0f} ESALs
            
            อัตราส่วน = {ratio_selected:.2f} (≥ 1.00)
            """)
        else:
            st.error(f"""
            ❌ **ไม่ผ่านเกณฑ์การออกแบบ**
            
            ความหนา D = {d_selected} นิ้ว ({d_selected * 2.54:.1f} ซม.) 
            รองรับ ESAL ได้เพียง {w18_selected:,.0f} ESALs
            ซึ่งน้อยกว่า ESAL ที่ต้องการ {w18_design:,.0f} ESALs
            
            อัตราส่วน = {ratio_selected:.2f} (< 1.00)
            
            **กรุณาเพิ่มความหนาคอนกรีต หรือปรับปรุงคุณสมบัติวัสดุ**
            """)
        
        st.markdown("---")
        
        # แสดงสมการที่ใช้
        st.subheader("📝 สมการ AASHTO 1993")
        
        st.latex(r'''
        \log_{10}(W_{18}) = Z_R \times S_o + 7.35 \times \log_{10}(D+1) - 0.06
        ''')
        
        st.latex(r'''
        + \frac{\log_{10}\left(\frac{\Delta PSI}{4.5-1.5}\right)}{1 + \frac{1.624 \times 10^7}{(D+1)^{8.46}}}
        ''')
        
        st.latex(r'''
        + (4.22 - 0.32 \times P_t) \times \log_{10}\left[\frac{S_c \times C_d \times (D^{0.75} - 1.132)}{215.63 \times J \times \left(D^{0.75} - \frac{18.42}{(E_c/k)^{0.25}}\right)}\right]
        ''')
        
        st.markdown("---")
        
        # ส่งออกรายงาน Word
        st.subheader("📄 ส่งออกรายงาน")
        
        # เตรียมข้อมูลสำหรับรายงาน
        inputs_dict = {
            'w18_design': w18_design,
            'pt': pt,
            'reliability': reliability,
            'so': so,
            'k_eff': k_eff,
            'ls': ls_value,
            'fc_cube': fc_cube,
            'sc': sc,
            'j': j_value,
            'cd': cd
        }
        
        calculated_dict = {
            'fc_cylinder': fc_cylinder,
            'ec': ec,
            'zr': zr,
            'delta_psi': delta_psi
        }
        
        # สร้างปุ่มดาวน์โหลด
        if st.button("📥 สร้างรายงาน Word", type="primary"):
            with st.spinner("กำลังสร้างรายงาน..."):
                try:
                    buffer = create_word_report(
                        pavement_type=pavement_type,
                        inputs=inputs_dict,
                        calculated_values=calculated_dict,
                        comparison_results=comparison_results,
                        selected_d=d_selected,
                        main_result=(passed_selected, ratio_selected),
                        layers_data=layers_data
                    )
                    
                    if buffer:
                        st.download_button(
                            label="⬇️ ดาวน์โหลดรายงาน (.docx)",
                            data=buffer,
                            file_name=f"AASHTO_Rigid_Pavement_Design_{datetime.now().strftime('%Y%m%d_%H%M')}.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                        st.success("สร้างรายงานสำเร็จ!")
                except Exception as e:
                    st.error(f"เกิดข้อผิดพลาด: {str(e)}")
                    st.info("กรุณาติดตั้ง python-docx: `pip install python-docx`")
