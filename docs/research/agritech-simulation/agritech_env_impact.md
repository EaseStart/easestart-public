# Bản Đồ Ảnh Hưởng Môi Trường → Nuôi Trồng

> Knowledge Base cho Simulation Engine. Mỗi yếu tố dưới đây = 1 module trong physics model.

---

## 1. Nhiệt Độ (Temperature)

```
Nhiệt độ ↑ → Quang hợp ↑ (đến ngưỡng) → Vượt ngưỡng → Stress nhiệt → Chết
Nhiệt độ ↓ → Trao đổi chất ↓ → Hấp thu dinh dưỡng ↓ → Tăng trưởng chậm
```

| Loài | Ngày (°C) | Đêm (°C) | Ghi chú |
|------|-----------|-----------|---------|
| Rau diếp | 20–24 | 16–18 | Cây mùa mát. >30°C → trổ hoa sớm (bolting) |
| Cà chua | 21–27 | 17–18 | Đêm 18°C tối ưu cho ra quả |
| Húng quế | 25–29 | 20–24 | Cần ấm, chịu nhiệt tốt |
| Thyme/Rosemary | 18–24 | 13–18 | Chịu lạnh hơn |

**Nhiệt độ rễ (Root Zone):** 18–24°C. Nước quá nóng → giảm oxy hòa tan → bệnh rễ.

**Ảnh hưởng đến vi khuẩn Nitrification (Aquaponics):**
- Tối ưu: 20–30°C
- <17°C: Vi khuẩn chậm → Ammonia tích tụ → **Cá chết**
- <0°C hoặc >49°C: Vi khuẩn chết

---

## 2. Độ Ẩm (Humidity)

```
Độ ẩm ↑ → Thoát hơi nước ↓ → Hấp thu dinh dưỡng ↓ + Nấm mốc ↑
Độ ẩm ↓ → Thoát hơi nước ↑ → Mất nước → Stress → Héo
```

| Giai đoạn | Tối ưu (%) | Rủi ro |
|-----------|-----------|--------|
| Nảy mầm | 80–90% | — |
| Sinh trưởng | 50–70% | >70% → nấm mốc |
| Ra hoa/Quả | 40–50% | >60% → thụ phấn kém |

---

## 3. pH Nước

> [!CAUTION]
> **pH là biến quan trọng nhất** trong simulation. Sai pH = toàn bộ dinh dưỡng bị khóa dù có đủ.

```
pH 5.5–6.5 → VÙNG VÀNG cho thuỷ canh (tối ưu hấp thu)
pH < 5.5  → Ca, Mg bị khóa + Al/Mn độc hại
pH > 6.5  → Fe, Mn, Zn bị khóa → Lá vàng (chlorosis)
```

**Aquaponics pH Compromise:** 6.8–7.2 (cân bằng cá + cây + vi khuẩn)

| Thành phần | pH tối ưu |
|------------|-----------|
| Cây thuỷ canh | 5.5–6.5 |
| Cá (Tilapia, Catfish) | 7.0–7.5 |
| Vi khuẩn Nitrification | 7.0–8.0 |
| **Hệ thống Aquaponics** | **6.8–7.2** |

---

## 4. EC / TDS (Nồng Độ Dinh Dưỡng)

```
EC ↑ → Quá mặn → Cháy rễ + Stress thẩm thấu → Cây héo
EC ↓ → Thiếu dinh dưỡng → Lá vàng + Tăng trưởng chậm
```

| Loài | EC tối ưu (mS/cm) | TDS (ppm) |
|------|--------------------|-----------|
| Rau diếp | 0.8–1.2 | 560–840 |
| Cà chua (ra quả) | 2.0–3.5 | 1400–2450 |
| Húng quế | 1.0–1.6 | 700–1120 |
| Cây mầm (seedling) | 0.5–1.0 | 350–700 |

---

## 5. Ánh Sáng (DLI — Daily Light Integral)

```
DLI = PPFD × Giờ chiếu × 0.0036
(mol/m²/ngày)
```

