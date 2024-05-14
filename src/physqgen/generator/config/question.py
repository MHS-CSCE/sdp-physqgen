from dataclasses import dataclass

from physqgen.generator.question import QUESTION_CONSTRUCTORS


@dataclass(slots=True)
class QuestionConfig:
    """
    Configuration for a specific question in a configuration. Can be used to generate a Question with randomized Variables.\n
    Attributes:\n
        See Question for attributes, excluding class variable, which is instead stored in the questionType instance variable\n
            variables is also replaced by variablesConfigs, which hold VariblesConfig objects instead of Variable objects\n
            does not have a uuid
    """
    variableConfigs: list # list[VariableConfig], can't annotate because of circular references
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
