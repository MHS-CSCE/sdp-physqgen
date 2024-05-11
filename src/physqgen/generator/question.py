from dataclasses import dataclass, field
from math import sqrt
from typing import Literal
from uuid import UUID, uuid4  # uuid4 doesn't include private information

from physqgen.database import executeOnDatabase
from physqgen.generator.config import QuestionConfig
from physqgen.generator.variables import Variable


@dataclass
class Question:
    """
    Base class for all question implementations. Can be generated from a configution, which creates a question with random Variables, or from stored data.\n
    Subclasses should implement snake case properties for each variable they involve, which pull the value if it is set or solve for it if not. See KinematicsQuestion for an example. Subclasses need to include valid variables in docs.\n
    Attributes:\n
        answerVariableName (str): value of the name property of the Variable to treat as the answer,\n
        variables (list[Variable]): relevant variables for the question, may not include Variables for every name in POSSIBLE_VARIABLES if they are not relevant,\n
        correctLeeway (float): allowed factor variance from the calculated answer when determining whether a submission is correct,\n
        imageFilename (str): filename of the image to display,\n
        text (str): displayed text,\n
        numberTries (int): number of submissions checked,\n
        correct (bool): whether the question has been completed,\n
        active (bool): used in conjunction with correct for completion tracking,\n
        uuid (UUID): unique question uuid,\n
        questionType (str): identifier for question subclass, used as a key in the QUESTION_CONSTRUCTORS dict, needs to be overriden in subclasses and addes to said dict
    """
    answerVariableName: str
    variables: list[Variable]
    correctLeeway: float

    text: str
    imageFilename: str
    numberTries: int = 0
    correct: bool = False
    active: bool = False

    uuid: UUID = field(default_factory=uuid4)

    # needs to be overriden in inheriting classes
    questionType = str

    @classmethod
    def fromConfig(cls, questionConfig: QuestionConfig):
        """Creates an randomized instance of cls from the passed configuration."""
        variables: list[Variable] = []
        for varConfig in questionConfig.variableConfigs:
            variables.append(Variable.fromConfig(varConfig))

        # get the subclass constructor
        questionClass = QUESTION_CONSTRUCTORS[questionConfig.questionType]

        question = questionClass(
            answerVariableName=questionConfig.answerVariableName.lower(),
            variables=variables,
            correctLeeway=questionConfig.correctLeeway,
            imageFilename=questionConfig.imageFilename,
            text=questionConfig.text
        )

        # add a variable for the answer to the question
        question.variables.append(
            Variable(
                variableName=questionConfig.answerVariableName,
                value=getattr(questionClass, questionConfig.answerVariableName.lower())
            )
        )

        return question
    
    @classmethod
    def fromDatabase(_, databasePath: str, questionUUID: str | UUID):
        """
        Returns the appropriate Question subclass for data in the database coresponding to the given uuid.\n
        Does not use the class it is called on directly. This is still marked as a classmethod because it fulfills the purpose of one, constructing an instance of the class, except it will search for the appropriate subclass instead.
        """
        sql = f'''SELECT (
            QUESTION_TYPE,
            ANSWER_VARIABLE_NAME,
            CORRECT_LEEWAY,
            TEXT,
            IMAGE_FILENAME,

            NUMBER_TRIES,
            CORRECT,
            ACTIVE
        ) FROM QUESTIONS WHERE QUESTION_UUID=?'''
        
        # TODO: check result validity
        # index 0 to get the unique question with the given uuid
        results = executeOnDatabase(databasePath, sql, tuple(str(questionUUID)))[0]

        # shadow the value of the index coresponding to CORRECT above with a boolean value, for some reason it gets connverted to str
        results[6] = bool(results[6] == "True")

        # get the constructor object for the appropriate question subclass object
        questionClass = QUESTION_CONSTRUCTORS[results[0]]

        return questionClass(
            answerVariableName=results[1].lower(),
            variables=Question.getAllVariables(questionUUID),
            correctLeeway=results[2],
            text=results[3],
            imageFilename=results[4],
            numberTries=results[5],
            correct=results[6],
            active=results[7],
            uuid=questionUUID
        )
    
    @staticmethod
    def getAllVariables(databasePath: str, questionUUID: str | UUID) -> list[Variable]:
        """Constructs a list of all the Variables in the database which corespond to the passed questionUUID."""
        sql = '''SELECT VARIABLE_UUID FROM VARIABLES WHERE QUESTION_UUID=?'''
        replacements = tuple(questionUUID)
        results = executeOnDatabase(databasePath, sql, replacements)
        # TODO: check result validity

        variables = []
        for (uuid) in results:
            variables.append(Variable.fromDatabase(databasePath, uuid))

        return variables

    @property
    def answer(self) -> float:
        """Returns the answer to the question given the randomized variable values."""
        # if returns False, didn't get answer
        ans = self.getValue(self.answerVariableName)
        if type(ans) == float:
            return ans
        raise RuntimeError(f"Fetching answer for question {self} failed.")

    def checkSubmission(self, submitted: float) -> bool:
        """Returns whether or not the submitted answer is within the allowed variance (0.1=10%) from the question's calculated answer."""
        firstBound = self.answer*(1-self.correctLeeway)
        secondBound = self.answer*(1+self.correctLeeway)
        # needs two checks, one for if the answer is negative and one if positive
        if self.answer < 0:
            return bool(submitted < firstBound and submitted > secondBound)
        else:
            return bool(submitted > firstBound and submitted < secondBound)
    
    def getValue(self, name: str) -> float | Literal[False]:
        """Returns the value for passed variable name, or False if there is no set variable in the current question with that name."""
        for var in self.variables:
            if var.variableName == name:
                return var.value
        return False

    @property
    def questionFrontendData(self) -> dict:
        """Returns question data that needs to be accessible on website when this question is active."""
        return {
            "questionUUID": self.uuid,
            # the check removes both the solve value and variables that are not defined for this specific question
            "variables": ", ".join(
                [str(var) for var in self.variables if var.variableName != self.answerVariableName]
            ),
            "text": self.text,
            "imageFilename": self.imageFilename
        }
    
    
