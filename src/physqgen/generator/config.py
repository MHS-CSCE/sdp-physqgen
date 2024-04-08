"""
Stuart, February 10, 2024
"""

from physqgen import generator

def generateQuestions(parsedConfig: dict) -> list:
    """
    Generates a set of question subclass instances with randomized values based on the passed config data.\n
    Returns a list of those instances.
    """
    questions: list = []

    dict = parsedConfig
    for question in dict["questions"]:
        # uses getattr to construct the corresponding class described in the config
        # should change to use some kind of class ID instead of the name directly at some point, to prevent in-code class name changes from breaking old config files
        if "correctRange" in question:
            questions.append(getattr(generator, question["question"])(variableConfig=question["variableConfig"], solveVariable=question["solveVariable"], text=question["text"], correctRange=question["correctRange"]))
        else:
            questions.append(getattr(generator, question["question"])(variableConfig=question["variableConfig"], solveVariable=question["solveVariable"], text=question["text"]))

    return questions
