"""
Stuart
February 9, 2024: Implement Question and KinematicsQuestion
February 20, 2024: Fix KinematicsQuestion, implement rest of solving formulas.
"""

from physqgen.generator.config import QuestionConfig
from physqgen.generator.variables import Variable

from dataclasses import InitVar, dataclass, field
from math import sqrt
from typing import Literal
from uuid import UUID, uuid4  # uuid4 doesn't include private information

# TODO: use Variable class instead of weird enum stuff, allows storing the extra data needed. also add the new flexibility to config
@dataclass
class Question:
    """
    Represents a question. Generated using the variableConfig or variableValues parameters. If variableValues is provided, id should also be. str key is variable name in lowercase, and the tuple value is the two bounds of the range for the variable randomization.\n
    Variables that are not set by the config are not created as private attributes, even if they exist in the enum.\n
    To use, create properties with name format f'{enum.value.name.lower()}' for each variable in subclass variables enum, which reference the attributes that are created from the variables enum values. They have format f'_{enum.value.name.lower()}'.\n
    Attributes:\n
        id (str): UUID for the question,\n
        text (str): body text of the question,\n
        img (object): not implemented,\n
        correctRange (float): a float representing the allowed percentage variance from the calculated answer when determining whether an answer is correct,\n
        solveVariable (str): string representation of the variable enum value that will be fetched by the .answer property in lowercase,\n
        variables (Enum): the variables, each with a corresponding generated private attribute containing their generator and defined properties including verification to access them,\n\n
        also has attributes for each value in variables, with format f'_{enum.value.name.lower()}' which have float values
    """ # TODO: fix docstring for refactor to more classes
    solveVariable: str = field(init=False)
    variables: list[Variable] = field(init=False)
    questionType: str = field(init=False)
    correctRange: float = field(init=False)

    # specified per-question
    config: InitVar[QuestionConfig | None] = None
    storedData: InitVar[dict | None] = None
    
    # img: object
    text: str = field(init=False)
    correct: bool = field(init=False)
    numberTries: int = field(init=False)

    id: UUID = field(init=False, default_factory=uuid4)

    def __post_init__(self, config: QuestionConfig | None, storedData: dict | None) -> None:
        """Initializes Question."""
        # TODO: make sure storing data works well: will need diff format, maybe separate table for variable values
        if type(config) == QuestionConfig:
            self.text = config.text
            self.correctRange = config.correctRange
            self.solveVariable = config.solveVariableType
            self.questionType = config.questionType
            self.correct = False
            self.numberTries = 0

            self.variables = []
            for varConfig in config.variableConfigs:
                self.variables.append(Variable(varConfig.range, varConfig.variableType, varConfig.units, varConfig.displayName))

        elif type(storedData) == dict:
            # TODO: extract to classmethod
            # is False, use storedData
            # overwrites generated data
            self.text = storedData["text"]
            self.correctRange = storedData["text"]
            self.id = storedData["id"]
            self.correct = storedData["correct"]
            self.numberTries = storedData["numberTries"]

            self.variables: list[Variable] = []
            # data may need to reference a separate table of variable data
            for varData in storedData["variableData"]:
                self.variables.append(Variable.fromStored(varData["name"], varData["value"], varData["units"], varData["displayName"]))
        else:
            raise TypeError(f"Both variableConfig and variableValues were not dicts holding required data. One of them must be defined in order to construction the question.")

    @property
    def answer(self) -> float:
        """Returns the answer to the question given the randomized variable values."""
        # TODO: make sure solves correctly
        # if returns False, didn't get answer
        ans = self.getValue(self.solveVariable)
        if type(ans) == float:
            return ans
        raise RuntimeError(f"Fetching answer for question {self} failed.")

    def check_answer(self, submitted) -> bool:
        """Returns True if the submitted answer is within the correctRange variance from the question's calculated answer."""
        return (submitted > (self.answer * (1 - self.correctRange))) and (submitted < (self.answer * (1 + self.correctRange)))
    
    def getValue(self, name: str) -> float | Literal[False]:
        """Returns the value for passed variable name, or False if there is no set variable in the current question with that name."""
        for var in self.variables:
            if var.name == name:
                return var.value
        return False

    @property
    def websiteDisplayData(self) -> dict:
        """Returns question data that needs to be accessible on website, that isn't stored directly."""
        data = {}
        # the check removes both the solve value and the unrelated value
        # TODO: figure out how to assemble, maybe try for multiple lines
        data["values"] = ", ".join(
            # TODO: consult about number of decimals, maybe make it configurable
            [f"{var.displayName} = {var.value:.3f}" for var in self.variables if var.name != self.solveVariable]
        )
        data["text"] = self.text
        data["correctRange"] = self.correctRange
        return data

    @property
    def varNames(self) -> list[str]:
        varNames = []
        for var in self.variables:
            varNames.append(var.name)
        return varNames

