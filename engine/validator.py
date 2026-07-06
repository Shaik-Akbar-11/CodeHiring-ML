import json


class Validator:

    def validate(self, question):

        errors = []

        # Required fields
        required_fields = [
            "company",
            "role",
            "section",
            "topic",
            "difficulty",
            "question",
            "options",
            "answer",
            "explanation"
        ]

        for field in required_fields:
            if field not in question:
                errors.append(f"Missing field: {field}")

        if errors:
            return False, errors

        # Question
        if not isinstance(question["question"], str) or len(question["question"].strip()) < 20:
            errors.append("Question is too short.")

        # Options
        if not isinstance(question["options"], dict):
            errors.append("Options must be a dictionary.")
        else:

            required_options = ["A", "B", "C", "D"]

            for option in required_options:
                if option not in question["options"]:
                    errors.append(f"Missing option {option}")

            if len(question["options"]) != 4:
                errors.append("There must be exactly 4 options.")

        # Answer
        if question["answer"] not in ["A", "B", "C", "D"]:
            errors.append("Answer must be A/B/C/D.")

        # Explanation
        if len(question["explanation"].strip()) < 30:
            errors.append("Explanation too short.")

        if len(errors) == 0:
            return True, []

        return False, errors