"""
Question Datastructures
ICS4U
Stuart, Isabelle, Amelia
Represent different types of questions.
History:
February TODO, 2024: Implement Question and KinematicsQuestion
"""

from random import random
from dataclasses import dataclass, field, InitVar
from uuid import UUID, uuid4 # uuid4 doesn't include private information
from enum import Enum
from math import sqrt
from typing import Literal

@dataclass
class Question:
    """
    Represents a question. Generated using the variableConfig parameter in init. str key is variable name in lowercase, and the tuple value is the two bounds of the range for the variable randomization.\n
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
    """
    # specified per-question
    variableConfig: InitVar[dict[str, tuple[float, float]]]
    solveVariable: str
    
    # override with values
    # img: object
    text: str = ""
    variables: Enum = field(default_factory=Enum)

    # should be left default
    # CORRECT_RANGE default was agreed upon with client at 10%
    CORRECT_RANGE: float = 0.1

    # always leave default
    id: UUID = field(default_factory=uuid4, init=False)

    def __post_init__(self, variableConfig: dict[str, tuple[float, float]]) -> None:
        """Randomizes variables values."""

        # randomize variables
        for variable, range in variableConfig.items():

            # replace str representation with enum member representation
            variable: Enum = self.variables[variable.upper()]

            # test if bounds of range are valid for the variable. assume that if both are valid, anything in between is
            # error if invallid
            # TODO: log instead of erroring

            # get variables validation function
            validationFunc = getattr(self, f"{variable.name.lower()}_validate")
            for bound in range:
                # test each bound
                if not validationFunc(bound):
                    raise ValueError(f"Bound {bound} for question {self} taken from config is invalid. Must pass validation function {validationFunc}.")

            # multiple the difference between the two ends of the range by a float between 0.0 and 1.0, and add it to the base.
            # randomizes the variable's value
            # will work no matter order of range values, smaller first or larger first
            randomValue = range[0] + random() * (range[1] - range[0])

            # create attribute in dict that has the randomizes value and an attribute name coresponding to the enum value name, in lowercase
            # TODO: check if there is better way to add attributes dynamically
            self.__dict__["_" + variable.name.lower()] = randomValue
            # define properties for each variablei subclasses, which use this defined value
        
    def __str__(self) -> str:
        """Returns a string representation of the question text"""
        # TODO: fix for enum
        return f"{self.text}\n{str(self.variables)}"
    
    @property
    def answer(self) -> float:
        """Returns the answer to the question given the randomized variable values."""
        # TODO: currently returns property instead of property value
        return getattr(self, self.solveVariable)

    def check_answer(self, submitted) -> bool:
        """Returns True if the submitted answer is within the CORRECT_RANGE variance from the question's calculated answer."""
        return (submitted > (self.answer * (1 - self.CORRECT_RANGE))) and (submitted < (self.answer * (1 + self.CORRECT_RANGE)))
    
    @staticmethod
    def enumToAttribute(enumAttribute: Enum, private: bool = False) -> str:
        """
        Has two uses.\n
        If private is True, formats the name of the passed attribute so it matches with the auto-created attributes for variables passed through the config.\n
        Otherwise, returns the name of the property for the passed enum.\n
        Properties are guarranteed to be defined for each variable for the Question subclass, auto-created private attributes are not.
        """
        if private:
            return f"_{enumAttribute.name.lower()}"
        else:
            return enumAttribute.name.lower()
    
    @staticmethod
    def validatePositiveNonZeroAttribute(value: float) -> bool:
        """Returns True if value is a positive non 0.0 float, otherwise returns False."""
        if type(value) is float and value > 0.0:
            return True
        else:
            return False
    
    @staticmethod
    def validatePositiveAttribute(value: float) -> bool:
        """Returns True if value is a float that is greater than or equal to 0.0. Otherwise returns False."""
        if type(value) is float and value >= 0.0:
            return True
        else:
            return False

    def variableDefined(self, lowercaseName: str) -> bool:
        """Return True if the variable name has a defined private attribute. Otherwise return False."""
        try:
            # test if exists, will error if doesn't
            getattr(self, self.enumToAttribute(self.variables[lowercaseName.upper()], True))
            return True
        except AttributeError:
            return False
    
    def getVariableValue(self, variableName: str) -> float | Literal[False]:
        """Fetches the value for the passed variable name, or False if it is not set."""
        return getattr(self, variableName, False)

