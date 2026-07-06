import csv
import os


class Exporter:

    def __init__(self):

        self.output_dir = "output/Amazon"

        os.makedirs(self.output_dir, exist_ok=True)

        self.file = os.path.join(
            self.output_dir,
            "aptitude.csv"
        )

        if not os.path.exists(self.file):

            with open(
                self.file,
                "w",
                newline="",
                encoding="utf-8"
            ) as csvfile:

                writer = csv.writer(csvfile)

                writer.writerow([
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
                ])

    def save(self, question):

        with open(
            self.file,
            "a",
            newline="",
            encoding="utf-8"
        ) as csvfile:

            writer = csv.writer(csvfile)

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

        print("✅ Question Saved")