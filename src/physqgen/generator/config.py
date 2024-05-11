from dataclasses import dataclass
from json import load
from os import listdir
from os.path import exists, join
from shutil import copy as shcopy

from physqgen.generator.question import QUESTION_CONSTRUCTORS


@dataclass(slots=True)
class VariableConfig:
    """
    Configuration for a specific variable in a question. Can be used to generate random Variables.\n
    Attributes:\n
        range is a list containing the upper and lower bounds the value should be randomized within,\n
        See Variable class for additional attributes\n
            variableType is refered to as name in Variable\n
            does not have a uuid
    """
    variableName: str
    range: list[float | int]
    units: str
    displayName: str
    decimalPlaces: int = 3

@dataclass(slots=True)
class QuestionConfig:
    """
    Configuration for a specific question in a configuration. Can be used to generate a question with randomized variables.\n
    Attributes:\n
        See Question for attributes, excluding class variables.
            variables is also replaced by variablesConfigs, which hold VariblesConfig objects instead of Variable objects\n
            does not have a uuid
    """
    variableConfigs: list[VariableConfig]
    answerVariableName: str
    questionType: str
    text: str
    imageFilename: str
    # default was agreed upon with client at 10%
    correctLeeway: float = 0.1

    def getRandomQuestion(self):
        """Generates a Question with random Variables based on this configuration."""
        # creates the class coresponding to questionType, with the values from the config
        return QUESTION_CONSTRUCTORS[self.questionType].fromConfig(self)

@dataclass(slots=True)
class Config:
    """
    The configuration for question generation. Allows random generation of question as per the configuration file specified.\n
    Attributes:\n
        questionConfigs (list[QuestionConfig]): configurations for each question
    """
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
        """Returns the list of question subclass instances with randomized Variable values."""
        return [questionConfig.getRandomQuestion() for questionConfig in self.questionConfigs]

def copyQuestionImagesToServerFolder(imageFolderPath: str, movedImagesPath: str) -> None:
    """Copies files from imageFolderPath to movedImagesPath. This is intended to make image files available to ber displayed on the server, if they are referenced in any configs."""
    # for the pathname-matching quick solution: https://stackoverflow.com/questions/11903037/copy-all-jpg-file-in-a-directory-to-another-directory-in-python
    for originalFileName in listdir(sourcePath := join(imageFolderPath)):
        if not exists(movedFilePath := join(movedImagesPath, originalFileName)):
            shcopy(join(sourcePath, originalFileName), movedFilePath)

def registerConfig(configFolderPath: str) -> Config:
    """Stores the current Config for duration of program run."""
    # get config on run
    global appConfig
    with open(join(configFolderPath, "active_config.json")) as file:
        with open(join(configFolderPath, load(file)["activeConfigName"])) as configFile:
            appConfig = Config.fromFile(load(configFile))
    return appConfig

