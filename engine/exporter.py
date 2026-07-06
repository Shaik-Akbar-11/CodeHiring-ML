import csv
import os


class Exporter:

    def __init__(self):

        self.output_root = "output/Amazon"

        os.makedirs(
            self.output_root,
            exist_ok=True
        )

        self.headers = [
            "Company",
            "Role",
            "Section",
            "Topic",
            "Difficulty",
            "Question",
            "Option A",
            "Option B",
            "Option C",
            "Option D",
            "Answer",
            "Explanation"
        ]

    def save(self, question):

        section = question["section"].lower()

        if "quantitative" in section:
            filename = "quantitative.csv"

        elif "logical" in section:
            filename = "logical.csv"

        elif "verbal" in section:
            filename = "verbal.csv"

        else:
            filename = "others.csv"

        file = os.path.join(
            self.output_root,
            filename
        )

        file_exists = os.path.exists(file)

        with open(
            file,
            "a",
            newline="",
            encoding="utf-8"
        ) as csvfile:

            writer = csv.writer(csvfile)

            if not file_exists:
                writer.writerow(self.headers)

            writer.writerow([
                question["company"],
                question["role"],
                question["section"],
                question["topic"],
                question["difficulty"],
                question["question"],
                question["options"]["A"],
                question["options"]["B"],
                question["options"]["C"],
                question["options"]["D"],
                question["answer"],
                question["explanation"]
            ])

        print(f"✅ Question Saved -> {filename}")