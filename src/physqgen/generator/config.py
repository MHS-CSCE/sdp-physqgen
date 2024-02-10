from io import StringIO
from json import load as loadJSON
from physqgen import generator

def parseQuestions(self, configTextIO: StringIO) -> list:
    """Parses a question config text stream for questions and returns a list of all contained question subclass objects."""
    questions: list = []

    dicts = loadJSON(configTextIO)
    for question in dicts:
        # uses getattr to construct the corresponding class described in the config
        # should change to use some kind of class ID instead of the name directly at some point, to prevent in-code class name changes from breaking old config files
        questions.append(getattr(generator, question["question"])(question["data"]))

    return questions
