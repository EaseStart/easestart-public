# Bản Đồ Đối Thủ Open Source — Agritech Simulation

> Kết quả World-class Research qua Google Search. Cập nhật: 17/03/2026.

---

## 1. Đối Thủ Trực Tiếp (Simulation Engine)

Đây là các dự án **thực sự mô phỏng** sinh trưởng cây trồng/hệ sinh thái, gần nhất với ý tưởng của bạn:

| Dự án | GitHub | Mô tả | Ngôn ngữ | Đánh giá |
|-------|--------|-------|-----------|----------|
| **APSIM** | `APSIMInitiative/APSIM710` | Nền tảng giả lập nông nghiệp **cấp quốc tế**, mô phỏng tương tác cây-đất-khí hậu-quản lý. Được dùng rộng rãi trong nghiên cứu. | C#/.NET | ⭐ Rất mạnh nhưng **Enterprise/Academic**, UX cực kỳ phức tạp. Không nhắm vào Indoor/Hydro. |
| **AquaponicSim** | `monsoon96/AquaponicSim` | Chương trình giả lập **chuyên cho Aquaponics**. | Python | ⚠️ Repo nhỏ, ít maintain. Nhưng chứng tỏ nhu cầu tồn tại. |
| **AlphaGardenSim** | `BerkeleyAutomation/AlphaGarden` | Giả lập vườn đa canh (polyculture) từ UC Berkeley. Tích hợp **OpenAI Gym** để học chính sách chăm sóc bằng Reinforcement Learning. | Python | ⭐ Rất thú vị, nhưng tập trung vào AI/RL research, không phải tool cho farmer. |
| **BioCro** | `BioCro/BioCro` | Dự đoán sinh trưởng cây trồng theo thời gian dựa trên thông số cây + dữ liệu môi trường. Kiến trúc modular. | R/C++ | ⭐ Mạnh về model sinh lý, nhưng là thư viện R, không có GUI/Web. |
| **plantFEM** | `kazulagi/plantfem` | Giả lập nông nghiệp đa vật lý bằng **Finite Element Method** cho cây trồng ngoài đồng ruộng + nền đất. | Fortran | 🔬 Thuần học thuật. Không dành cho indoor farming. |
| **PMF** | `jlu-ilr-hydro/pmf` | Plant Modeling Framework — framework Python linh hoạt để phát triển mô hình cây trồng tuỳ chỉnh. | Python | ⭐ Modular, Python. Có thể là nền tảng tham khảo tốt cho core engine. |
| **plant_growth_simulation** | `kernelshreyak/plant_growth_simulation` | Giả lập 2D sinh trưởng cây. Có GUI (PyQt6), mô hình ánh sáng/nhiệt/ẩm đất, dùng Numba tăng tốc. | Python | ✅ Gần nhất với concept của bạn về GUI + mô phỏng, nhưng chỉ 2D và không có Hydro/Aqua. |
| **farm-simulator** | `Fantaso/farm-simulator` | Giả lập sinh trưởng cây trồng với các yếu tố đất, dinh dưỡng, thời tiết. | Python | ⚠️ Một số công thức nông nghiệp là hư cấu. Ý tưởng tốt nhưng chưa chính xác khoa học. |

---

## 2. Dự Án Liên Quan (Control/Monitoring, Không Phải Simulation)

Các dự án này **không mô phỏng** nhưng cung cấp phần cứng/phần mềm điều khiển hệ thống thật:

| Dự án | Loại | Mô tả |
|-------|------|-------|
| **FarmBot** | Hardware + Software | 100% open source, tự động trồng/tưới/nhổ cỏ. Rất nổi tiếng. |
| **HydroBuddy** | Calculator | Tính toán dung dịch dinh dưỡng thuỷ canh. Rất phổ biến. |
| **OpenHydro** | Controller | Hệ thống điều khiển thuỷ canh dùng Arduino + Raspberry Pi + Node-RED. |
| **SmartPot** | Automation | Quản lý vườn thuỷ canh, có tính năng giả lập sensor trên Wokwi. |
| **ESPonics** | Aeroponics | Hệ thống khí canh tự động dùng ESP32 với web interface. |
| **MyCodo** | Data Logger | Giám sát và điều khiển môi trường, dùng Raspberry Pi. |
| **LiteFarm** | Farm Management | Phần mềm quản lý trang trại bền vững (Quản lý, không giả lập). |
| **Tania** | Farm Management | Quản lý trang trại với IoT, theo dõi hoạt động kinh doanh. |
| **CEAOD** | Dataset | Repository dữ liệu chuẩn hoá cho nghiên cứu nhà kính & indoor farm. |

---

## 3. Phân Tích Khoảng Trống (Gap Analysis)

> [!IMPORTANT]
> **Khoảng trống lớn nhất trên thị trường Open Source:**
> Không có dự án nào kết hợp đồng thời **3 yếu tố**: ① Simulation Engine cho Indoor/Hydro/Aqua ② Giao diện trực quan dễ dùng (Web UI) ③ Open Source MIT.

| Yếu tố | APSIM | AlphaGarden | AquaponicSim | PMF | **Dự án của bạn** |
|---------|-------|-------------|--------------|-----|-------------------|
| Simulation Engine | ✅ | ✅ | ✅ | ✅ | ✅ |
| Indoor/Hydro/Aqua focus | ❌ | ❌ | ✅ | ❌ | ✅ |
| Web UI trực quan | ❌ | ❌ | ❌ | ❌ | ✅ |
| Dễ dùng cho Farmer | ❌ | ❌ | ❌ | ❌ | ✅ |
| Open Source MIT | ✅ | ✅ | ✅ | ✅ | ✅ |
| Community Recipes | ❌ | ❌ | ❌ | ❌ | ✅ |

**Kết luận:** Bạn không xây lại APSIM. Bạn xây **"Figma cho Indoor Farming"** — một công cụ trực quan, kéo-thả, chạy giả lập nhanh mà bất kỳ Urban Farmer nào cũng dùng được ngay lập tức.

---

## 4. Chiến Lược Tận Dụng (Leverage Strategy)

Thay vì build từ số 0, bạn có thể đứng trên vai các ông lớn:

| Thành phần | Tự build | Tận dụng từ OSS |
|------------|----------|-----------------|
| Plant Growth Models | ❌ | ✅ PMF (Python, modular) hoặc BioCro |
| Aquaponics Chemistry | ❌ | ✅ HydroBuddy (nutrient calculations) |
| Environment Data | ❌ | ✅ CEAOD (chuẩn hoá datasets) |
| Web UI / Visualization | ✅ | — (Đây là USP của bạn) |
| Simulation Orchestrator | ✅ | — (Core IP) |
| Community Recipe Store | ✅ | — (Micro-MOAT) |
