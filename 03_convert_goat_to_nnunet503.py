from pathlib import Path
import os
import shutil
import json

PROJECT_DIR = Path("/hdd4/sines/gpl/ahad.sines/peds_brain_project")

WITH_GT_ROOT = PROJECT_DIR / "data" / "extracted" / "with_gt"
VAL_ROOT = PROJECT_DIR / "data" / "extracted" / "validation"

OUT_ROOT = PROJECT_DIR / "data" / "nnUNet_raw" / "Dataset503_BraTSGoAT"
IMAGES_TR = OUT_ROOT / "imagesTr"
LABELS_TR = OUT_ROOT / "labelsTr"
IMAGES_TS = OUT_ROOT / "imagesTs"

MODALITIES = {
    "t1n": "0000",
    "t1c": "0001",
    "t2w": "0002",
    "t2f": "0003",
}

def ensure_dirs():
    for p in [IMAGES_TR, LABELS_TR, IMAGES_TS]:
        p.mkdir(parents=True, exist_ok=True)

def link_or_copy(src: Path, dst: Path):
    """
    Use hardlink if possible to save disk space and time.
    If hardlink fails, fall back to normal copy.
    """
    if dst.exists():
        return

    try:
        os.link(src, dst)
    except Exception:
        shutil.copy2(src, dst)

def find_case_dirs(root: Path):
    return sorted([p for p in root.rglob("BraTS-GoAT-*") if p.is_dir()])

def copy_training_cases():
    case_dirs = find_case_dirs(WITH_GT_ROOT)
    bad = []
    copied = 0

    print("=" * 90, flush=True)
    print("Converting With-GT training cases", flush=True)
    print("=" * 90, flush=True)
    print("Found case dirs:", len(case_dirs), flush=True)

    for d in case_dirs:
        case_id = d.name
        missing = []

        for mod in MODALITIES:
            f = d / f"{case_id}-{mod}.nii.gz"
            if not f.exists():
                missing.append(mod)

        seg = d / f"{case_id}-seg.nii.gz"
        if not seg.exists():
            missing.append("seg")

        if missing:
            bad.append((case_id, missing))
            continue

        for mod, channel in MODALITIES.items():
            src = d / f"{case_id}-{mod}.nii.gz"
            dst = IMAGES_TR / f"{case_id}_{channel}.nii.gz"
            link_or_copy(src, dst)

        link_or_copy(seg, LABELS_TR / f"{case_id}.nii.gz")

        copied += 1
        if copied % 100 == 0:
            print(f"Copied/linked training cases: {copied}", flush=True)

    print("Training cases copied/linked:", copied, flush=True)
    print("Bad training cases:", len(bad), flush=True)

    if bad:
        print("First bad training cases:", flush=True)
        for x in bad[:50]:
            print(x, flush=True)
        raise RuntimeError("Bad/incomplete training cases found.")

    return copied

def copy_validation_cases_as_imagesTs():
    case_dirs = find_case_dirs(VAL_ROOT)
    bad = []
    copied = 0

    print("=" * 90, flush=True)
    print("Converting validation cases into imagesTs", flush=True)
    print("=" * 90, flush=True)
    print("Found validation case dirs:", len(case_dirs), flush=True)

    for d in case_dirs:
        case_id = d.name
        missing = []

        for mod in MODALITIES:
            f = d / f"{case_id}-{mod}.nii.gz"
            if not f.exists():
                missing.append(mod)

        if missing:
            bad.append((case_id, missing))
            continue

        for mod, channel in MODALITIES.items():
            src = d / f"{case_id}-{mod}.nii.gz"
            dst = IMAGES_TS / f"{case_id}_{channel}.nii.gz"
            link_or_copy(src, dst)

        copied += 1
        if copied % 100 == 0:
            print(f"Copied/linked validation cases: {copied}", flush=True)

    print("Validation cases copied/linked:", copied, flush=True)
    print("Bad validation cases:", len(bad), flush=True)

    if bad:
        print("First bad validation cases:", flush=True)
        for x in bad[:50]:
            print(x, flush=True)
        raise RuntimeError("Bad/incomplete validation cases found.")

    return copied

def write_dataset_json(num_training: int):
    dataset = {
        "channel_names": {
            "0": "t1n",
            "1": "t1c",
            "2": "t2w",
            "3": "t2f"
        },
        "labels": {
            "background": 0,
            "NCR": 1,
            "ED": 2,
            "ET": 3
        },
        "numTraining": num_training,
        "file_ending": ".nii.gz"
    }

    with open(OUT_ROOT / "dataset.json", "w") as f:
        json.dump(dataset, f, indent=4)

    print("=" * 90, flush=True)
    print("dataset.json written", flush=True)
    print(OUT_ROOT / "dataset.json", flush=True)

def main():
    ensure_dirs()

    n_train = copy_training_cases()
    n_val = copy_validation_cases_as_imagesTs()
    write_dataset_json(n_train)

    print("=" * 90, flush=True)
    print("CONVERSION COMPLETE", flush=True)
    print("=" * 90, flush=True)
    print("Output:", OUT_ROOT, flush=True)
    print("imagesTr files:", len(list(IMAGES_TR.glob("*.nii.gz"))), flush=True)
    print("labelsTr files:", len(list(LABELS_TR.glob("*.nii.gz"))), flush=True)
    print("imagesTs files:", len(list(IMAGES_TS.glob("*.nii.gz"))), flush=True)
    print("Training cases:", n_train, flush=True)
    print("Validation cases:", n_val, flush=True)

if __name__ == "__main__":
    main()
