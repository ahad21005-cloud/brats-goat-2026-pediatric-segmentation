from pathlib import Path
import json
import shutil

PROJECT_DIR = Path("/hdd4/sines/gpl/ahad.sines/peds_brain_project")

SRC_ROOT = PROJECT_DIR / "data" / "nnUNet_raw"
SMOKE_ROOT = PROJECT_DIR / "smoke_test" / "nnUNet_raw"

src_candidates = sorted(SRC_ROOT.glob("Dataset503*"))
if not src_candidates:
    raise RuntimeError(f"No Dataset503 folder found in {SRC_ROOT}")

SRC = src_candidates[0]
DST = SMOKE_ROOT / "Dataset599_BraTSGoATSmoke"

print("=" * 80)
print("Creating isolated smoke dataset")
print(f"Source:      {SRC}")
print(f"Destination: {DST}")
print("=" * 80)

if DST.exists():
    print("Old smoke dataset found. Removing it safely...")
    shutil.rmtree(DST)

(DST / "imagesTr").mkdir(parents=True, exist_ok=True)
(DST / "labelsTr").mkdir(parents=True, exist_ok=True)

src_images = SRC / "imagesTr"
src_labels = SRC / "labelsTr"
src_json = SRC / "dataset.json"

if not src_images.exists():
    raise RuntimeError(f"Missing imagesTr: {src_images}")
if not src_labels.exists():
    raise RuntimeError(f"Missing labelsTr: {src_labels}")
if not src_json.exists():
    raise RuntimeError(f"Missing dataset.json: {src_json}")

label_files = sorted(src_labels.glob("*.nii.gz"))
if len(label_files) < 5:
    raise RuntimeError(f"Need at least 5 labels. Found {len(label_files)}")

selected = []
for lab in label_files:
    case_id = lab.name.replace(".nii.gz", "")
    imgs = sorted(src_images.glob(f"{case_id}_*.nii.gz"))
    if len(imgs) >= 1:
        selected.append((case_id, lab, imgs))
    if len(selected) == 5:
        break

if len(selected) < 5:
    raise RuntimeError("Could not find 5 complete cases with images and labels.")

print(f"Selected {len(selected)} cases:")

for case_id, lab, imgs in selected:
    print(f"  {case_id}: {len(imgs)} images")
    shutil.copy2(lab, DST / "labelsTr" / lab.name)
    for img in imgs:
        shutil.copy2(img, DST / "imagesTr" / img.name)

with open(src_json, "r") as f:
    ds = json.load(f)

ds["name"] = "BraTSGoATSmoke"
ds["description"] = "Isolated 5-case smoke test for BraTS-GoAT nnU-Net pipeline"
ds["numTraining"] = len(selected)

with open(DST / "dataset.json", "w") as f:
    json.dump(ds, f, indent=4)

print("=" * 80)
print("Smoke dataset created successfully.")
print(f"Smoke dataset path: {DST}")
print(f"Images copied: {len(list((DST / 'imagesTr').glob('*.nii.gz')))}")
print(f"Labels copied: {len(list((DST / 'labelsTr').glob('*.nii.gz')))}")
print("=" * 80)
