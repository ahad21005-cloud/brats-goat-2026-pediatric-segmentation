import json
import math
from pathlib import Path

summary_path = Path("data/nnUNet_results/Dataset503_BraTSGoAT/nnUNetTrainer__nnUNetPlans__3d_fullres/fold_0/validation/summary.json")
out_path = Path("reports/fold0_best_worst_cases_nan_safe_2026_07_07.txt")

with open(summary_path) as f:
    s = json.load(f)

rows = []
nan_rows = []

for c in s["metric_per_case"]:
    pred = Path(c["prediction_file"]).name
    m = c["metrics"]

    d1 = m["1"]["Dice"]
    d2 = m["2"]["Dice"]
    d3 = m["3"]["Dice"]

    vals = [d1, d2, d3]
    valid_vals = [v for v in vals if not (isinstance(v, float) and math.isnan(v))]

    if len(valid_vals) == 0:
        avg = float("nan")
        nan_rows.append((avg, d1, d2, d3, pred))
        continue

    valid_avg = sum(valid_vals) / len(valid_vals)

    if len(valid_vals) < 3:
        nan_rows.append((valid_avg, d1, d2, d3, pred))
    else:
        rows.append((valid_avg, d1, d2, d3, pred))

rows_sorted = sorted(rows, key=lambda x: x[0])
nan_rows_sorted = sorted(nan_rows, key=lambda x: x[0])

lines = []
lines.append("Fold 0 Best/Worst Internal Validation Cases — NaN-safe")
lines.append("=" * 75)

lines.append("\nWorst 15 cases with all 3 labels valid:")
for avg, d1, d2, d3, pred in rows_sorted[:15]:
    lines.append(f"{pred} | avg={avg:.4f} | NCR={d1:.4f} | ED={d2:.4f} | ET={d3:.4f}")

lines.append("\nBest 15 cases with all 3 labels valid:")
for avg, d1, d2, d3, pred in rows_sorted[-15:][::-1]:
    lines.append(f"{pred} | avg={avg:.4f} | NCR={d1:.4f} | ED={d2:.4f} | ET={d3:.4f}")

lines.append("\nCases with at least one NaN label Dice:")
for avg, d1, d2, d3, pred in nan_rows_sorted[:30]:
    lines.append(f"{pred} | valid_avg={avg:.4f} | NCR={d1} | ED={d2} | ET={d3}")

out_path.write_text("\n".join(lines))
print(out_path)
print("\n".join(lines))
