import json
from pathlib import Path

summary_path = Path("data/nnUNet_results/Dataset503_BraTSGoAT/nnUNetTrainer__nnUNetPlans__3d_fullres/fold_0/validation/summary.json")
out_path = Path("reports/fold0_best_worst_cases_2026_07_07.txt")

with open(summary_path) as f:
    s = json.load(f)

rows = []
for c in s["metric_per_case"]:
    pred = Path(c["prediction_file"]).name
    m = c["metrics"]
    dice1 = m["1"]["Dice"]
    dice2 = m["2"]["Dice"]
    dice3 = m["3"]["Dice"]
    avg = (dice1 + dice2 + dice3) / 3
    rows.append((avg, dice1, dice2, dice3, pred))

rows_sorted = sorted(rows, key=lambda x: x[0])

lines = []
lines.append("Fold 0 Best/Worst Internal Validation Cases")
lines.append("=" * 70)

lines.append("\nWorst 15 cases by average label Dice:")
for avg, d1, d2, d3, pred in rows_sorted[:15]:
    lines.append(f"{pred} | avg={avg:.4f} | NCR={d1:.4f} | ED={d2:.4f} | ET={d3:.4f}")

lines.append("\nBest 15 cases by average label Dice:")
for avg, d1, d2, d3, pred in rows_sorted[-15:][::-1]:
    lines.append(f"{pred} | avg={avg:.4f} | NCR={d1:.4f} | ED={d2:.4f} | ET={d3:.4f}")

out_path.write_text("\n".join(lines))
print(out_path)
print("\n".join(lines))
