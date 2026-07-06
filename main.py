import json

from engine.company_loader import CompanyLoader
from engine.prompt_builder import PromptBuilder
from engine.generator import Generator
from engine.validator import Validator
from engine.exporter import Exporter


MAX_ATTEMPTS = 5
QUESTIONS_PER_TOPIC = 3


def main():

    print("\n========== CODEHIRING AI DATASET ENGINE ==========\n")

    # Load Company Knowledge
    loader = CompanyLoader("knowledge/Amazon")
    data = loader.load_all()

    print("✅ Company Loaded Successfully\n")

    # Initialize Modules
    builder = PromptBuilder(
        data["profile"],
        data["pattern"]
    )

    generator = Generator()
    validator = Validator()
    exporter = Exporter()

    # Load aptitude topics
    topics = data["aptitude"]

    total_saved = 0

    # Loop through each topic
    for _, row in topics.iterrows():

        topic = row["topic"]
        difficulty = row["difficulty"]

        print("\n" + "=" * 80)
        print(f"TOPIC : {topic}")
        print(f"DIFFICULTY : {difficulty}")
        print("=" * 80)

        saved = 0

        while saved < QUESTIONS_PER_TOPIC:

            print(f"\nGenerating Question {saved + 1}/{QUESTIONS_PER_TOPIC}")

            accepted = False
            attempt = 1

            while not accepted and attempt <= MAX_ATTEMPTS:

                print(f"Attempt : {attempt}")

                prompt = builder.build_prompt(
                    topic=topic,
                    difficulty=difficulty
                )

                try:

                    response = generator.generate(prompt)

                    clean_response = (
                        response.replace("```json", "")
                                .replace("```", "")
                                .strip()
                    )

                    question = json.loads(clean_response)

                except Exception as e:

                    print("❌ Invalid JSON")
                    print(e)

                    attempt += 1
                    continue

                # Python Validation
                valid, errors = validator.validate(question)

                print("\n========== VALIDATION ==========")

                if valid:
                    print("✅ Validation Passed")
                else:
                    print("❌ Validation Failed")
                    print(errors)

                accepted = valid

                if accepted:

                    exporter.save(question)

                    saved += 1
                    total_saved += 1

                    print(f"\n✅ Saved ({saved}/{QUESTIONS_PER_TOPIC})")

                else:

                    print("\n❌ Rejected")

                attempt += 1

            if not accepted:
                print(f"\n⚠ Skipping {topic} after {MAX_ATTEMPTS} failed attempts.")

    print("\n========================================")
    print("DATASET GENERATION COMPLETED")
    print(f"TOTAL QUESTIONS SAVED : {total_saved}")
    print("========================================")


if __name__ == "__main__":
    main()