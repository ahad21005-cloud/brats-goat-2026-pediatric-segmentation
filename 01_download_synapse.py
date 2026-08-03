from pathlib import Path
import time
import traceback
import synapseclient

PROJECT_DIR = Path("/hdd4/sines/gpl/ahad.sines/peds_brain_project")
OUT_DIR = PROJECT_DIR / "data" / "raw_zip"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TARGETS = [
    ("with_ground_truth", "syn60084146"),
    ("without_ground_truth", "syn60084765"),
]

def show_files():
    print("\nCurrent raw_zip contents:", flush=True)
    for p in sorted(OUT_DIR.glob("*")):
        try:
            size_gb = p.stat().st_size / (1024 ** 3)
            print(f"  {p.name}  {size_gb:.2f} GB", flush=True)
        except Exception:
            print(f"  {p.name}", flush=True)

print("=" * 90, flush=True)
print("BraTS-GoAT Synapse download started", flush=True)
print(f"Output directory: {OUT_DIR}", flush=True)
print("=" * 90, flush=True)

syn = synapseclient.Synapse()
syn.login()

show_files()

for name, synid in TARGETS:
    print("\n" + "=" * 90, flush=True)
    print(f"Starting download: {name}", flush=True)
    print(f"Synapse ID: {synid}", flush=True)
    print("=" * 90, flush=True)

    success = False

    for attempt in range(1, 4):
        try:
            print(f"Attempt {attempt}/3", flush=True)
            ent = syn.get(synid, downloadLocation=str(OUT_DIR))
            print(f"SUCCESS: {name}", flush=True)
            print(f"Saved to: {ent.path}", flush=True)
            success = True
            break

        except KeyboardInterrupt:
            print("Interrupted by user.", flush=True)
            raise

        except Exception as e:
            print(f"ERROR during {name}, attempt {attempt}/3", flush=True)
            print(repr(e), flush=True)
            traceback.print_exc()
            if attempt < 3:
                print("Waiting 60 seconds before retry...", flush=True)
                time.sleep(60)

    if not success:
        raise RuntimeError(f"Failed to download {name} after 3 attempts.")

    show_files()
    time.sleep(10)

print("\n" + "=" * 90, flush=True)
print("All downloads completed successfully.", flush=True)
print("=" * 90, flush=True)
show_files()
