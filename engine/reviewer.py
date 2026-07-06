import json
from engine.generator import Generator


class Reviewer:

    def __init__(self):
        self.generator = Generator()

    def review(self, question_json: str):

        prompt = f"""
Review this aptitude question.

Check only:

1. Mathematics is correct.
2. Correct answer is correct.
3. Explanation matches answer.
4. Topic matches.
5. Difficulty matches.
6. Question is original.

Reject ONLY if any of the above fails.

Return ONLY JSON.

{{
    "accepted": true,
    "score": 95,
    "company_match": true,
    "difficulty_match": true,
    "mathematics_correct": true,
    "answer_correct": true,
    "explanation_correct": true,
    "original": true,
    "errors":[]
}}

Question:

{question_json}
"""

        response = self.generator.generate(prompt)

        response = (
            response.replace("```json", "")
                    .replace("```", "")
                    .strip()
        )

        try:
            return json.loads(response)

        except Exception:

            return {
                "accepted": False,
                "score": 0,
                "company_match": False,
                "difficulty_match": False,
                "mathematics_correct": False,
                "answer_correct": False,
                "explanation_correct": False,
                "original": False,
                "errors": [
                    "Reviewer returned invalid JSON."
                ]
            }