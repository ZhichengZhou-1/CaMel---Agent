from runs.demo_benign import main as benign_main
from runs.demo_attack import main as attack_main
import importlib
import sys


def run():
    print("Running benign scenario...")
    try:
        benign_main()
        benign_ok = True
    except Exception as e:
        print("Benign scenario error:", e)
        benign_ok = False

    print("\nRunning attack scenario...")
    try:
        attack_main()
        attack_ok = True
    except Exception as e:
        print("Attack scenario runtime error:", e)
        attack_ok = False

    print("\nSummary:")
    print("Benign run OK:", benign_ok)
    print("Attack run OK (no crash):", attack_ok)
    print("Note: attack should be BLOCKED by policies (PermissionError).")


if __name__ == "__main__":
    run()
