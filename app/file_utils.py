import json
from pathlib import Path


def save_json(data, filepath):

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


def save_text(data, filepath):

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        for row in data:

            f.write(
                f"[{row['start']:.2f}-{row['end']:.2f}]\n"
            )

            f.write(
                row["text"] + "\n\n"
            )