from dataclasses import dataclass
from json import load
from os import listdir
from os.path import exists, join
from shutil import copy as shcopy

from physqgen.generator.config.question import QuestionConfig
from physqgen.generator.config.variable import VariableConfig


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
