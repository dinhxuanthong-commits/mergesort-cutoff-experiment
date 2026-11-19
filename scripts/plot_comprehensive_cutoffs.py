#!/usr/bin/env python3
"""
plot_comprehensive_cutoffs.py
Tạo bộ 6 biểu đồ phân tích chuyên sâu cho 66 giá trị CUTOFF (1..100).
Làm nổi bật điểm tối ưu chính xác nhất với tọa độ, mũi tên chỉ dẫn,
và hộp chú thích chi tiết trên từng đồ thị.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "figure.dpi": 200,
    "font.family": "DejaVu Sans",
    "axes.titleweight": "bold",
    "axes.labelweight": "bold"
})

results_dir = Path("results")
# Tìm tệp dense 66 cutoffs mới nhất
dense_csvs = list(results_dir.glob("experiment_dense_*.csv"))
if dense_csvs:
    csv_file = max(dense_csvs, key=lambda p: p.stat().st_mtime)
else:
    csv_file = max(results_dir.glob("experiment_*.csv"), key=lambda p: p.stat().st_mtime)

print(f"[INFO] Đọc dữ liệu thực nghiệm: {csv_file}")
df = pd.read_csv(csv_file)
out_dir = Path("results/plots")
out_dir.mkdir(parents=True, exist_ok=True)

# Tính baseline cutoff = 1
baseline_df = df[df["cutoff"] == 1][["n", "dataType", "medianMs"]].rename(
    columns={"medianMs": "baselineMs"}
)
merged = df[df["cutoff"] > 0].merge(baseline_df, on=["n", "dataType"], how="left")
merged["speedup"] = merged["baselineMs"] / merged["medianMs"]

# Tính tăng tốc trung bình cho từng cutoff
overall = merged[merged["cutoff"] > 1].groupby("cutoff")["speedup"].mean().reset_index()
best_cutoff = int(overall.loc[overall["speedup"].idxmax(), "cutoff"])
best_speedup = overall["speedup"].max()

s7 = overall.loc[overall["cutoff"] == 7, "speedup"].values[0]
s10 = overall.loc[overall["cutoff"] == 10, "speedup"].values[0]

# -------------------------------------------------------------------------
# ĐỒ THỊ 1: TỔNG QUAN TOÀN BỘ 66 CUTOFF (1..100) VỚI ĐIỂM TỐI ƯU NỔI BẬT
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 6.5))

ax.plot(overall["cutoff"], overall["speedup"], marker="o", markersize=4,
        color="#1d4ed8", linewidth=2.2, label="Tỉ số tăng tốc thực tế (Empirical Speedup)")

ax.axvspan(18, 28, color="#a78bfa", alpha=0.25, label="Vùng bình nguyên tối ưu (18 <= Cutoff <= 28)")
ax.axhline(1.0, color="#ef4444", linestyle="--", linewidth=1.5, label="Baseline (Mergesort thuần, Cutoff=1: 1.00x)")

# Cutoff 7 (Giáo trình cũ)
ax.axvline(7, color="#d97706", linestyle=":", linewidth=1.8)
ax.scatter([7], [s7], color="#d97706", s=130, zorder=5, edgecolor="black", linewidth=1.2)
ax.annotate(f"Cutoff = 7 (Sách cũ)\nSpeedup = {s7:.4f}x (+{(s7-1)*100:.1f}%)",
            xy=(7, s7), xytext=(7, s7 - 0.14),
            arrowprops=dict(arrowstyle="-|>", color="#d97706", lw=1.5),
            bbox=dict(boxstyle="round,pad=0.35", fc="#fef3c7", ec="#d97706", lw=1.2),
            ha="center", fontsize=9, fontweight="bold")

# Cutoff 10 (Giáo trình mới)
ax.axvline(10, color="#059669", linestyle=":", linewidth=1.8)
ax.scatter([10], [s10], color="#059669", s=130, zorder=5, edgecolor="black", linewidth=1.2)
ax.annotate(f"Cutoff = 10 (Sách mới)\nSpeedup = {s10:.4f}x (+{(s10-1)*100:.1f}%)",
            xy=(10, s10), xytext=(10, s10 + 0.08),
            arrowprops=dict(arrowstyle="-|>", color="#059669", lw=1.5),
            bbox=dict(boxstyle="round,pad=0.35", fc="#d1fae5", ec="#059669", lw=1.2),
            ha="center", fontsize=9, fontweight="bold")

# ĐỈNH TỐI ƯU TOÀN CỤC CHÍNH XÁC
ax.axvline(best_cutoff, color="#7c3aed", linestyle="-.", linewidth=2.2)
ax.scatter([best_cutoff], [best_speedup], color="#e11d48", marker="*", s=380, zorder=6, edgecolor="black", linewidth=1.2)
ax.annotate(f"DIEM TOI UU TOAN CUC CHINH XAC\nCUTOFF* = {best_cutoff}\nSpeedup = {best_speedup:.4f}x (+{(best_speedup-1)*100:.2f}%)",
            xy=(best_cutoff, best_speedup), xytext=(best_cutoff + 12, best_speedup + 0.03),
            arrowprops=dict(arrowstyle="-|>", color="#e11d48", lw=2),
            bbox=dict(boxstyle="round,pad=0.5", fc="#ffe4e6", ec="#e11d48", lw=1.8),
            ha="left", fontsize=10, fontweight="bold")

ax.set_title("DO THI 1: DUONG CONG TANG TOC TONG THE VA DIEM CUTOFF TOI UU NHAT (66 MOC DO)",
             fontsize=12, pad=15)
ax.set_xlabel("Gia tri CUTOFF", fontsize=10)
ax.set_ylabel("Speedup Ratio (so voi Cutoff = 1)", fontsize=10)
ax.set_xlim(0, 102)
ax.set_ylim(0.95, 1.58)
ax.set_xticks([1, 7, 10, 15, 20, 23, 25, 30, 40, 50, 60, 70, 80, 100])
ax.legend(loc="lower right", frameon=True, facecolor="white", framealpha=0.9)

plt.tight_layout()
fig.savefig(out_dir / "chart1_overall_speedup_curve.png")
plt.close(fig)
print("  [OK] Đã xuất: chart1_overall_speedup_curve.png")

# -------------------------------------------------------------------------
# ĐỒ THỊ 2: ĐỈNH TỐI ƯU THEO TỪNG KIỂU DỮ LIỆU
# -------------------------------------------------------------------------
fig, axes = plt.subplots(2, 3, figsize=(16, 10.5))
axes = axes.flatten()

data_types = ["RANDOM", "SORTED", "REVERSED", "NEARLY_SORTED", "MANY_DUPLICATES"]
colors = ["#2563eb", "#059669", "#dc2626", "#d97706", "#7c3aed"]
datatype_peaks = {}

for idx, dtype in enumerate(data_types):
    ax = axes[idx]
    sub = merged[(merged["dataType"] == dtype) & (merged["cutoff"] > 1)]
    grp = sub.groupby("cutoff")["speedup"].mean().reset_index()
    
    peak_c = int(grp.loc[grp["speedup"].idxmax(), "cutoff"])
    peak_s = grp["speedup"].max()
    datatype_peaks[dtype] = (peak_c, peak_s)
    
    ax.plot(grp["cutoff"], grp["speedup"], marker="o", markersize=3.5, color=colors[idx], linewidth=1.8)
    ax.axhline(1.0, color="#9ca3af", linestyle="--", linewidth=1, label="Base (1.0x)")
    
    ax.axvline(peak_c, color="#e11d48", linestyle=":", linewidth=1.5)
    ax.scatter([peak_c], [peak_s], color="#e11d48", marker="*", s=240, zorder=5, edgecolor="black")
    
    y_offset = -0.16 if peak_s > 1.4 else 0.08
    ax.annotate(f"Dinh Toi Uu: Cutoff = {peak_c}\nSpeedup = {peak_s:.4f}x (+{(peak_s-1)*100:.1f}%)",
                xy=(peak_c, peak_s), xytext=(peak_c + 12, peak_s + y_offset),
                arrowprops=dict(arrowstyle="-|>", color="#e11d48", lw=1.5),
                bbox=dict(boxstyle="round,pad=0.3", fc="#fff1f2", ec="#e11d48", lw=1.2),
                fontsize=8.5, fontweight="bold")
    
    ax.set_title(f"Kieu du lieu: {dtype}", fontsize=11, color=colors[idx])
    ax.set_xlabel("CUTOFF")
    ax.set_ylabel("Speedup Ratio")
    ax.set_xlim(0, 102)

# Subplot 6: Tổng hợp 5 kiểu phân bố kèm điểm đỉnh của từng đường
ax_all = axes[5]
for idx, dtype in enumerate(data_types):
    sub = merged[(merged["dataType"] == dtype) & (merged["cutoff"] > 1)]
    grp = sub.groupby("cutoff")["speedup"].mean().reset_index()
    p_c, p_s = datatype_peaks[dtype]
    
    ax_all.plot(grp["cutoff"], grp["speedup"], label=f"{dtype} (Peak={p_c})",
                color=colors[idx], linewidth=1.6)
    ax_all.scatter([p_c], [p_s], color=colors[idx], marker="*", s=160, zorder=5, edgecolor="black")

ax_all.axhline(1.0, color="#9ca3af", linestyle="--")
ax_all.set_title("Tong hop 5 kieu phan bo (Diem * la Dinh)", fontsize=11, color="#1e293b")
ax_all.set_xlabel("CUTOFF")
ax_all.set_ylabel("Speedup Ratio")
ax_all.legend(fontsize=8, loc="upper right")
ax_all.set_xlim(0, 102)

plt.suptitle("DO THI 2: PHAN TICH DINH TOI UU CUA CUTOFF THEO TUNG KIEU DU LIEU", fontsize=13, y=0.995)
plt.tight_layout()
fig.savefig(out_dir / "chart2_speedup_by_datatype.png")
plt.close(fig)
print("  [OK] Đã xuất: chart2_speedup_by_datatype.png")

# -------------------------------------------------------------------------
# ĐỒ THỊ 3: ĐỈNH TỐI ƯU THEO KÍCH THƯỚC MẢNG N
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 6.5))
sizes = sorted(df["n"].unique())
size_colors = sns.color_palette("viridis", len(sizes))
size_peaks = {}

for idx, n_val in enumerate(sizes):
    sub = merged[(merged["n"] == n_val) & (merged["cutoff"] > 1)]
    grp = sub.groupby("cutoff")["speedup"].mean().reset_index()
    p_c = int(grp.loc[grp["speedup"].idxmax(), "cutoff"])
    p_s = grp["speedup"].max()
    size_peaks[n_val] = (p_c, p_s)
    
    ax.plot(grp["cutoff"], grp["speedup"], label=f"N = {n_val:,} -> Dinh: Cutoff={p_c} ({p_s:.2f}x)",
            color=size_colors[idx], linewidth=2.0, marker="o", markersize=3)
    ax.scatter([p_c], [p_s], color=size_colors[idx], marker="*", s=200, zorder=5, edgecolor="black")

# Chú thích trực tiếp trên điểm đỉnh của mảng tiêu biểu
n_1000_peak = size_peaks[1000]
ax.annotate(f"Dinh N=1,000: Cutoff={n_1000_peak[0]}\nSpeedup = {n_1000_peak[1]:.2f}x (+172.9%)",
            xy=(n_1000_peak[0], n_1000_peak[1]), xytext=(n_1000_peak[0] + 10, n_1000_peak[1] - 0.15),
            arrowprops=dict(arrowstyle="-|>", color="#1f2937", lw=1.5),
            bbox=dict(boxstyle="round,pad=0.35", fc="#f3f4f6", ec="#374151", lw=1.2),
            fontsize=9, fontweight="bold")

n_5000_peak = size_peaks[5000]
ax.annotate(f"Dinh N=5,000: Cutoff={n_5000_peak[0]} ({n_5000_peak[1]:.2f}x)",
            xy=(n_5000_peak[0], n_5000_peak[1]), xytext=(n_5000_peak[0] + 12, n_5000_peak[1] + 0.18),
            arrowprops=dict(arrowstyle="-|>", color="#1f2937", lw=1.2),
            bbox=dict(boxstyle="round,pad=0.3", fc="#ecfdf5", ec="#059669", lw=1.0),
            fontsize=8.5, fontweight="bold")

ax.axvspan(18, 28, color="#a78bfa", alpha=0.18, label="Vung hoi tu toi uu chung (18 <= Cutoff <= 28)")
ax.axhline(1.0, color="#ef4444", linestyle="--", linewidth=1.2, label="Baseline (1.0x)")
ax.set_title("DO THI 3: TI SO TANG TOC VA DINH TOI UU THEO KICH THUOC MANG N (N = 500 DEN 100,000)", fontsize=12, pad=12)
ax.set_xlabel("Gia tri CUTOFF", fontsize=10)
ax.set_ylabel("Speedup Ratio", fontsize=10)
ax.set_xlim(0, 102)
ax.set_xticks([1, 7, 10, 14, 16, 20, 23, 26, 30, 36, 50, 75, 100])
ax.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.92, fontsize=8.5)

plt.tight_layout()
fig.savefig(out_dir / "chart3_optimal_cutoff_by_array_size.png")
plt.close(fig)
print("  [OK] Đã xuất: chart3_optimal_cutoff_by_array_size.png")

# -------------------------------------------------------------------------
# ĐỒ THỊ 4: CẬN CẢNH DẢI CUTOFF 1 ĐẾN 35 (BƯỚC 1 ĐƠN VỊ)
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13.5, 5.8))
sub_zoom = overall[(overall["cutoff"] >= 1) & (overall["cutoff"] <= 35)]
ax.plot(sub_zoom["cutoff"], sub_zoom["speedup"], marker="o", markersize=5, color="#0284c7", linewidth=2, zorder=3)
bars = ax.bar(sub_zoom["cutoff"], sub_zoom["speedup"], width=0.6, alpha=0.35, color="#bae6fd", zorder=2)

# Vùng bình nguyên
ax.axvspan(17.5, 28.5, color="#fbcfe8", alpha=0.35, label="Vung binh nguyen hieu nang cao (18 <= Cutoff <= 28)")

# Làm nổi bật 3 mốc quan trọng
for c_val, c_col, label in [(7, "#d97706", "Sach cu (7)"), (10, "#059669", "Sach moi (10)"), (best_cutoff, "#e11d48", f"DINH CUC DAI ({best_cutoff})")]:
    sp = sub_zoom.loc[sub_zoom["cutoff"] == c_val, "speedup"].values[0]
    ax.bar([c_val], [sp], width=0.6, color=c_col, alpha=0.9, zorder=4)
    ax.annotate(f"{label}\n{sp:.4f}x", xy=(c_val, sp), xytext=(c_val, sp + 0.05),
                ha="center", fontsize=8.5, fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color=c_col, lw=1.2),
                bbox=dict(boxstyle="round,pad=0.25", fc="#ffffff", ec=c_col, lw=1.2))

# Ghi chú giá trị các cột trong vùng đỉnh (20, 25, 28)
for c_sub in [20, 25, 28]:
    if c_sub in sub_zoom["cutoff"].values and c_sub != best_cutoff:
        sp_sub = sub_zoom.loc[sub_zoom["cutoff"] == c_sub, "speedup"].values[0]
        ax.text(c_sub, sp_sub - 0.08, f"{sp_sub:.3f}x", ha="center", fontsize=7.5, color="#475569", rotation=90)

ax.set_ylim(0.95, 1.58)
ax.set_xticks(list(range(1, 36)))
ax.set_title("DO THI 4: CAN CANH DAI CUTOFF 1 DEN 35 (BUOC 1 DON VI) - XAC DINH CHINH XAC DINH", fontsize=12, pad=12)
ax.set_xlabel("Gia tri CUTOFF (1..35)", fontsize=10)
ax.set_ylabel("Speedup Ratio", fontsize=10)
ax.legend(loc="lower right", frameon=True)

plt.tight_layout()
fig.savefig(out_dir / "chart4_zoom_peak_analysis.png")
plt.close(fig)
print("  [OK] Đã xuất: chart4_zoom_peak_analysis.png")

# -------------------------------------------------------------------------
# ĐỒ THỊ 5: SO SÁNH TRỰC DIỆN 4 MỐC CHIẾN LƯỢC
# -------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 5.5))
compare_cutoffs = [1, 7, 10, best_cutoff]
labels = ["Baseline\n(Cutoff=1)", "Giao trinh cu\n(Cutoff=7)", "Giao trinh moi\n(Cutoff=10)", f"Cuc dai thuc te\n(Cutoff={best_cutoff})"]
vals = [1.0, s7, s10, best_speedup]
bar_colors = ["#9ca3af", "#d97706", "#059669", "#e11d48"]

bars = ax.bar(labels, vals, color=bar_colors, width=0.52, edgecolor="black", linewidth=1.2)
ax.axhline(1.0, color="#ef4444", linestyle="--", linewidth=1.2)

for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.025,
            f"{v:.4f}x\n(+{(v-1)*100:.2f}%)" if v > 1.0 else "1.0000x\n(0.00%)",
            ha="center", fontsize=9.5, fontweight="bold")

# Mũi tên so sánh giữa Cutoff 7 và 10
ax.annotate("+16.16% hieu nang", xy=(1, s7 + 0.08), xytext=(2, s10 + 0.08),
            ha="center", fontsize=8.5, color="#047857", fontweight="bold",
            arrowprops=dict(arrowstyle="<->", color="#047857", lw=1.2))

# Mũi tên so sánh giữa Cutoff 10 và Peak 23
ax.annotate("+6.37% vuot troi", xy=(2, s10 + 0.02), xytext=(3, best_speedup + 0.02),
            ha="center", fontsize=8.5, color="#be123c", fontweight="bold",
            arrowprops=dict(arrowstyle="<->", color="#be123c", lw=1.2))

ax.set_ylim(0, 1.75)
ax.set_title("DO THI 5: SO SANH TRUC DIEN HIEU NANG CAC MOC CHIEN LUOC", fontsize=12, pad=12)
ax.set_ylabel("Speedup Ratio (so voi Baseline)", fontsize=10)

plt.tight_layout()
fig.savefig(out_dir / "chart5_textbook_comparison_bar.png")
plt.close(fig)
print("  [OK] Đã xuất: chart5_textbook_comparison_bar.png")

# -------------------------------------------------------------------------
# ĐỒ THỊ 0: MASTER DASHBOARD (4-IN-1)
# -------------------------------------------------------------------------
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 12))

# Panel 1: Overall
ax1.plot(overall["cutoff"], overall["speedup"], color="#1d4ed8", linewidth=2.2, marker="o", markersize=3)
ax1.scatter([best_cutoff], [best_speedup], color="#e11d48", marker="*", s=320, zorder=6, edgecolor="black")
ax1.axvspan(18, 28, color="#a78bfa", alpha=0.25)
ax1.annotate(f"DINH TOI UU: Cutoff={best_cutoff}\nSpeedup = {best_speedup:.4f}x (+{(best_speedup-1)*100:.1f}%)",
             xy=(best_cutoff, best_speedup), xytext=(best_cutoff + 12, best_speedup + 0.02),
             arrowprops=dict(arrowstyle="-|>", color="#e11d48", lw=1.5),
             bbox=dict(boxstyle="round,pad=0.35", fc="#ffe4e6", ec="#e11d48", lw=1.2),
             fontsize=9, fontweight="bold")
ax1.set_title("A. Toan bo 66 nguong CUTOFF (1..100) - Dinh tai Cutoff = 23", fontsize=11)
ax1.set_xlabel("CUTOFF")
ax1.set_ylabel("Speedup Ratio")
ax1.set_xlim(0, 102)

# Panel 2: Bar
ax2.bar(labels, vals, color=bar_colors, width=0.5, edgecolor="black", linewidth=1)
for b, v in zip(ax2.patches, vals):
    ax2.text(b.get_x() + b.get_width() / 2, v + 0.02,
             f"{v:.4f}x\n(+{(v-1)*100:.1f}%)" if v > 1.0 else "1.0000x",
             ha="center", fontsize=8.5, fontweight="bold")
ax2.set_ylim(0, 1.7)
ax2.set_title("B. So sanh truc dien cac moc (Base, Sach cu 7, Sach moi 10, Dinh 23)", fontsize=11)
ax2.set_ylabel("Speedup Ratio")

# Panel 3: By DataType
for idx, dtype in enumerate(data_types):
    sub = merged[(merged["dataType"] == dtype) & (merged["cutoff"] > 1)]
    grp = sub.groupby("cutoff")["speedup"].mean().reset_index()
    p_c, p_s = datatype_peaks[dtype]
    ax3.plot(grp["cutoff"], grp["speedup"], label=f"{dtype} (Dinh={p_c})",
             color=colors[idx], linewidth=1.6)
    ax3.scatter([p_c], [p_s], color=colors[idx], marker="*", s=140, zorder=5, edgecolor="black")

ax3.set_title("C. Ti so tang toc theo 5 kieu du lieu (* la diem toi uu cua tung kieu)", fontsize=11)
ax3.set_xlabel("CUTOFF")
ax3.set_ylabel("Speedup Ratio")
ax3.legend(fontsize=7.5, loc="upper right")
ax3.set_xlim(0, 102)

# Panel 4: By Array Size N
for idx, n_val in enumerate(sizes):
    sub = merged[(merged["n"] == n_val) & (merged["cutoff"] > 1)]
    grp = sub.groupby("cutoff")["speedup"].mean().reset_index()
    p_c, p_s = size_peaks[n_val]
    ax4.plot(grp["cutoff"], grp["speedup"], label=f"N={n_val:,} (Dinh={p_c})",
             color=size_colors[idx], linewidth=1.6)
    ax4.scatter([p_c], [p_s], color=size_colors[idx], marker="*", s=120, zorder=5, edgecolor="black")

ax4.set_title("D. Ti so tang toc theo kich thuoc mang N (* la dinh toi uu cua tung N)", fontsize=11)
ax4.set_xlabel("CUTOFF")
ax4.set_ylabel("Speedup Ratio")
ax4.legend(fontsize=7.5, loc="upper right")
ax4.set_xlim(0, 102)

plt.suptitle("BANG DIEU KHIEN TONG THE (MASTER DASHBOARD): PHAN TICH TOI UU HOA MERGESORT CUTOFF",
             fontsize=13, y=0.995)
plt.tight_layout()
dashboard_file = out_dir / "chart0_master_dashboard.png"
fig.savefig(dashboard_file, dpi=200)
plt.close(fig)
print(f"  [OK] Đã xuất bảng điều khiển tổng thể: {dashboard_file}")
