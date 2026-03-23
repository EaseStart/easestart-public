# 🌱 Agritech Simulation Platform — Research Report

> **Dự án:** Open Source Simulation Engine cho Indoor Farming (Thuỷ canh, Khí canh, Aquaponics)
> **CEO:** Jang Trịnh — Technologist + Farmer
> **License:** MIT (Open Source)
> **Ngày nghiên cứu:** 17/03/2026
> **Trạng thái:** ✅ Stage 2 Complete → Ready for MVP (Stage 3)

---

## Tóm Tắt Kết Quả

Sau 4 vòng nghiên cứu chuyên sâu (World-class Web Research), dự án đã đạt đủ tiêu chí để chuyển sang giai đoạn MVP:

| Hạng mục | Kết quả | File |
|----------|---------|------|
| Ý tưởng & Lean Canvas | ✅ 5/5 Giantiny Quality Gates | [agritech_ideation.md](./agritech_ideation.md) |
| Bản đồ đối thủ OSS | ✅ 30+ dự án, gap analysis | [agritech_oss_landscape.md](./agritech_oss_landscape.md) |
| Nguồn dữ liệu mở | ✅ 7 layers, 15+ APIs miễn phí | [agritech_data_sources.md](./agritech_data_sources.md) |
| Ảnh hưởng môi trường | ✅ 8 yếu tố, optimal ranges | [agritech_env_impact.md](./agritech_env_impact.md) |

---

## Phát Hiện Quan Trọng

### 1. Khoảng Trống Thị Trường (Market Gap)
Không có dự án open source nào kết hợp đồng thời:
- ① Simulation Engine cho Indoor/Hydro/Aqua
- ② Web UI trực quan dễ dùng
- ③ Open Source MIT

**→ Vị trí: "Figma cho Indoor Farming"**

### 2. Dữ Liệu Không Cần Thu Thập Từ Đầu
- **WOFOST** → 23 loại cây (YAML)
- **FishBase** → Hàng nghìn loài cá
- **Open-Meteo** → 80+ năm khí hậu, miễn phí
- **SoilGrids** → Đất toàn cầu theo GPS
- **HydroBuddy** → Database phân bón

### 3. pH Là Biến Vua Của Simulation
- Sai 0.5 đơn vị pH = toàn bộ dinh dưỡng bị khóa
- Aquaponics có "tam giác xung đột": Cây (5.5–6.5) vs Cá (7.0–7.5) vs Vi khuẩn (7.0–8.0)
- Zone chung sống duy nhất: **6.8–7.2**

### 4. Killer UX Feature
User nhập địa chỉ → hệ thống tự động kéo:
- pH nước máy (USGS/Waterbase API)
- Khí hậu địa phương (Open-Meteo API)
- Đặc tính đất (SoilGrids API)
→ **Pre-fill toàn bộ thông số môi trường. Zero manual input.**

---

## Counter-Positioning vs Enterprise

| | AnyLogic / BioWin | **Dự án của bạn** |
|---|---|---|
| Giá | $$$$ Enterprise | Free (MIT) |
| Đối tượng | Nhà nghiên cứu, Lab | Urban Farmer, Developer |
| UX | Cực kỳ phức tạp | Tối giản (EaseUI philosophy) |
| Extensibility | Đóng kín | Plugin / Community Recipes |
| Setup | Tuần–Tháng | Phút |

---

## Kiến Trúc Dữ Liệu (7 Layers)

```
Layer 7: Soil Data ──────── SoilGrids, SSURGO
Layer 6: Water Quality ──── USGS WQP, Waterbase EU
Layer 5: Climate APIs ───── Open-Meteo, NASA POWER
Layer 4: Community Recipes ─ BẠN TỰ XÂY (Micro-MOAT)
Layer 3: Fish Biology ───── FishBase, Kaggle
Layer 2: Nutrient Chemistry HydroBuddy, CEAOD
Layer 1: Plant Growth ───── WOFOST, PMF, BioCro
```

---

## Next Steps (MVP Phase)

1. **Chọn Tech Stack** cho Simulation Engine (Python? Rust? WebAssembly?)
2. **Import WOFOST data** (23 loại cây) làm seed data
3. **Tích hợp Open-Meteo API** cho climate profiles
4. **Build Web UI** prototype (drag-and-drop farm builder)
5. **Implement pH/EC/Temperature physics** (module đầu tiên)

---

## Danh Mục Tài Liệu

| File | Nội dung | Kích thước |
|------|----------|-----------|
| `agritech_ideation.md` | Lean Canvas, 5 Quality Gates, Business Model | Brainstorming |
| `agritech_oss_landscape.md` | 30+ dự án OSS, Gap Analysis, Leverage Strategy | Competitor Research |
| `agritech_data_sources.md` | 7 Layers, 15+ APIs/Datasets, License Compatibility | Data Strategy |
| `agritech_env_impact.md` | 8 yếu tố môi trường, optimal ranges, cause-effect matrix | Domain Knowledge |
