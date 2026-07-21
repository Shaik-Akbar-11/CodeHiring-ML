import re


class Validator:

    REQUIRED_FIELDS = [
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

    REQUIRED_OPTIONS = ["A", "B", "C", "D"]

    def validate(self, question):

        errors = []

        # -----------------------------
        # Required Fields
        # -----------------------------
        for field in self.REQUIRED_FIELDS:

            if field not in question:
                errors.append(f"Missing field: {field}")

        if errors:
            return False, errors

        # -----------------------------
        # String Fields
        # -----------------------------
        for field in [
            "company",
            "role",
            "section",
            "topic",
            "difficulty",
            "question",
            "answer",
            "explanation"
        ]:

            value = question.get(field)

            if not isinstance(value, str):
                errors.append(f"{field} must be a string.")
                continue

            if len(value.strip()) == 0:
                errors.append(f"{field} cannot be empty.")

        # -----------------------------
        # Question
        # -----------------------------
        q = question["question"].strip()

        if len(q) < 25:
            errors.append("Question is too short.")

        # -----------------------------
        # Options
        # -----------------------------
        options = question["options"]

        if not isinstance(options, dict):

            errors.append("Options must be a dictionary.")

        else:

            if len(options) != 4:
                errors.append("Exactly four options are required.")

            for opt in self.REQUIRED_OPTIONS:

                if opt not in options:
                    errors.append(f"Missing option {opt}")
                    continue

                value = str(options[opt]).strip()

                if len(value) == 0:
                    errors.append(f"Option {opt} is empty.")

        # -----------------------------
        # Answer
        # -----------------------------
        if question["answer"] not in self.REQUIRED_OPTIONS:

            errors.append(
                "Answer must be one of A, B, C or D."
            )

        # -----------------------------
        # Explanation
        # -----------------------------
        explanation = question["explanation"].strip()

        if len(explanation) < 40:

            errors.append(
                "Explanation is too short."
            )

        # -----------------------------
        # Duplicate Options
        # -----------------------------
        if isinstance(options, dict):

            values = [
                str(v).strip().lower()
                for v in options.values()
            ]

            if len(values) != len(set(values)):
                errors.append(
                    "Duplicate options detected."
                )

        # -----------------------------
        # Answer Exists
        # -----------------------------
        if (
            isinstance(options, dict)
            and question["answer"] in options
        ):

            answer_text = options[
                question["answer"]
            ]

            if len(str(answer_text).strip()) == 0:

                errors.append(
                    "Correct answer is empty."
                )

        # -----------------------------
        # Basic Grammar Check
        # -----------------------------
        if not re.search(r"[?.!]$", q):

            errors.append(
                "Question should end with punctuation."
            )

        # -----------------------------
        # Final Result
        # -----------------------------
        if errors:

            return False, errors

        return True, []