import json
from pathlib import Path

summary_path = Path("data/nnUNet_results/Dataset503_BraTSGoAT/nnUNetTrainer__nnUNetPlans__3d_fullres/fold_0/validation/summary.json")
out_path = Path("reports/fold0_validation_summary_2026_07_07.txt")

with open(summary_path) as f:
    s = json.load(f)

fg = s["foreground_mean"]
mean = s["mean"]
cases = s["metric_per_case"]

lines = []
lines.append("BraTS-GoAT Dataset503 nnU-Net Fold 0 Internal Validation Summary")
lines.append("=" * 70)
lines.append(f"Number of internal validation cases: {len(cases)}")
lines.append("")
lines.append("Foreground mean:")
lines.append(f"  Dice: {fg['Dice']:.6f}")
lines.append(f"  IoU:  {fg['IoU']:.6f}")
lines.append("")
lines.append("Raw label-wise mean Dice:")
lines.append(f"  Label 1 NCR: {mean['1']['Dice']:.6f}")
lines.append(f"  Label 2 ED:  {mean['2']['Dice']:.6f}")
lines.append(f"  Label 3 ET:  {mean['3']['Dice']:.6f}")
lines.append("")
lines.append("Note:")
lines.append("  This is nnU-Net internal fold-0 validation on the training GT split.")
lines.append("  It is label-wise 1/2/3 validation, not final BraTS region-wise ET/TC/WT scoring.")

out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text("\n".join(lines))
print(out_path)
print("\n".join(lines))
