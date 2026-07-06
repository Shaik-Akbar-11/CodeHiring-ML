class PromptBuilder:

    def __init__(self, profile, pattern):

        self.profile = profile
        self.pattern = pattern

    def build_prompt(self, section, topic, difficulty):

        company = self.profile["company"]
        role = self.profile["role"]

        question_style = self.pattern["question_style"]
        language = self.pattern["language"]
        real_world = self.pattern["real_world_context"]
        reasoning = self.pattern["multi_step_reasoning"]
        calculator = self.pattern["calculator_allowed"]

        rules = "\n".join(
            [f"- {rule}" for rule in self.pattern["rules"]]
        )

        # -----------------------------
        # Difficulty Mapping
        # -----------------------------
        difficulty_key = difficulty

        if difficulty not in self.pattern["difficulty"]:

            mapping = {
                "Easy-Medium": "Medium",
                "Medium-Hard": "Hard",
                "Easy-Hard": "Hard",
                "Very Easy": "Easy",
                "Very Hard": "Hard"
            }

            difficulty_key = mapping.get(
                difficulty,
                "Medium"
            )

        diff = self.pattern["difficulty"][difficulty_key]

        steps = diff["steps"]
        time = diff["time"]

        prompt = f"""
You are a Senior Assessment Architect working for {company}.

Design ONE ORIGINAL {section} question exactly as it would appear in a real {company} Online Assessment.

==================================================
COMPANY DETAILS
==================================================

Company : {company}

Role : {role}

Section : {section}

Topic : {topic}

Difficulty : {difficulty}

==================================================
COMPANY PATTERN
==================================================

Question Style : {question_style}

Language : {language}

Real World Context : {real_world}

Multi Step Reasoning : {reasoning}

Calculator Allowed : {calculator}

Reasoning Steps : {steps}

Expected Solving Time : {time}

==================================================
RULES
==================================================

{rules}

==================================================
QUALITY REQUIREMENTS
==================================================

Before returning the question verify internally:

1. Mathematics is 100% correct.
2. Answer is correct.
3. Explanation exactly matches the answer.
4. Topic is {topic}.
5. Section is {section}.
6. Difficulty is {difficulty}.
7. JSON is valid.
8. Question is completely original.

If any verification fails,
discard the question and generate another one.

==================================================
OUTPUT FORMAT
==================================================

Return ONLY valid JSON.

Do NOT use markdown.

Do NOT use ```json.

Return EXACTLY:

{{
    "company":"{company}",
    "role":"{role}",
    "section":"{section}",
    "topic":"{topic}",
    "difficulty":"{difficulty}",
    "question":"",
    "options": {{
        "A":"",
        "B":"",
        "C":"",
        "D":""
    }},
    "answer":"A",
    "explanation":""
}}

Return nothing except JSON.
"""

        return prompt.strip()