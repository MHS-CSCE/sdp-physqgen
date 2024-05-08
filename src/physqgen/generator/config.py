from dataclasses import dataclass

from physqgen import generator

from shutil import copy as shcopy
from os.path import join, exists
from os import listdir


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
    img: str
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
            qConfigs.append(QuestionConfig(vConfigs, question["solveVariable"], question["question"], question["text"], question["image"], question["correctRange"]))
        
        return cls(qConfigs)

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

def copyQuestionImagesToServerFolder(imageFolderPath: str, movedImagesPath: str) -> None:
    """Copies files from ./configs/images to ./src/physqgen/app/static/images. This will make image files available to ber displayed on the server, if they are referenced in any configs."""
    # for the pathname-matching quick solution: https://stackoverflow.com/questions/11903037/copy-all-jpg-file-in-a-directory-to-another-directory-in-python
    for originalFileName in listdir(sourcePath := join(imageFolderPath)):
        if not exists(movedFilePath := join(movedImagesPath, originalFileName)):
            shcopy(join(sourcePath, originalFileName), movedFilePath)