@dataclass
class KinematicsQuestion(Question):
    """
    Kinematics questions with constant acceleration. Inherits all attributes from Question.\n
    Implements properties for displacement, initial_velocity, final_velocity, time, and acceleration.
    """

    questionType = "KinematicsQuestion"

    def __init__(self, *args, **kwargs) -> None:
        return super().__init__(*args, **kwargs)

    # TODO: restrict variables/add skips in solvers for variables that could /0, or where a sqrt could result in a negative answer but code outputs positive
    # or, add documentation warning about the same

    @property
    def displacement(self) -> float:
        """Fetches or calculates the displacement variable, depending on if it is set or not."""
        # fetch private var value set by config generation, or false if not set
        value = self.getValue("displacement")

        # if fetches value, return it
        if type(value) is float:
            return value
        
        # otherwise use equations
        else:
            # check if each needed var is defined
            v1Defined = self.getValue("initial_velocity")
            v2Defined = self.getValue("final_velocity")
            tDefined = self.getValue("time")

            # assume that enough variables are defined, find the one that isn't
            if not v1Defined:
                v2 = self.getValue("final_velocity")
                t = self.getValue("time")
                a = self.getValue("acceleration")
                
                # d from v2, t, a
                return (v2 * t) - ((0.5 * a)* (t**2))
            
            elif not v2Defined:
                v1 = self.getValue("initial_velocity")
                t = self.getValue("time")
                a = self.getValue("acceleration")

                # d from v1, t, a
                return (v1 * t) + ((0.5 * a) * (t**2))

            elif not tDefined:
                v1 = self.getValue("initial_velocity")
                v2 = self.getValue("final_velocity")
                a = self.getValue("acceleration")

                # d from v1, v2, a
                return ((v2**2) - (v1**2)) / (2 * a)
            
            else: # not aDefined
                v1 = self.getValue("initial_velocity")
                v2 = self.getValue("final_velocity")
                t = self.getValue("time")

                # d from v1, v2, t formula
                return ((v1 + v2) / 2) * t                                       
    
    @property
    def initial_velocity(self) -> float:
        """Fetches or calculates the displacement variable, depending on if it is set or not."""
        # fetch private var value set by config generation, or false if not set
        value = self.getValue("initial_velocity")
        
        # if fetches value, return it
        if type(value) is float:
            return value
        
        # otherwise use equations
        else:
            # check if each var is defined
            dDefined = self.getValue("displacement")
            v2Defined = self.getValue("final_velocity")
            tDefined = self.getValue("time")

            # not needed
            # aDefined = self.getValue("acceleration")

            # assume that enough variables are defined, find the one that isn't
            if not dDefined:
                v2 = self.getValue("final_velocity")
                t = self.getValue("time")
                a = self.getValue("acceleration")
                
                # v1 from v2, t, a
                return v2 - (a*t)
            
            elif not v2Defined:
                d = self.getValue("displacement")
                t = self.getValue("time")
                a = self.getValue("acceleration")

                # v1 from d, t, a
                return (d / t) - (0.5 * a * t)

            elif not tDefined:
                d = self.getValue("displacement")
                v2 = self.getValue("final_velocity")
                a = self.getValue("acceleration")

                # v1 from d, v2, a
                # TODO: make sure sqrt doesn't cause problems
                return sqrt(v2**2 - 2*a*d)

            else: # not aDefined
                d = self.getValue("displacement")
                v2 = self.getValue("final_velocity")
                t = self.getValue("time")

                # v1 from d, v2, t formula
                return ((d*2) / t) - v2
    
    @property
    def final_velocity(self) -> float:
        """Fetches or calculates the displacement variable, depending on if it is set or not."""
        # fetch private var value set by config generation, or false if not set
        value = self.getValue("final_velocity")
        
        # if fetches value, return it
        if type(value) is float:
            return value
        
        # otherwise use equations
        else:
            # check if each var is defined
            dDefined = self.getValue("displacement")
            v1Defined = self.getValue("initial_velocity")
            tDefined = self.getValue("time")

            # not needed
            # aDefined = self.getValue("acceleration")

            # assume that enough variables are defined, find the one that isn't
            if not dDefined:
                v1 = self.getValue("initial_velocity")
                t = self.getValue("time")
                a = self.getValue("acceleration")
                
                # v2 from v1, t, a
                return (a*t) + v1
            
            elif not v1Defined:
                d = self.getValue("displacement")
                t = self.getValue("time")
                a = self.getValue("acceleration")

                # v2 from d, t, a
                return (d / t) + (0.5 * a * t)

            elif not tDefined:
                d = self.getValue("displacement")
                v1 = self.getValue("initial_velocity")
                a = self.getValue("acceleration")

                # v2 from d, v1, a
                # TODO: make sure sqrt doesn't cause problems
                return sqrt(v1**2 + 2*a*d)

            else: # not aDefined
                d = self.getValue("displacement")
                v1 = self.getValue("initial_velocity")
                t = self.getValue("time")

                # v2 from d, v1, t formula
                return ((d*2) / t) - v1
    
    @property
    def time(self) -> float:
        """Fetches or calculates the displacement variable, depending on if it is set or not."""
        # fetch private var value set by config generation, or false if not set
        value = self.getValue("time")
        
        # if fetches value, return it
        if type(value) is float:
            return value
        
        # otherwise use equations
        else:
            # check if each var is defined
            dDefined = self.getValue("displacement")
            v1Defined = self.getValue("initial_velocity")
            v2Defined = self.getValue("final_velocity")

            # not needed
            # aDefined = self.getValue("acceleration")

            # assume that enough variables are defined, find the one that isn't
            # also check that acceleration isn't 0. if so, cannot find time from just acceleration and velocity values, so move on to following ones
            if not dDefined and not all((v1 == v2), (a == 0)):
                v1 = self.getValue("initial_velocity")
                v2 = self.getValue("final_velocity")
                a = self.getValue("acceleration")
                
                # t from v1, v2, a
                return (v2 - v1) / a
            
            elif not v1Defined:
                d = self.getValue("displacement")
                v2 = self.getValue("final_velocity")
                a = self.getValue("acceleration")

                # t from d, v2, a
                # TODO: for now, always returns highest answer even if there are two correct values. figure out how to make this more accurate
                return (v2/a) + (sqrt(v2**2 - 2*a*d)/a) # would be subtraction in the middle to get the other answer

            elif not v2Defined:
                d = self.getValue("displacement")
                v1 = self.getValue("initial_velocity")
                a = self.getValue("acceleration")

                # t from d, v1, a
                return (-v1/a) + (sqrt(v1**2 - 2*a*d)/a)

            else: # not aDefined
                d = self.getValue("displacement")
                v1 = self.getValue("initial_velocity")
                v2 = self.getValue("final_velocity")

                # t from d, v1, v2 formula
                return (d*2)/(v1 + v2)
    
    @property
    def acceleration(self) -> float:
        """Fetches or calculates the displacement variable, depending on if it is set or not."""
        # fetch private var value set by config generation, or false if not set
        value = self.getValue("acceleration")
        
        # if fetches value, return it
        if type(value) is float or type(value) is int:
            return value
        
        # otherwise use equations
        else:
            # check if each var is defined
            dDefined = self.getValue("displacement")
            v1Defined = self.getValue("initial_velocity")
            v2Defined = self.getValue("final_velocity")

            # not needed
            # tDefined = self.getValue("time")

            # assume that enough variables are defined, find the one that isn't
            if not dDefined:
                v1 = self.getValue("initial_velocity")
                v2 = self.getValue("final_velocity")
                t = self.getValue("time")
                
                # a from v1, v2, t
                return 
            
            elif not v1Defined:
                d = self.getValue("displacement")
                v2 = self.getValue("final_velocity")
                t = self.getValue("time")

                # a from d, v2, t
                return # TODO

            elif not v2Defined:
                d = self.getValue("displacement")
                v1 = self.getValue("initial_velocity")
                t = self.getValue("time")

                # a from d, v1, t
                return ((2*d) / (t**2)) - ((2*v1) / (t))

            else: # not tDefined
                d = self.getValue("displacement")
                v1 = self.getValue("initial_velocity")
                v2 = self.getValue("final_velocity")

                # a from d, v1, v2 formula
                return ((2*v2) / (t)) - ((2*d) / (t**2)) 

# this is where new constructors/question types need to be added to function correctly
QUESTION_CONSTRUCTORS = {
    "KinematicsQuestion": KinematicsQuestion
}