@dataclass
class KinematicsQuestion(Question):
    """Kinematics questions, with constant acceleration. Inherits attributes from Question. Sets variables attribute to Enum("KinematicsVariables", "DISPLACEMENT, INITIAL_VELOCITY, FINAL_VELOCITY, TIME, ACCELERATION")."""

    # set enum default
    # can create enum entirely using the call, but that would sacrifice some clarity
    variables: Enum = Enum("KinematicsVariables", "DISPLACEMENT, INITIAL_VELOCITY, FINAL_VELOCITY, TIME, ACCELERATION")

    # TODO: writing properties for each value
        # transfer formulas
    # TODO: variable verification (not in setter, use staticmethod, call in properties)
        # restrict variables that could /0 in solvers, or where a sqrt could result in a negative answer but code outputs positive, etc.

    # TODO: maybe validate stuff differently depending on solve variable

    # supply getattrs with default False, check if returns a False value to see if the value was not set by config

    @property
    def displacement(self) -> float:
        """Fetches or calculates the displacement variable, depending on if it is set or not."""
        value = self.getVariableValue(self.enumToAttribute(self.variables.DISPLACEMENT))

        # check if returned False, currently also adding additional check so that value of 0.0 still goes through
        # maybe remove extra step for variables that cannot be 0.0
        if type(value) is bool and not value:
            # check existance of other variables, use the formula that has all necessary values
            if self.variableDefined("initial_velocity"):
                if self.variableDefined("final_velocity"):
                    if self.variableDefined("time"):
                        # d from v1, v2, t formula
                        return (
                            (
                                (
                                    self.getVariableValue(self.variables.INITIAL_VELOCITY) 
                                    + self.getVariableValue(self.variables.FINAL_VELOCITY)
                                ) 
                            / 2) 
                        * self.getVariableValue(self.variables.TIME)
                        )
                    elif self.variableDefined("acceleration"):
                        # d from v1, v2, a
                        return (
                            (
                                (
                                    self.getVariableValue(self.variables.FINAL_VELOCITY)**2
                                ) - (
                                    self.getVariableValue(self.variables.INITIAL_VELOCITY)**2
                                )
                            ) 
                            / (
                                2 
                                * self.getVariableValue(self.variables.ACCELERATION)
                            )
                        )
                elif self.variableDefined("time"):
                    if self.variableDefined("acceleration"):
                        # d from v1, t, a
                        return (
                            (
                                self.getVariableValue(self.enumToAttribute(self.variables.INITIAL_VELOCITY))
                                * self.getVariableValue(self.enumToAttribute(self.variables.TIME))
                            ) 
                            + (
                                0.5 
                                * self.getVariableValue(self.enumToAttribute(self.variables.ACCELERATION)) 
                                * (
                                    self.getVariableValue(self.enumToAttribute(self.variables.TIME))**2
                                )
                            )
                        )
            elif self.variableDefined("final_velocity"):
                if self.variableDefined("time"):
                    if self.variableDefined("acceleration"):
                        # d from v2, t, a
                        return (
                            (
                            self.getVariableValue(self.enumToAttribute(self.variables.FINAL_VELOCITY)) 
                            * self.getVariableValue(self.enumToAttribute(self.variables.TIME))
                            ) - (
                                0.5 
                                * self.getVariableValue(self.enumToAttribute(self.variables.ACCELERATION))
                                * (
                                    self.getVariableValue(self.enumToAttribute(self.variables.TIME))**2
                                )
                            )
                        )

        else:
            return value
    
    @staticmethod
    def displacement_validate(value: float) -> bool:
        """Uses appropriate validation functions to ensure displacement is valid. Currently allowed any float value."""
        if type(value) is float:
            return True
        else:
            return False

    @property
    def initial_velocity(self) -> float:
        """Fetches or calculates the displacement variable, depending on if it is set or not."""
        value = getattr(self, self.enumToAttribute(self.variables.INITIAL_VELOCITY, True), False)
        # check if isn't set
        if not value:
            # check existance of other variables, use the formula that has all necessary values
            pass # TODO

        else:
            return value
    
    @staticmethod
    def initial_velocity_validate(value: float) -> bool:
        """Uses appropriate validation functions to ensure initial velocity is valid. Currently allowed any float value."""
        # TODO: might change to not allow being equal to final velocity, which would only happen if acceleration is 0
        if type(value) is float:
            return True
        else:
            return False

    @property
    def final_velocity(self) -> float:
        """Fetches or calculates the displacement variable, depending on if it is set or not."""
        value = getattr(self, self.enumToAttribute(self.variables.FINAL_VELOCITY, True), False)
        # check if isn't set
        if not value:
            # check existance of other variables, use the formula that has all necessary values
            pass # TODO

        else:
            return value
    
    @staticmethod
    def final_velocity_validate(value: float) -> bool:
        """Uses appropriate validation functions to ensure final velocity is valid. Currently allowed any float value."""
        # TODO: might change to not allow being equal to initial velocity, which would only happen if acceleration is 0
        if type(value) is float:
            return True
        else:
            return False

    @property
    def time(self) -> float:
        """Fetches or calculates the displacement variable, depending on if it is set or not."""
        value = getattr(self, self.enumToAttribute(self.variables.TIME, True), False)
        # check if isn't set
        if not value:
            # check existance of other variables, use the formula that has all necessary values
            pass # TODO

        else:
            return value
    
    def time_validate(self, value: float) -> bool:
        """Uses appropriate validation functions to ensure time is valid. Currently allowed any positive non-zero float value."""
        if self.validatePositiveNonZeroAttribute(value):
            return True
        else:
            return False

    @property
    def acceleration(self) -> float:
        """Fetches or calculates the displacement variable, depending on if it is set or not."""
        value = getattr(self, self.enumToAttribute(self.variables.ACCELERATION, True), False)
        # check if isn't set
        if not value:
            # check existance of other variables, use the formula that has all necessary values
            pass # TODO

        else:
            return value

    def acceleration_validate(self, value: float) -> bool:
        """Uses appropriate validation functions to ensure acceleration is valid. Currently allowed any positive float value."""
        # TODO: might change to not allow acceleration of 0
        if self.validatePositiveAttribute(value):
            return True
        else:
            return False

    # def _checkNeededSolveVars(self, neededSolveVars: list[str]) -> int:
    #     """Checks if the vars in neededSolveVars all have values other than None. If any have None, will return 0. Otherwise, returns 1."""
    #     for neededSolveVar in neededSolveVars:
    #         if self.variables[neededSolveVar] is None:
    #             return 0
        
    #     return 1


    # def _velocity1Solve1(self) -> float:
    #     """Sets the velocity_1 variable v1 based on d, t, and a. If required variables not set, returns 0. If succeeds, returns 1."""
        
    #     # check for required variables
    #     if self._checkNeededSolveVars(["d", "t", "a"]) == 0:
    #         return 0

    #     # solve if has required variables
    #     self.variables["v1"] = (self.variables["d"] / self.variables["t"]) - (0.5 * self.variables["a"] * self.variables["t"])
    #     return 1
    
    # def _velocity1Solve2(self) -> float:
    #     """Sets the velocity_1 variable v1 based on d, v2, and t. If required variables not set, returns 0. If succeeds, returns 1."""
        
    #     # check for required variables
    #     if self._checkNeededSolveVars(["d", "v2", "t"]) == 0:
    #         return 0

    #     # solve if has required variables
    #     self.variables["v1"] = ((self.variables["d"] / self.variables["t"]) * 2) - (self.variables["v2"])
    #     return 1

    # def _velocity1Solve3(self) -> float:
    #     """Sets the velocity_1 variable v1 based on v2, t, and a. If required variables not set, returns 0. If succeeds, returns 1."""
        
    #     # check for required variables
    #     if self._checkNeededSolveVars(["v2", "t", "a"]) == 0:
    #         return 0

    #     # solve if has required variables
    #     self.variables["v1"] = self.variables["v2"] - ((self.variables["a"] * self.variables["t"]))
    #     return 1

    # def _velocity1Solve4(self) -> float:
    #     """Sets the velocity_1 variable v1 based on v2, d, and a. If required variables not set, returns 0. If succeeds, returns 1."""
        
    #     # check for required variables
    #     if self._checkNeededSolveVars(["v1", "d", "a"]) == 0:
    #         return 0

    #     # solve if has required variables
    #     self.variables["v1"] = sqrt((self.variables["v2"]**2) - (2 * self.variables["a"] * self.variables["d"]))
    #     return 1

    # def _velocity2Solve1(self) -> float:
    #     """Sets the velocity_2 variable v2 based on d, t, and a. If required variables not set, returns 0. If succeeds, returns 1."""
        
    #     # check for required variables
    #     if self._checkNeededSolveVars(["d", "t", "a"]) == 0:
    #         return 0

    #     # solve if has required variables
    #     self.variables["v2"] = (self.variables["d"] / self.variables["t"]) + (0.5 * self.variables["a"] * self.variables["t"])
    #     return 1

    # def _velocity2Solve2(self) -> float:
    #     """Sets the velocity_2 variable v2 based on v1, d, and t. If required variables not set, returns 0. If succeeds, returns 1."""
        
    #     # check for required variables
    #     if self._checkNeededSolveVars(["v1", "d", "t"]) == 0:
    #         return 0

    #     # solve if has required variables
    #     self.variables["v2"] = ((self.variables["d"] / self.variables["t"]) * 2) - self.variables["v1"]
    #     return 1

    # def _velocity2Solve3(self) -> float:
    #     """Sets the velocity_2 variable v2 based on v1, a, and t. If required variables not set, returns 0. If succeeds, returns 1."""
        
    #     # check for required variables
    #     if self._checkNeededSolveVars(["v1", "a", "t"]) == 0:
    #         return 0

    #     # solve if has required variables
    #     self.variables["v2"] = (self.variables["a"] * self.variables["t"]) + self.variables["v1"]
    #     return 1

    # def _velocity2Solve4(self) -> float:
    #     """Sets the velocity_2 variable v2 based on v1, a, and d. If required variables not set, returns 0. If succeeds, returns 1."""
        
    #     # check for required variables
    #     if self._checkNeededSolveVars(["v1", "a", "d"]) == 0:
    #         return 0

    #     # solve if has required variables
    #     self.variables["v2"] = sqrt((self.variables["v1"]**2) + (2 * self.variables["a"] * self.variables["d"]))
    #     return 1
    
    # def _timeSolve1(self) -> float:
    #     """Sets the time variable t based on v1, d, and a. If required variables not set, returns 0. If succeeds, returns 1."""
        
    #     # check for required variables
    #     if self._checkNeededSolveVars(["v1", "d", "a"]) == 0:
    #         return 0

    #     # solve if has required variables
    #     if self.variables["a"] != 0:
    #         # quadratic formula, choose the positive answer
    #         a = (0.5 * self.variables["a"])
    #         b = self.variables["v1"]
    #         c = self.variables["d"]
    #         ans1 = (-b + sqrt(b**2 - 4*a*c)) / (2*a)
    #         ans2 = (-b - sqrt(b**2 - 4*a*c)) / (2*a)
    #         # take positive using max
    #         self.variables["t"] = max(ans1, ans2)
    #     else:
    #         # if is not a quadratic
    #         self.variables["t"] = self.variables["d"] / self.variables["v2"]
    #     return 1

    # def _timeSolve2(self) -> float:
    #     """Sets the time variable t based on v2, d, and a. If required variables not set, returns 0. If succeeds, returns 1."""
        
    #     # check for required variables
    #     if self._checkNeededSolveVars(["v2", "d", "a"]) == 0:
    #         return 0

    #     # solve if has required variables
    #     if self.variables["a"] != 0:
    #         # quadratic formula, choose the positive answer
    #         a = (-0.5 * self.variables["a"])
    #         b = self.variables["v2"]
    #         c = self.variables["d"]
    #         ans1 = (-b + sqrt(b**2 - 4*a*c)) / (2*a)
    #         ans2 = (-b - sqrt(b**2 - 4*a*c)) / (2*a)
    #         # take positive using max
    #         self.variables["t"] = max(ans1, ans2)
    #     else:
    #         # if is not a quadratic
    #         self.variables["t"] = self.variables["d"] / self.variables["v2"]
    #     return 1
    
    # def _timeSolve3(self) -> float:
    #     """Sets the time variable t based on v1, v2, and d. If required variables not set, returns 0. If succeeds, returns 1."""
        
    #     # check for required variables
    #     if self._checkNeededSolveVars(["v1", "v2", "d"]) == 0:
    #         return 0

    #     # solve if has required variables
    #     self.variables["t"] = (self.variables["d"] * 2) / (self.variables["v1"] + self.variables["v2"])
    #     return 1
    
    # def _timeSolve4(self) -> float:
    #     """Sets the time variable t based on v1, v2, and a. If required variables not set, returns 0. If succeeds, returns 1."""
        
    #     # check for required variables
    #     if self._checkNeededSolveVars(["v1", "v2", "a"]) == 0:
    #         return 0

    #     # solve if has required variables
    #     self.variables["t"] = (self.variables["v1"] - self.variables["v2"]) / self.variables["a"]
    #     return 1

# test
# TODO: move
# TODO: use parse function and pass in a str directly
KinematicsQuestion({"time": (1.0, 2.0), "displacement": (1.0, 2.0), "initial_velocity": (1.0, 2.0), "final_velocity": (1.0, 2.0)}, "displacement", "")
print(KinematicsQuestion.answer)