| Loài | DLI tối ưu (mol/m²/d) | PPFD tối ưu (µmol/m²/s) |
|------|----------------------|--------------------------|
| Rau diếp | 12–17 | 200–300 |
| Cà chua | 20–30 | 400–600 |
| Húng quế | 15–20 | 300–400 |
| Dâu tây | 15–25 | 300–500 |

**Quang phổ quan trọng:** Đỏ (620–700nm) → quang hợp chính. Xanh (400–500nm) → hình thái lá.

---

## 6. Oxy Hoà Tan (DO — Dissolved Oxygen)

```
Nhiệt độ nước ↑ → DO ↓ → Rễ ngộp + Vi khuẩn yếu + Cá stress
```

| Sinh vật | DO tối thiểu (ppm) | DO tối ưu (ppm) |
|----------|--------------------|-----------------| 
| Cá (chung) | 5 | 5–8 |
| Tilapia | 3 (sống sót) | >4 |
| Vi khuẩn Nitrification | 4 | 4–8 |
| Rễ cây | 4 | 6–8 |

---

## 7. Chu Trình Nitrogen (Aquaponics)

```
Cá thải → NH3 (ammonia) ──Nitrosomonas──→ NO2⁻ (nitrite) ──Nitrobacter──→ NO3⁻ (nitrate) → Cây hấp thu
                ↑ CỰC ĐỘC               ↑ RẤT ĐỘC                    ↑ AN TOÀN
```

| Chất | Ngưỡng an toàn | Ngưỡng nguy hiểm |
|------|----------------|-------------------|
| NH3 (Ammonia) | 0 ppm | >1 ppm → cá chết |
| NO2⁻ (Nitrite) | <1 ppm | >5 ppm → cá chết |
| NO3⁻ (Nitrate) | <150 ppm | >300 ppm → stress cây |

---

## 8. Chất Lượng Nước Đầu Vào (Tap Water)

```
Nước cứng (Ca/Mg cao) → EC baseline ↑ → Ít "chỗ" cho dinh dưỡng khác → Khóa vi lượng
Chlorine/Chloramine    → Giết vi khuẩn có lợi → Chu trình Nitrogen sụp đổ (Aquaponics)
```

| Yếu tố | Ngưỡng an toàn | Cách xử lý |
|---------|----------------|------------|
| TDS nước máy | <200 ppm | >200 ppm → dùng RO |
| Chlorine | 0 ppm | Để nước 24–48h hoặc lọc carbon |
| Chloramine | 0 ppm | **Không bốc hơi** → bắt buộc lọc carbon |
| pH nước máy | 6.5–7.5 | Điều chỉnh trước khi pha dinh dưỡng |

---

## Ma Trận Ảnh Hưởng (Simulation Engine Logic)

> Đây là **bảng quan hệ nhân-quả** mà Engine cần implement:

| Biến Đầu Vào | ↑ Quá cao | ↓ Quá thấp | Module Engine |
|---------------|-----------|------------|---------------|
| Nhiệt độ không khí | Stress nhiệt, bolting | Chậm phát triển | `climate_sim` |
| Nhiệt độ nước | DO giảm, bệnh rễ | Vi khuẩn chậm, ammonia tích tụ | `water_sim` |
| Độ ẩm | Nấm mốc, thụ phấn kém | Héo, mất nước | `climate_sim` |
| pH | Fe/Mn/Zn bị khóa | Ca/Mg bị khóa, Al độc | `chemistry_sim` |
| EC/TDS | Cháy rễ, stress thẩm thấu | Thiếu dinh dưỡng | `nutrient_sim` |
| DLI | Photoinhibition | Cây yếu, dài chân | `light_sim` |
| DO | — (hiếm khi quá cao) | Ngộp rễ, cá chết | `water_sim` |
| Ammonia | Cá chết | — (không có vấn đề) | `nitrogen_cycle` |
| Chlorine | Giết vi khuẩn có lợi | — | `water_quality` |
| Độ cứng nước | Khóa vi lượng | — | `water_quality` |