@dataclass
class KinematicsQuestion(Question):
    """Kinematics questions, with constant acceleration. Inherits attributes from Question. Sets variables attribute to Enum("KinematicsVariables", "DISPLACEMENT, INITIAL_VELOCITY, FINAL_VELOCITY, TIME, ACCELERATION")."""

    # variables = Enum("KinematicsVariables", "DISPLACEMENT, INITIAL_VELOCITY, FINAL_VELOCITY, TIME, ACCELERATION")
    POSSIBLE_VARIABLES = ("DISPLACEMENT", "INITIAL_VELOCITY", "FINAL_VELOCITY", "TIME", "ACCELERATION")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs )
        value = self.solve()
        self.variables.append(Variable.fromStored(name=self.solveVariable, value=value, units="", displayName="", varID=uuid4()))
        return

    # TODO: restrict variables that could /0 in solvers, or where a sqrt could result in a negative answer but code outputs positive, etc.
    # TODO: fix value of 0.0 for any defined variable except acceleration breaking the how-to-solve check.
    # TODO: re-add verification, where necessary.

    def solve(self) -> float:
        """Solve for the value of the solveVariable, based on the given variables."""
        
        # fetch the property that solves for the wanted value
        return getattr(self, self.solveVariable)

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
    
    # @staticmethod
    # def displacement_validate(value: float) -> bool:
    #     """Uses appropriate validation functions to ensure displacement is valid. Currently allowed any float value."""
    #     if type(value) is float or type(value) is int:
    #         return True
    #     else:
    #         return False

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
    
    # @staticmethod
    # def initial_velocity_validate(value) -> bool:
    #     """Uses appropriate validation functions to ensure initial velocity is valid. Currently allowed any float value."""
    #     # TODO: might change to not allow being equal to final velocity, which would only happen if acceleration is 0
    #     if type(value) is float or type(value) is int:
    #         return True
    #     else:
    #         return False

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
    
    # @staticmethod
    # def final_velocity_validate(value) -> bool:
    #     """Uses appropriate validation functions to ensure final velocity is valid. Currently allowed any float value."""
    #     # TODO: might change to not allow being equal to initial velocity, which would only happen if acceleration is 0
    #     if type(value) is float or type(value) is int:
    #         return True
    #     else:
    #         return False

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
            if not dDefined:
                v1 = self.getValue("initial_velocity")
                v2 = self.getValue("final_velocity")
                a = self.getValue("acceleration")
                
                # t from v1, v2, a
                # TODO: fix v1=v2 situation, gives 0/0
                return (v2 - v1) / a
            
            elif not v1Defined:
                d = self.getValue("displacement")
                v2 = self.getValue("final_velocity")
                a = self.getValue("acceleration")

                # t from d, v2, a
                # TODO: for now, always return highest answer even if there are two correct values
                return (v2/a) + (sqrt(v2**2 - 2*a*d)/a) # negative in between for other answer

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
    
    # def time_validate(self, value) -> bool:
    #     """Uses appropriate validation functions to ensure time is valid. Currently allowed any positive non-zero float value."""
    #     if self.validatePositiveNonZeroAttribute(value):
    #         return True
    #     else:
    #         return False

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

    # def acceleration_validate(self, value) -> bool:
    #     """Uses appropriate validation functions to ensure acceleration is valid. Currently allowed any positive float value."""
    #     # TODO: might change to not allow acceleration of 0
    #     if self.validatePositiveAttribute(value):
    #         return True
    #     else:
    #         return False
