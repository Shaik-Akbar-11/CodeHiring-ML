class DatasetBuilder:

    def __init__(self, topics):

        self.topics = topics

        self.difficulties = [
            "Easy",
            "Medium",
            "Hard"
        ]

    def build(self):

        dataset = []

        for topic in self.topics:

            for difficulty in self.difficulties:

                dataset.append({

                    "topic": topic,

                    "difficulty": difficulty,

                    "count": 100

                })

        return dataset