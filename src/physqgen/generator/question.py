from dataclasses import InitVar, dataclass, field
from math import sqrt
from sqlite3 import connect
from typing import Literal
from uuid import UUID, uuid4  # uuid4 doesn't include private information

from physqgen import generator
from physqgen.generator.config import QuestionConfig
from physqgen.generator.variables import Variable


@dataclass
class Question:
    """
    Base class for all question implementations. Can be generated from a configution, which creates a question with random Variables, or from stored data.\n
    Subclasses should implement snake case properties for each POSSIBLE_VARIABLE, which pull the value if it is set or solve for it if not. See KinematicsQuestion for an example.\n
    Attributes:\n
        solveVariable (str): value of the name property of the Variable to treat as the answer,\n
        variables (list[Variable]): relevant variables for the question, may not include Variables for every name in POSSIBLE_VARIABLES if they are not relevant,\n
        questionType (str): class name of the question subclass, for ease of access,\n
        correctRange (float): allowed factor variance from the calculated answer when determining whether a submission is correct,\n
        imageName (str): filename of the image to display,\n
        text (str): displayed text,\n
        correct (bool): whether the question has been completed,\n
        numberTries (int): number of submissions checked,\n
        id (UUID): question uuid,\n
        POSSIBLE_VARIABLES (tuple): class variable containing the uppercase names of every possible variable for the question subclass. Needs to be overriden in inheriting classes.
    """
    solveVariable: str
    variables: list[Variable]
    questionType: str
    correctRange: float

    imageName: str
    text: str
    correct: bool
    numberTries: int

    id: UUID = field(default_factory=uuid4)

    # needs to be overriden in inheriting classes
    POSSIBLE_VARIABLES = tuple()

    def __post_init__(self) -> None:
        # use fromStored() to create a Variable with a predefined value, this is the answer
        self.variables.append(Variable.fromStored(name=self.solveVariable, value=getattr(self, self.solveVariable), varID=uuid4()))
        return

    @classmethod
    def fromStoredData(cls, questionData: dict):
        """Creates an instance of cls from the passed data."""
        storedVars: list[Variable] = []
        for varData in questionData["variableData"]:
            storedVars.append(
                Variable.fromStored(
                    name=varData["NAME"],
                    value=varData["VALUE"],
                    units=varData["UNITS"],
                    displayName=varData["DISPLAY_NAME"],
                    varID=UUID(varData["VARIABLE_UUID"]),
                    decimalPlaces=varData["DECIMAL_PLACES"]
                )
            )
        
        return cls(
            solveVariable=questionData["SOLVE_VARIABLE"],
            variables=storedVars,
            questionType=questionData["questionType"],
            correctRange=questionData["CORRECT_RANGE"],
            imageName=questionData["IMAGE_PATH"],
            text=questionData["TEXT"],
            correct=questionData["CORRECT"],
            numberTries=questionData["NUMBER_TRIES"],
            id=UUID(questionData["QUESTION_UUID"])
        )
    
    @classmethod
    def fromConfiguration(cls, questionConfig: QuestionConfig):
        """Creates an randomized instance of cls from the passed configuration."""
        randomVars: list[Variable] = []
        for varConfig in questionConfig.variableConfigs:
            randomVars.append(varConfig.getRandomVariable())

        return cls(
            solveVariable=questionConfig.solveVariable,
            variables=randomVars,
            questionType=questionConfig.questionType,
            correctRange=questionConfig.correctRange,
            imageName=questionConfig.imageName,
            text=questionConfig.text,
            correct=False,
            numberTries=0
        )

    @classmethod
    def fromUUID(cls, databasePath: str, qType: str, questionID: str):
        """Creates an instance of cls from the question data in the database for the given question UUID."""
        return cls.fromStoredData(Question.fetchQuestionData(databasePath, qType, questionID))

    @property
    def answer(self) -> float:
        """Returns the answer to the question given the randomized variable values."""
        # TODO: make sure solves correctly
        # if returns False, didn't get answer
        ans = self.getValue(self.solveVariable)
        if type(ans) == float:
            return ans
        raise RuntimeError(f"Fetching answer for question {self} failed.")

    def check_answer(self, submitted: float) -> bool:
        """Returns whether or not the submitted answer is within the correctRange factor variance (0.1=10%) from the question's calculated answer."""
        firstBound = self.answer*(1-self.correctRange)
        secondBound = self.answer*(1+self.correctRange)
        # needs two checks, one for if the answer is negative and one if positive
        if self.answer < 0:
            return bool(submitted < firstBound and submitted > secondBound)
        else:
            return bool(submitted > firstBound and submitted < secondBound)
    
    def getValue(self, name: str, id: bool = False) -> float | Literal[False]:
        """
        Returns the value for passed variable name, or False if there is no set variable in the current question with that name.\n
        If id is True, fetches the variable's UUID instead.
        """
        for var in self.variables:
            if var.name == name:
                if id:
                    return var.varID
                else:
                    return var.value
        return False

    @property
    def websiteDisplayData(self) -> dict:
        """Returns question data that needs to be accessible on website, that isn't stored directly. This allows it to be stored in Flask session."""
        data = {}
        # the check removes both the solve value and variables that are not defined for this specific question
        data["values"] = ", ".join(
            [str(var) for var in self.variables if var.name != self.solveVariable]
        )
        data["text"] = self.text
        data["correctRange"] = self.correctRange
        data["numberTries"] = self.numberTries
        data["imageName"] = self.imageName
        return data

    @property
    def varNames(self) -> list[str]:
        """Returns a list of the names of the variables that are actually defined for the question."""
        varNames = []
        for var in self.variables:
            varNames.append(var.name)
        return varNames

    @staticmethod
    def fetchQuestionData(databasePath: str, qType: str, uuid: str) -> dict:
        """
        Returns a dictionary of stored data to be used to construct a question subclass object.
        """
        with connect(databasePath) as conn:
            cursor = conn.cursor()

            # TODO: reformat databases to protect against sql injection, have single Question table instead of multiple
            sql = f'''SELECT * FROM {qType.upper()} WHERE QUESTION_UUID=?'''
            cursor.execute(sql, [str(uuid)])
            questionData = cursor.fetchone()
            
            # 10+ => variable UUIDs, in order of database, which is order in the class's POSSIBLE_VARIABLES tuple class variable
            namedData = {
                "QUESTION_UUID": questionData[0],
                "FIRST_NAME": questionData[1],
                "LAST_NAME": questionData[2],
                "EMAIL": questionData[3],
                "NUMBER_TRIES": questionData[4],
                # for some reason this contains the string "False" or "True", not a bool, so it has to be converted
                "CORRECT": bool(questionData[5] == "True"),
                "SOLVE_VARIABLE": questionData[6],
                "TEXT": questionData[7],
                "IMAGE_PATH": questionData[8],
                "CORRECT_RANGE": questionData[9],
                # add variable extracted dicts
                "variableData": [],
                #add questionType
                "questionType": qType
            }

            # get the constructor object for the appropriate question subclass object
            questionClass = getattr(generator, qType)

            for index in range(len(questionClass.POSSIBLE_VARIABLES)):
                skip = False # whether fetching uuid returned False, which means that variable did not have a set value and should be skipped for construction
                # fetch UUIDs, using index + number of previous indexes to start when the var columns start
                varID = questionData[index + 10]
                # check for None, if var is not defined for this question
                if varID is None:
                    skip = True

                if not skip:
                    # fetch variable data given uuid
                    # TODO: sql injection isn't an issue, but may as well fix it
                    varFetchSQL = f'''SELECT * FROM VARIABLES WHERE VARIABLE_UUID="{varID}"'''

                    cursor.execute(varFetchSQL)
                    variableData = cursor.fetchone()

                    namedData["variableData"].append(
                        {
                            "VARIABLE_UUID": variableData[0],
                            "NAME": variableData[1],
                            "VALUE": variableData[2],
                            "UNITS": variableData[3],
                            "DISPLAY_NAME": variableData[4],
                            "DECIMAL_PLACES": variableData[5]
                        }
                    )

        # just in case
        conn.close()
        return namedData

@dataclass
class KinematicsQuestion(Question):
    """
    Kinematics questions with constant acceleration. Inherits all attributes from Question.\n
    Implements properties for displacement, initial_velocity, final_velocity, time, and acceleration.\n
    Overrides POSSIBLE_VARIABLES with uppercase variants of the above properties.
    """

    POSSIBLE_VARIABLES = ("DISPLACEMENT", "INITIAL_VELOCITY", "FINAL_VELOCITY", "TIME", "ACCELERATION")

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
