from dataclasses import dataclass, field
from math import sqrt
from typing import Literal
from uuid import UUID, uuid4  # uuid4 doesn't include private information

from physqgen.database import executeOnDatabase
from physqgen.generator.variable import Variable


@dataclass(slots=True)
class Question:
    """
    Base class for all question types. Can be generated from a configuration, which creates a question with random Variables, or from stored data.\n
    Subclasses should implement snake case properties for each variable they involve, which pull the value if it is set or solve for it if not. See KinematicsQuestion for an example.\n
    Subclasses need to include valid variables in docs.\n
    Subclasses can also have verification, handled separately, see VERIFICATION_METHODS in variables.py.\n
    Attributes:\n
        answerVariableName (str): value of the name property of the Variable to treat as the answer,\n
        variables (list[Variable]): relevant variables for the question, may not include Variables for every name in POSSIBLE_VARIABLES if they are not relevant,\n
        correctLeeway (float): allowed factor variance from the calculated answer when determining whether a submission is correct,\n
        text (str): displayed text,\n
        imageFilename (str): filename of the image to display,\n
        numberTries (int): number of submissions checked,\n
        correct (bool): whether the question has been completed,\n
        active (bool): used in conjunction with correct for completion tracking,\n
        uuid (UUID): unique question uuid,\n
        questionType (str): identifier for question subclass, used as a key in the QUESTION_CONSTRUCTORS dict, needs to be overriden in subclasses and added to said dict
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
    questionType = ""

    @classmethod
    def fromConfig(_, questionConfig):
        """Creates an randomized instance of cls from the passed questionConfig (QuestionConfig)."""
        variables: list[Variable] = []
        for varConfig in questionConfig.variableConfigs:
            variables.append(Variable.fromConfig(varConfig, questionConfig.questionType))

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
                # this is where all the properties added to subclasses are actually used to get answer
                value=getattr(question, questionConfig.answerVariableName.lower())
            )
        )

        return question
    
    @classmethod
    def fromDatabase(_, databasePath: str, questionUUID: str | UUID):
        """
        Returns the appropriate Question subclass for data in the database coresponding to the given uuid.\n
        Does not use the class it is called on directly. This is still marked as a classmethod because it fulfills the purpose of one, constructing an instance of the class, except it will search for the appropriate subclass instead.
        """
        sql = '''
            SELECT
                QUESTION_TYPE,
                ANSWER_VARIABLE_NAME,
                CORRECT_LEEWAY,
                TEXT,
                IMAGE_FILENAME,

                NUMBER_TRIES,
                CORRECT,
                ACTIVE
            FROM QUESTIONS WHERE QUESTION_UUID=?
        '''
        replacements = (str(questionUUID),)
        
        # index 0 to get the unique question with the given uuid
        # will error if the database has been cleared since the session was created
        # let it error to prevent other issues
        # should never error, given other things should error first, so don't include it in docstring
        results = executeOnDatabase(databasePath, sql, replacements)[0]

        # get the constructor object for the appropriate question subclass object
        questionClass = QUESTION_CONSTRUCTORS[results[0]]

        return questionClass(
            answerVariableName=results[1].lower(),
            variables=Question.getAllVariables(databasePath, questionUUID),
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
        replacements = (questionUUID,)
        results = executeOnDatabase(databasePath, sql, replacements)
        if len(results) == 0:
            # could happen if the database has been cleared since creation
            # should error on other things first, but check just in case
            # because this should never run, don't include it in docstring
            raise RuntimeError("Session has been cleared. Cannot load data.")

        variables = []
        for uuid in results:
            # unpack the row tuples, each have a single element
            uuid = uuid[0]
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
            # whether to show incorrect submission prompt
            "numberTries": self.numberTries,
            "imageFilename": self.imageFilename
        }
    
    def addToDatabase(self, databasePath: str, sessionUUID: str | UUID) -> None:
        """Adds this Questions data to the databse, including contained Variables."""
        sql = '''
            INSERT INTO QUESTIONS (
                QUESTION_UUID,
                SESSION_UUID,
                QUESTION_TYPE,
                NUMBER_TRIES,
                CORRECT,
                ACTIVE,
                TEXT,
                ANSWER_VARIABLE_NAME,
                IMAGE_FILENAME,
                CORRECT_LEEWAY
            ) VALUES (
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            )
        '''
        replacements = (
            str(self.uuid),
            str(sessionUUID),
            self.questionType,
            self.numberTries,
            self.correct,
            self.active,
            self.text,
            self.answerVariableName,
            self.imageFilename,
            self.correctLeeway
        )
        executeOnDatabase(databasePath, sql, replacements)

        for variable in self.variables:
            variable.addToDatabase(databasePath, self.uuid)
        
        return
        
    def updateDatabase(self, databasePath: str) -> None:
        """Updates Question data stored in database."""
        sql = '''
            UPDATE QUESTIONS
            SET
                NUMBER_TRIES=?,
                CORRECT=?,
                ACTIVE=?
            WHERE
                QUESTION_UUID=?
        '''
        replacements = (
            self.numberTries,
            self.correct,
            self.active,
            self.uuid
        )
        executeOnDatabase(databasePath, sql, replacements)
        
        # nothing in Variables changes over the course of a sesssion, don't need to update
        return


@dataclass(slots=True)
class KinematicsQuestion(Question):
    """
    Kinematics questions with constant acceleration. Inherits all attributes from Question.\n
    Implements properties for displacement, initial_velocity, final_velocity, time, and acceleration.
    """

    questionType = "KinematicsQuestion"

    # TODO: add source to readme
    # derivations verified with: https://calculator-online.net/kinematics-calculator/

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
            # will be False if not defined
            v1 = self.getValue("initial_velocity")
            v2 = self.getValue("final_velocity")
            t = self.getValue("time")
            a = self.getValue("acceleration")

            # assume that enough variables are defined, find the one that isn't
            if v1 is False:
                # d from v2, t, a
                return (v2 * t) - ((0.5 * a) * (t**2))
            
            elif v2 is False:
                # d from v1, t, a
                return (v1 * t) + ((0.5 * a) * (t**2))

            elif t is False:
                # d from v1, v2, a
                return ((v2**2) - (v1**2)) / (2 * a)
            
            else: # a is False
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
            # will be False if not defined
            d = self.getValue("displacement")
            v2 = self.getValue("final_velocity")
            t = self.getValue("time")
            a = self.getValue("acceleration")

            # assume that enough variables are defined, find the one that isn't
            if d is False:
                # v1 from v2, t, a
                return v2 - (a*t)
            
            elif v2 is False:
                # v1 from d, t, a
                return (d / t) - ((a * t) / 2)

            elif t is False:
                # v1 from d, v2, a
                return sqrt(v2**2 - 2*a*d)

            else: # a is False 
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
            # will be False if not defined
            d = self.getValue("displacement")
            v1 = self.getValue("initial_velocity")
            t = self.getValue("time")
            a = self.getValue("acceleration")

            # assume that enough variables are defined, find the one that isn't
            if d is False:
                # v2 from v1, t, a
                return (a*t) + v1
            
            elif v1 is False:
                # v2 from d, t, a
                return (d / t) + (0.5 * a * t)

            elif t is False:
                # v2 from d, v1, a
                return sqrt(v1**2 + 2*a*d)

            else: # a is False
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
            # time relies on the other solvers instead of its own, is fine so long as the others implement all formulas

            # check if each var is defined
            # will be set to False if not yet defined
            v1 = self.getValue("initial_velocity")
            v2 = self.getValue("final_velocity")
            a = self.getValue("acceleration")

            # identity so float 0.0 isn't interpreted as False
            if v1 is False:
                v1 = self.initial_velocity
            elif v2 is False:
                v2 = self.final_velocity
            elif a is False:
                a = self.acceleration
           
            # t from v1, v2, a, simpler formula to deal with
            return ((v2 - v1) / a)
    
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
            # will be False if not defined
            d = self.getValue("displacement")
            v1 = self.getValue("initial_velocity")
            v2 = self.getValue("final_velocity")
            t = self.getValue("time")

            # assume that enough variables are defined, find the one that isn't
            if d is False:
                # a from v1, v2, t
                return ((v2 - v1)/t)
            
            elif v1 is False:
                # a from d, v2, t
                return ((2 * v2) / t) - ((2 * d) / (t**2))

            elif v2 is False:
                # a from d, v1, t
                return ((2*d) / (t**2)) - ((2*v1) / t)

            else: # t is False
                # a from d, v1, v2 formula
                return ((v2**2 - v1**2) / (2 * d))

# this is where new constructors/question types need to be added to function correctly
QUESTION_CONSTRUCTORS = {
    "KinematicsQuestion": KinematicsQuestion
}
