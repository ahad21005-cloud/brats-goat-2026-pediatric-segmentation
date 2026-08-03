import synapseclient

TARGETS = {
    "with_ground_truth": "syn60084146",
    "without_ground_truth": "syn60084765",
}

syn = synapseclient.Synapse()
syn.login()

for name, synid in TARGETS.items():
    print("=" * 80)
    print(f"Testing: {name}")
    print(f"Synapse ID: {synid}")
    try:
        ent = syn.get(synid, downloadFile=False)
        print("ACCESS OK")
        print("Name:", getattr(ent, "name", "NA"))
        print("ID:", getattr(ent, "id", "NA"))
    except Exception as e:
        print("ACCESS FAILED")
        print("Error:", repr(e))
        raise
