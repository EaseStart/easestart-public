# Nguồn Dữ Liệu Mở Có Thể Tận Dụng — Agritech Simulation Engine

> Câu trả lời: **CÓ, rất nhiều.** Bạn gần như không cần thu thập dữ liệu từ đầu.

---

## Tổng Quan Kiến Trúc Dữ Liệu

Simulation Engine cần 4 lớp dữ liệu. Mỗi lớp đều có nguồn mở sẵn:

```
┌─────────────────────────────────────────────┐
│  Layer 4: Community Recipes (BẠN TỰ BUILD)  │  ← Micro-MOAT
├─────────────────────────────────────────────┤
│  Layer 3: Fish Biology & Chemistry          │  ← FishBase, Kaggle
├─────────────────────────────────────────────┤
│  Layer 2: Nutrient & Water Chemistry        │  ← HydroBuddy, Veleda
├─────────────────────────────────────────────┤
│  Layer 1: Plant Growth Models               │  ← WOFOST, PMF, FAO
└─────────────────────────────────────────────┘
```

---

## Layer 1: Mô Hình Sinh Trưởng Cây (Plant Growth Models)

| Nguồn | Dữ liệu | License | Cách tận dụng |
|-------|----------|---------|---------------|
| **WOFOST** (GitHub) | Bộ thông số cho **23 loại cây trồng** (YAML): lúa, ngô, đậu, khoai, cà chua... Bao gồm: quang hợp, hô hấp, phenology. | Open | Import trực tiếp YAML → JSON cho engine. |
| **DSSAT** | Mô hình cho **45+ loại cây**, kèm dataset thí nghiệm (soil, weather, management). | Free | Trích xuất crop parameters làm seed data. |
| **FAO AquaCrop** | Mô hình năng suất cây trồng theo nước. Có manual + training data. | Public | Tham khảo công thức tính yield response. |
| **PMF** (Python) | Framework modular Python để xây mô hình cây trồng tuỳ chỉnh. | Open | Fork làm core engine hoặc adapter layer. |
| **BioCro** (R/C++) | Dự đoán sinh trưởng cây theo thời gian, kiến trúc modular. | Open | Port model parameters sang Python. |
| **TRY Database** | **37 triệu bản ghi**, 160K loài, 2100 đặc tính cây trồng. | Free (academic) | Tra cứu traits cho bất kỳ loài nào. |

---

## Layer 2: Hoá Học Dinh Dưỡng & Nước (Nutrient Chemistry)

| Nguồn | Dữ liệu | License | Cách tận dụng |
|-------|----------|---------|---------------|
| **HydroBuddy** (GitHub) | Database phân bón tích hợp + online DB cộng đồng. Export CSV. | GPL v3 | Import công thức dinh dưỡng + tỉ lệ pha. |
| **Veleda Platform** | Open-data cho hydroponics: nhiệt độ nước/không khí, pH, EC, biomass. | Open | Dùng làm calibration data cho simulation. |
| **CEAOD** (GitHub) | Datasets chuẩn hoá cho nhà kính + vertical farm. Time-series sensor data (GH_Cucumber, GH_Lettuce...). | Open | Import trực tiếp làm environment profiles. |

---

## Layer 3: Sinh Học Cá & Hệ Sinh Thái (Fish Biology)

| Nguồn | Dữ liệu | License | Cách tận dụng |
|-------|----------|---------|---------------|
| **FishBase** | Database khoa học quốc tế: tốc độ tăng trưởng, thông số môi trường cho **hàng nghìn** loài cá. | CC-BY-NC | Tra cứu: Tilapia, Catfish, Koi → growth rate, pH range, ammonia tolerance. |
| **Kaggle: Aquaponics Fish Ponds** | Dữ liệu cảm biến thực tế: pH, TDS, nhiệt độ, NH3, DO, độ đục, cân nặng cá, mật độ. | Open | Training data cho mô hình cá trong aquaponics. |
| **Kaggle: Hydroponic IoT Logs** | Time-series sensor: pH, TDS, nhiệt độ nước, độ ẩm, trạng thái actuator. | Open | Calibration cho simulation môi trường thuỷ canh. |

---

## Layer 4: Community Recipes (BẠN TỰ XÂY)

> [!IMPORTANT]
> Đây là **Micro-MOAT duy nhất** mà không nguồn mở nào có. Khi user chạy giả lập thành công, hệ thống lưu lại "recipe" (nhiệt độ, pH, EC, loài cây, loài cá, diện tích) → thư viện template cộng đồng.

---

## Layer 5: Khí Hậu & Thời Tiết Địa Phương (Climate APIs)

User chỉ cần nhập **toạ độ GPS** hoặc **tên thành phố** → Engine tự động kéo dữ liệu khí hậu thực tế về.

