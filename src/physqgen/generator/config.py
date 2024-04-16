"""
Stuart, February 10, 2024
"""

from dataclasses import dataclass

from physqgen import generator


@dataclass(slots=True)
class VariableConfig:
    variableType: str
    range: list[float | int]
    units: str
    displayName: str

@dataclass(slots=True)
class QuestionConfig:
    variableConfigs: list[VariableConfig]
    solveVariableType: str
    questionType: str
    text: str
    # correctRange default was agreed upon with client at 10%
    correctRange: float = 0.1

@dataclass(slots=True)
class Config:
    questionConfigs: list[QuestionConfig]

    @classmethod
    def fromFile(cls, dict):
        """Creates a config from a loaded json-formatted config file."""
        qConfigs = []
        for question in dict["questions"]:
            vConfigs = []
            for varType, data in question["variableConfig"].items():
                vConfigs.append(VariableConfig(varType, data["range"], data["units"], data["displayName"]))
            qConfigs.append(QuestionConfig(vConfigs, question["solveVariable"], question["question"], question["text"], question["correctRange"]))
        
        return cls(qConfigs)

# TODO: may need to put in separate file as it imports the full module
def generateQuestions(config: Config) -> list:
    """
    Generates a set of question subclass instances with randomized values based on the passed config data.\n
    Returns a list of those instances.
    """
    questions: list = []

    for questionConfig in config.questionConfigs:
        # should change to use some kind of class ID instead of the name directly at some point, to prevent in-code class name changes from breaking old config files
        # creates the class coresponding with the questionType, with the values from the config, and passes the QuestionConfig on.
        questions.append(getattr(generator, questionConfig.questionType)(config=questionConfig))

    return questions
