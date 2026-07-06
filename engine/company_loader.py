import json
from pathlib import Path
import pandas as pd


class CompanyLoader:

    def __init__(self, knowledge_path):
        self.knowledge_path = Path(knowledge_path)

    def load_json(self, filename):

        file = self.knowledge_path / filename

        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_csv(self, filename):

        file = self.knowledge_path / filename

        return pd.read_csv(file)

    def load_all(self):

        return {

            "profile": self.load_json("company_profile.json"),

            "pattern": self.load_json("pattern.json"),

            "aptitude": self.load_csv("aptitude_topics.csv"),

            "logical": self.load_csv("logical_topics.csv"),

            "verbal": self.load_csv("verbal_topics.csv"),

            "coding": self.load_csv("coding_topics.csv")
        }