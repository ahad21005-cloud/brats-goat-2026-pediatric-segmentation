from pathlib import Path
import traceback
import synapseclient

PROJECT_DIR = Path("/hdd4/sines/gpl/ahad.sines/peds_brain_project")
OUT_DIR = PROJECT_DIR / "data" / "raw_zip"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SYNID = "syn61457059"

print("=" * 90, flush=True)
print("BraTS-GoAT Validation download started", flush=True)
print(f"Synapse ID: {SYNID}", flush=True)
print(f"Output directory: {OUT_DIR}", flush=True)
print("=" * 90, flush=True)

syn = synapseclient.Synapse()
syn.login()

try:
    ent = syn.get(SYNID, downloadLocation=str(OUT_DIR))
    print("SUCCESS: validation data", flush=True)
    print(f"Saved to: {ent.path}", flush=True)
except Exception as e:
    print("ERROR during validation download", flush=True)
    print(repr(e), flush=True)
    traceback.print_exc()
    raise

print("=" * 90, flush=True)
print("Validation download completed", flush=True)
print("=" * 90, flush=True)
