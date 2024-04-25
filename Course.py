class Course:
    def __init__(self, topic, definition, difficulty):
        self.topic = topic
        self.definition = definition
        self.difficulty = difficulty

    def print_topic(self):
        print(f"Topic: {self.topic}")
        print(f"Definition: {self.definition}")
        print(f"Difficulty: {self.difficulty}")

    def update_difficulty(self, new_difficulty):
        self.difficulty = new_difficulty

    def update_definition(self, new_definition):
        self.definition = new_definition