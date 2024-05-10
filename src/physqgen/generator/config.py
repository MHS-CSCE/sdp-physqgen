from dataclasses import dataclass
from os import listdir
from os.path import exists, join
from shutil import copy as shcopy

from physqgen import generator
from physqgen.generator.variables import Variable


@dataclass(slots=True)
class VariableConfig:
    """
    Configuration for a specific variable in a question. Can be used to generate random Variables.\n
    Attributes:\n
        range is a list containing the upper and lower bounds the value should be randomized within,\n
        See Variable class for additional attributes\n
            variableType is refered to as name in Variable
    """
    variableType: str
    range: list[float | int]
    units: str
    displayName: str
    decimalPlaces: int = 3

    def getRandomVariable(self) -> Variable:
        """Generates a Variable with random value based on this configuration."""
        return Variable(range=self.range, name=self.variableType, units=self.units, displayName=self.displayName, decimalPlaces=self.decimalPlaces)

@dataclass(slots=True)
class QuestionConfig:
    variableConfigs: list[VariableConfig]
    solveVariable: str
    questionType: str
    text: str
    imageName: str
    # correctRange default was agreed upon with client at 10%
    correctRange: float = 0.1

@dataclass(slots=True)
class Config:
    questionConfigs: list[QuestionConfig]

    @classmethod
    def fromFile(cls, dict: dict[str, list[dict]]):
        """Creates a config from a loaded json-formatted config file."""
        qConfigs = []
        for question in dict["questions"]:
            vConfigs = []
            # use pop to remore the value that doesn't need to go to questionconfig constructor
            for varType, data in question.pop("variableConfig").items():
                vConfigs.append(VariableConfig(varType, **data))
            qConfigs.append(QuestionConfig(vConfigs, **question))
        
        return cls(qConfigs)

    def generateQuestions(self) -> list:
        """
        Generates a set of question subclass instances with randomized Variable values.\n
        Returns the list of question subclass instances.
        """
        questions: list = []

        for questionConfig in self.questionConfigs:
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
