# app.py
# -*- coding: utf-8 -*-
"""
Ứng dụng Streamlit: QUẢN LÝ ĐIỂM SINH VIÊN
Chuyển đổi từ Google Colab sang Streamlit.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# ============================================================
# CẤU HÌNH TRANG
# ============================================================
st.set_page_config(
    page_title="Quản lý điểm sinh viên",
    page_icon="🎓",
    layout="wide"
)

# ============================================================
# 1. TẠO DỮ LIỆU
# ============================================================
data = {
    "Họ và tên": [
        "Nguyễn Văn An",
        "Trần Thị Bình",
        "Lê Hoàng Chi",
        "Phạm Minh Dũng",
        "Hoàng Thị Em",
        "Vũ Đức Giang",
        "Đặng Thị Hoa",
        "Bùi Văn Hùng",
        "Đỗ Thị Lan",
        "Ngô Quốc Minh"
    ],
    "Điểm chuyên cần": [8.0, 9.0, 7.0, 10.0, 6.0, 8.0, 9.0, 7.0, 10.0, 8.0],
    "Điểm giữa kỳ":    [7.5, 8.0, 6.5, 9.0, 5.5, 7.0, 8.5, 6.0, 9.5, 7.5],
    "Điểm cuối kỳ":    [8.0, 7.5, 7.0, 9.5, 6.0, 7.5, 8.0, 6.5, 9.0, 8.5]
}

df = pd.DataFrame(data)

# ============================================================
# 2. TÍNH ĐIỂM TỔNG KẾT
# ============================================================
df["Tong_ket"] = (
    0.2 * df["Điểm chuyên cần"]
    + 0.3 * df["Điểm giữa kỳ"]
    + 0.5 * df["Điểm cuối kỳ"]
).round(1)

# ============================================================
# 3. XẾP LOẠI
# ============================================================
def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung Bình"
    else:
        return "Yếu"

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)

# Đặt STT từ 1
df.index = range(1, len(df) + 1)
df.index.name = "STT"

# ============================================================
# 4. TIÊU ĐỀ
# ============================================================
st.title("🎓 QUẢN LÝ ĐIỂM SINH VIÊN")
st.markdown("---")

# ============================================================
# 5. BẢNG ĐIỂM
# ============================================================
st.subheader("📋 Bảng điểm 10 sinh viên")

# Chọn các cột theo yêu cầu
df_hien_thi = df[[
    "Họ và tên",
    "Điểm chuyên cần",
    "Điểm giữa kỳ",
    "Điểm cuối kỳ",
    "Tong_ket",
    "Xep_loai"
]].rename(columns={
    "Điểm chuyên cần": "Chuyên cần",
    "Điểm giữa kỳ":    "Giữa kỳ",
    "Điểm cuối kỳ":    "Cuối kỳ",
    "Tong_ket":        "Tổng kết",
    "Xep_loai":        "Xếp loại"
})

st.dataframe(df_hien_thi, use_container_width=True)

# ============================================================
# 6. THỐNG KÊ
# ============================================================
st.markdown("---")
st.subheader("📊 Thống kê")

diem_tb       = df["Tong_ket"].mean()
sv_cao_nhat   = df.loc[df["Tong_ket"].idxmax()]
sv_thap_nhat  = df.loc[df["Tong_ket"].idxmin()]
so_dat        = (df["Tong_ket"] >= 5).sum()
tong_sv       = len(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Điểm trung bình lớp",
    f"{diem_tb:.2f}"
)

col2.metric(
    "Sinh viên cao nhất",
    f"{sv_cao_nhat['Tong_ket']}",
    sv_cao_nhat["Họ và tên"]
)

col3.metric(
    "Sinh viên thấp nhất",
    f"{sv_thap_nhat['Tong_ket']}",
    sv_thap_nhat["Họ và tên"],
    delta_color="inverse"
)

col4.metric(
    "Số sinh viên đạt (≥5)",
    f"{so_dat} / {tong_sv}"
)

# ============================================================
# 7. SELECTBOX CHỌN SINH VIÊN
# ============================================================
st.markdown("---")
st.subheader("🔍 Tra cứu thông tin sinh viên")

danh_sach_ten = df["Họ và tên"].tolist()
ten_duoc_chon = st.selectbox("Chọn một sinh viên:", danh_sach_ten)

# Lấy thông tin sinh viên được chọn
sv = df[df["Họ và tên"] == ten_duoc_chon].iloc[0]

st.markdown(f"### 📌 Thông tin: **{sv['Họ và tên']}**")

c1, c2, c3, c4, c5 = st.columns(5)
c1.info(f"**Chuyên cần**\n\n{sv['Điểm chuyên cần']}")
c2.info(f"**Giữa kỳ**\n\n{sv['Điểm giữa kỳ']}")
c3.info(f"**Cuối kỳ**\n\n{sv['Điểm cuối kỳ']}")
c4.success(f"**Tổng kết**\n\n{sv['Tong_ket']}")
c5.warning(f"**Xếp loại**\n\n{sv['Xep_loai']}")

# ============================================================
# 8. BIỂU ĐỒ CỘT ĐIỂM TỔNG KẾT
# ============================================================
st.markdown("---")
st.subheader("📈 Biểu đồ điểm tổng kết của 10 sinh viên")

# Tên ngắn hiển thị trên trục Y (giống hình mẫu)
df["Ten_ngan"] = ["An", "Bình", "Chi", "Dũng",
                  "Em", "Giang", "Hoa", "Hùng", "Lan", "Minh"]

fig, ax = plt.subplots(figsize=(10, 6))

# Đảo thứ tự để người đầu tiên nằm trên cùng
df_dao = df.iloc[::-1]

ax.barh(
    df_dao["Ten_ngan"],
    df_dao["Tong_ket"],
    color="#4A90E2",
    edgecolor="none",
    height=0.6
)

ax.set_title("Điểm tổng kết của 10 sinh viên",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Điểm tổng kết", fontsize=11)
ax.set_ylabel("Sinh viên", fontsize=11)

ax.set_xlim(0, 10)
ax.xaxis.set_major_locator(MultipleLocator(2.5))

ax.grid(axis="x", linestyle="--", alpha=0.4)
ax.set_axisbelow(True)

for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

plt.tight_layout()
st.pyplot(fig)

# ============================================================
# 9. FOOTER: HỌ TÊN + MSSV (chữ nhỏ)
# ============================================================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; font-size: 12px; color: gray;'>
        Ứng dụng được tạo bởi: <b>Vũ Kỳ Nam</b> — MSSV: <b>031208000036</b>
    </div>
    """,
    unsafe_allow_html=True
)