| Nguồn | Dữ liệu | Giá | Cách tận dụng |
|-------|----------|-----|---------------|
| **Open-Meteo** | Dữ liệu **80+ năm** (từ 1940), hàng giờ: nhiệt độ, độ ẩm, gió, mưa, bức xạ mặt trời, nhiệt độ đất, độ ẩm đất. Độ phân giải 9km. | ✅ **Miễn phí**, không cần API key | `GET api → JSON` → Import trực tiếp làm environment profile cho simulation. **Nguồn chính cho MVP.** |
| **NASA POWER** | Dữ liệu vệ tinh toàn cầu: bức xạ mặt trời (shortwave), nhiệt độ min/max, độ ẩm tương đối, lượng mưa. Có archive riêng cho nông nghiệp ("Agroclimatology"). | ✅ **Miễn phí** | Bổ sung dữ liệu Solar Radiation chính xác hơn (quan trọng cho mô hình quang hợp). Có Python client `pynasapower`. |
| **OpenWeatherMap Agro** | Thời tiết hiện tại + dự báo + dữ liệu vệ tinh cho precision farming. | Free tier có sẵn | Dùng cho tính năng "Real-time sync" sau MVP. |
| **Open-Meteo Climate** | Dữ liệu mô hình khí hậu **đến năm 2050** (dự đoán biến đổi khí hậu). | ✅ **Miễn phí** | Cho phép user chạy simulation "Nếu nhiệt độ tăng 2°C trong 10 năm tới thì farm có bị ảnh hưởng?" |

---

## Layer 6: Chất Lượng Nguồn Nước (Water Quality APIs)

Nước máy / nước giếng ở mỗi vùng có pH, độ cứng, TDS khác nhau → ảnh hưởng trực tiếp đến dung dịch thuỷ canh.

| Nguồn | Phạm vi | Dữ liệu | Cách tận dụng |
|-------|---------|----------|---------------|
| **USGS Water Quality Portal** | 🇺🇸 Mỹ | pH, TDS, độ cứng, khoáng chất — từ **400+ cơ quan** liên bang/tiểu bang. REST API. | User nhập ZIP code → auto-fill thông số nước đầu vào. |
| **Waterbase (EEA)** | 🇪🇺 Châu Âu | Chất lượng nước sông, hồ, nước ngầm toàn Châu Âu. Open API. | Tương tự cho user Châu Âu. |
| **TapWaterData** | 🇺🇸 Mỹ | Tra cứu chất lượng nước máy theo ZIP code: pH, độ cứng, chất ô nhiễm. | UX feature: "Nhập mã vùng → biết nước nhà bạn có pH bao nhiêu." |
| **WHO/UNICEF JMP** | 🌍 Toàn cầu | Dữ liệu nguồn nước sạch theo quốc gia/khu vực. | Fallback cho vùng không có API chi tiết. |

> [!TIP]
> **Killer UX Feature:** User chỉ cần nhập địa chỉ → hệ thống tự động kéo pH nước máy + khí hậu địa phương → pre-fill toàn bộ thông số môi trường cho simulation. Không ai làm việc này.

---

## Layer 7: Dữ Liệu Đất (Soil Data APIs)

Quan trọng cho các hệ thống trồng dưới đất (soil-based) và aquaponics media bed.

| Nguồn | Dữ liệu | Cách tận dụng |
|-------|----------|---------------|
| **SoilGrids (ISRIC)** | Dữ liệu đất **toàn cầu** theo GPS: pH, thành phần cát/bùn/sét, Nitrogen, Carbon hữu cơ. 6 tầng sâu (0–200cm). REST API miễn phí. | User nhập toạ độ → biết đất vùng mình có đặc tính gì. |
| **SSURGO (USGS)** | 🇺🇸 Bản đồ đất chi tiết Mỹ: loại đất, pH, khả năng giữ nước. | Dữ liệu bổ sung cho user Mỹ. |
| **Kaegro Global Soil API** | Dữ liệu đất dự đoán toàn cầu: texture, pH, nitrogen, khả năng giữ nước. Không cần auth. | Backup API nếu SoilGrids quá tải. |

---

## Chiến Lược Tích Hợp (Data Pipeline)

```
Giai đoạn 1 (MVP):
  WOFOST YAML → parse → Plant Growth DB (JSON)
  HydroBuddy CSV → parse → Nutrient DB (JSON)
  FishBase API → query → Fish Species DB (JSON)

Giai đoạn 2 (Post-MVP):
  CEAOD datasets → import → Environment Profiles
  Kaggle sensor data → ML training → Anomaly Detection
  TRY Database → enrich → Plant Traits Library

Giai đoạn 3 (Community):
  User simulation runs → save → Community Recipes Store
```

---

## Lưu Ý Về License

| License | Dự án | Tương thích MIT? |
|---------|-------|------------------|
| Open/Public Domain | WOFOST, CEAOD, Kaggle, Veleda | ✅ Hoàn toàn |
| GPL v3 | HydroBuddy | ⚠️ Chỉ dùng **dữ liệu output**, không fork code |
| CC-BY-NC | FishBase | ⚠️ OK cho non-commercial. Cần ghi nguồn. |
| Free (Academic) | TRY Database, DSSAT, FAO | ✅ Dùng data OK, ghi nguồn |

> [!TIP]
> Với **mô hình Open Source MIT** của bạn, hầu hết các nguồn trên đều tương thích. Chỉ cần lưu ý:
> - **HydroBuddy**: Dùng dữ liệu (CSV export) thay vì fork code GPL.
> - **FishBase**: Ghi attribution. Nếu muốn thương mại sau, cần liên hệ license riêng.
