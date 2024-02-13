from io import StringIO
from json import load as loadJSON
from physqgen import generator

def parseQuestions(configTextIO: StringIO) -> list:
    """Parses a question config text stream for questions and returns a list of all contained question subclass objects."""
    questions: list = []

    dict = loadJSON(configTextIO)
    for question in dict["questions"]:
        # uses getattr to construct the corresponding class described in the config
        # should change to use some kind of class ID instead of the name directly at some point, to prevent in-code class name changes from breaking old config files
        if "correctRange" in question:
            questions.append(getattr(generator, question["question"])(variableConfig=question["variableConfig"], solveVariable=question["solveVariable"], text=question["text"], correctRange=question["correctRange"]))
        else:
            questions.append(getattr(generator, question["question"])(variableConfig=question["variableConfig"], solveVariable=question["solveVariable"], text=question["text"]))

    return questions
