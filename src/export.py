import json
import os


def export_results(results, filename="outputs/results.json"):
    os.makedirs("outputs", exist_ok=True)

    with open(filename, "w") as f:
        json.dump(results, f, indent=4)