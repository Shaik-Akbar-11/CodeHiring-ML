import json
from pathlib import Path
import pandas as pd


class CompanyLoader:

    def __init__(self, knowledge_path):
        self.knowledge_path = Path(knowledge_path)

    def load_json(self, filename):
        file = self.knowledge_path / filename

        if not file.exists():
            raise FileNotFoundError(f"{filename} not found.")

        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_csv(self, filename):
        file = self.knowledge_path / filename

        if not file.exists():
            raise FileNotFoundError(f"{filename} not found.")

        return pd.read_csv(file)

    def load_all(self):

        return {

            # ==========================
            # Company Information
            # ==========================
            "profile": self.load_json("company_profile.json"),
            "preferences": self.load_json("company_preferences.json"),
            "insights": self.load_json("company_insights.json"),
            "metadata": self.load_json("metadata.json"),

            # ==========================
            # Assessment Structure
            # ==========================
            "oa_rounds": self.load_json("oa_rounds.json"),
            "oa_platforms": self.load_json("oa_platforms.json"),
            "section_distribution": self.load_json("section_distribution.json"),
            "scoring_rules": self.load_json("scoring_rules.json"),
            "previous_patterns": self.load_json("previous_patterns.json"),
            "interview_pattern": self.load_json("interview_pattern.json"),
            "hiring_statistics": self.load_json("hiring_statistics.json"),

            # ==========================
            # Generation Rules
            # ==========================
            "question_generation_rules": self.load_json("question_generation_rules.json"),
            "validation_rules": self.load_json("validation_rules.json"),
            "constraints": self.load_json("constraints.json"),
            "coding_constraints": self.load_json("coding_constraints.json"),
            "difficulty_rules": self.load_json("difficulty_rules.json"),
            "prompt_templates": self.load_json("company_prompt_templates.json"),

            # ==========================
            # Question Templates
            # ==========================
            "question_templates": self.load_json("question_templates.json"),

            # ==========================
            # Pattern
            # ==========================
            "pattern": self.load_json("pattern.json"),

            # ==========================
            # Topic CSVs
            # ==========================
            "aptitude": self.load_csv("aptitude_topics.csv"),
            "logical": self.load_csv("logical_topics.csv"),
            "verbal": self.load_csv("verbal_topics.csv"),
            "coding": self.load_csv("coding_topics.csv"),
            "company_pattern": self.load_csv("company_pattern.csv")
        }