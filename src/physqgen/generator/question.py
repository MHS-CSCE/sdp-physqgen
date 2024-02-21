"""
Question Datastructures
ICS4U
Stuart, Isabelle, Amelia
Represent different types of questions.
History:
February 9, 2024: Implement Question and KinematicsQuestion
February 20, 2024: Fix KinematicsQuestion, implement rest of solving ofrmulas.
"""

from dataclasses import InitVar, dataclass, field
from enum import Enum
from io import StringIO
from math import sqrt
from random import random
from typing import Literal
from uuid import UUID, uuid4  # uuid4 doesn't include private information


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
    # correct_range default was agreed upon with client at 10%
    correct_range: float = 0.1

    # always leave default
    id: UUID = field(default_factory=uuid4, init=False)

    def __post_init__(self, variableConfig: dict[str, list[float, float]]) -> None:
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
            # define properties for each variable subclasses, which use this defined value
        
    def __str__(self) -> str:
        """Returns a string representation of the question variables."""
        # returns a list of the question's variables

        # intialize with first value
        varText = StringIO()

        # TODO: ask client about prefered specificity here
        # generator comprehension, yields next variable and value consecutively to writelines
        generator = (f"{var.name.lower()} = {getattr(self, var.name.lower()):.2f}\n" for var in self.variables)
        varText.writelines(generator)

        return varText.getvalue()
    
    @property
    def answer(self) -> float:
        """Returns the answer to the question given the randomized variable values."""
        # TODO: currently returns property instead of property value
        return getattr(self, self.solveVariable)

    def check_answer(self, submitted) -> bool:
        """Returns True if the submitted answer is within the correct_range variance from the question's calculated answer."""
        return (submitted > (self.answer * (1 - self.correct_range))) and (submitted < (self.answer * (1 + self.correct_range)))
    
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
        value = getattr(self, self.enumToAttribute(self.variables.DISPLACEMENT, True), False)

        # if fetches value, return it
        if type(value) is float:
            return value
        
        # otherwise use equations
        else:
            # check if each var is defined
            v1Defined = self.variableDefined("initial_velocity")
            v2Defined = self.variableDefined("final_velocity")
            tDefined = self.variableDefined("time")

            # not needed
            # aDefined = self.variableDefined("acceleration")

            # assume that enough variables are defined, find the one that isn't
            if not v1Defined:
                v2 = self.getVariableValue(self.enumToAttribute(self.variables.FINAL_VELOCITY))
                t = self.getVariableValue(self.enumToAttribute(self.variables.TIME))
                a = self.getVariableValue(self.enumToAttribute(self.variables.ACCELERATION))
                
                # d from v2, t, a
                return (v2 * t) - ((0.5 * a)* (t**2))
            
            elif not v2Defined:
                v1 = self.getVariableValue(self.enumToAttribute(self.variables.INITIAL_VELOCITY))
                t = self.getVariableValue(self.enumToAttribute(self.variables.TIME))
                a = self.getVariableValue(self.enumToAttribute(self.variables.ACCELERATION))

                # d from v1, t, a
                return (v1 * t) + ((0.5 * a) * (t**2))

            elif not tDefined:
                v1 = self.getVariableValue(self.enumToAttribute(self.variables.INITIAL_VELOCITY))
                v2 = self.getVariableValue(self.enumToAttribute(self.variables.FINAL_VELOCITY))
                a = self.getVariableValue(self.enumToAttribute(self.variables.ACCELERATION))

                # d from v1, v2, a
                return ((v2**2) - (v1**2)) / (2 * a)
            
            else: # not aDefined
                v1 = self.getVariableValue(self.enumToAttribute(self.variables.INITIAL_VELOCITY))
                v2 = self.getVariableValue(self.enumToAttribute(self.variables.FINAL_VELOCITY))
                t = self.getVariableValue(self.enumToAttribute(self.variables.TIME))

                # d from v1, v2, t formula
                return ((v1 + v2) / 2) * t                                       
    
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
        
        # if fetches value, return it
        if type(value) is float:
            return value
        
        # otherwise use equations
        else:
            # check if each var is defined
            dDefined = self.variableDefined("displacement")
            v2Defined = self.variableDefined("final_velocity")
            tDefined = self.variableDefined("time")

            # not needed
            # aDefined = self.variableDefined("acceleration")

            # assume that enough variables are defined, find the one that isn't
            if not dDefined:
                v2 = self.getVariableValue(self.enumToAttribute(self.variables.FINAL_VELOCITY))
                t = self.getVariableValue(self.enumToAttribute(self.variables.TIME))
                a = self.getVariableValue(self.enumToAttribute(self.variables.ACCELERATION))
                
                # v1 from v2, t, a
                return v2 - (a*t)
            
            elif not v2Defined:
                d = self.getVariableValue(self.enumToAttribute(self.variables.DISPLACEMENT))
                t = self.getVariableValue(self.enumToAttribute(self.variables.TIME))
                a = self.getVariableValue(self.enumToAttribute(self.variables.ACCELERATION))

                # v1 from d, t, a
                return (d / t) - (0.5 * a * t)

            elif not tDefined:
                d = self.getVariableValue(self.enumToAttribute(self.variables.DISPLACEMENT))
                v2 = self.getVariableValue(self.enumToAttribute(self.variables.FINAL_VELOCITY))
                a = self.getVariableValue(self.enumToAttribute(self.variables.ACCELERATION))

                # v1 from d, v2, a
                # TODO: make sure sqrt doesn't cause problems
                return sqrt(v2**2 - 2*a*d)

            else: # not aDefined
                d = self.getVariableValue(self.enumToAttribute(self.variables.DISPLACEMENT))
                v2 = self.getVariableValue(self.enumToAttribute(self.variables.FINAL_VELOCITY))
                t = self.getVariableValue(self.enumToAttribute(self.variables.TIME))

                # v1 from d, v2, t formula
                return ((d*2) / t) - v2
    
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
        
        # if fetches value, return it
        if type(value) is float:
            return value
        
        # otherwise use equations
        else:
            # check if each var is defined
            dDefined = self.variableDefined("displacement")
            v1Defined = self.variableDefined("initial_velocity")
            tDefined = self.variableDefined("time")

            # not needed
            # aDefined = self.variableDefined("acceleration")

            # assume that enough variables are defined, find the one that isn't
            if not dDefined:
                v1 = self.getVariableValue(self.enumToAttribute(self.variables.INITIAL_VELOCITY))
                t = self.getVariableValue(self.enumToAttribute(self.variables.TIME))
                a = self.getVariableValue(self.enumToAttribute(self.variables.ACCELERATION))
                
                # v2 from v1, t, a
                return (a*t) + v1
            
            elif not v1Defined:
                d = self.getVariableValue(self.enumToAttribute(self.variables.DISPLACEMENT))
                t = self.getVariableValue(self.enumToAttribute(self.variables.TIME))
                a = self.getVariableValue(self.enumToAttribute(self.variables.ACCELERATION))

                # v2 from d, t, a
                return (d / t) + (0.5 * a * t)

            elif not tDefined:
                d = self.getVariableValue(self.enumToAttribute(self.variables.DISPLACEMENT))
                v1 = self.getVariableValue(self.enumToAttribute(self.variables.INITIAL_VELOCITY))
                a = self.getVariableValue(self.enumToAttribute(self.variables.ACCELERATION))

                # v2 from d, v1, a
                # TODO: make sure sqrt doesn't cause problems
                return sqrt(v1**2 + 2*a*d)

            else: # not aDefined
                d = self.getVariableValue(self.enumToAttribute(self.variables.DISPLACEMENT))
                v1 = self.getVariableValue(self.enumToAttribute(self.variables.INITIAL_VELOCITY))
                t = self.getVariableValue(self.enumToAttribute(self.variables.TIME))

                # v2 from d, v1, t formula
                return ((d*2) / t) - v1
    
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
        
        # if fetches value, return it
        if type(value) is float:
            return value
        
        # otherwise use equations
        else:
            # check if each var is defined
            dDefined = self.variableDefined("displacement")
            v1Defined = self.variableDefined("initial_velocity")
            v2Defined = self.variableDefined("final_velocity")

            # not needed
            # aDefined = self.variableDefined("acceleration")

            # assume that enough variables are defined, find the one that isn't
            if not dDefined:
                v1 = self.getVariableValue(self.enumToAttribute(self.variables.INITIAL_VELOCITY))
                v2 = self.getVariableValue(self.enumToAttribute(self.variables.FINAL_VELOCITY))
                a = self.getVariableValue(self.enumToAttribute(self.variables.ACCELERATION))
                
                # t from v1, v2, a
                # TODO: fix v1=v2 situation, gives 0/0
                return (v2 - v1) / a
            
            elif not v1Defined:
                d = self.getVariableValue(self.enumToAttribute(self.variables.DISPLACEMENT))
                v2 = self.getVariableValue(self.enumToAttribute(self.variables.FINAL_VELOCITY))
                a = self.getVariableValue(self.enumToAttribute(self.variables.ACCELERATION))

                # t from d, v2, a
                # TODO: for now, always return highest answer even if there are two correct values
                return (v2/a) + (sqrt(v2**2 - 2*a*d)/a) # negative in between for other answer

            elif not v2Defined:
                d = self.getVariableValue(self.enumToAttribute(self.variables.DISPLACEMENT))
                v1 = self.getVariableValue(self.enumToAttribute(self.variables.INITIAL_VELOCITY))
                a = self.getVariableValue(self.enumToAttribute(self.variables.ACCELERATION))

                # t from d, v1, a
                return (-v1/a) + (sqrt(v1**2 - 2*a*d)/a)

            else: # not aDefined
                d = self.getVariableValue(self.enumToAttribute(self.variables.DISPLACEMENT))
                v1 = self.getVariableValue(self.enumToAttribute(self.variables.INITIAL_VELOCITY))
                v2 = self.getVariableValue(self.enumToAttribute(self.variables.FINAL_VELOCITY))

                # t from d, v1, v2 formula
                return (d*2)/(v1 + v2)
    
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
        
        # if fetches value, return it
        if type(value) is float:
            return value
        
        # otherwise use equations
        else:
            # check if each var is defined
            dDefined = self.variableDefined("displacement")
            v1Defined = self.variableDefined("initial_velocity")
            v2Defined = self.variableDefined("final_velocity")

            # not needed
            # tDefined = self.variableDefined("time")

            # assume that enough variables are defined, find the one that isn't
            if not dDefined:
                v1 = self.getVariableValue(self.enumToAttribute(self.variables.INITIAL_VELOCITY))
                v2 = self.getVariableValue(self.enumToAttribute(self.variables.FINAL_VELOCITY))
                t = self.getVariableValue(self.enumToAttribute(self.variables.TIME))
                
                # a from v1, v2, t
                return 
            
            elif not v1Defined:
                d = self.getVariableValue(self.enumToAttribute(self.variables.DISPLACEMENT))
                v2 = self.getVariableValue(self.enumToAttribute(self.variables.FINAL_VELOCITY))
                t = self.getVariableValue(self.enumToAttribute(self.variables.TIME))

                # a from d, v2, t
                return # TODO

            elif not v2Defined:
                d = self.getVariableValue(self.enumToAttribute(self.variables.DISPLACEMENT))
                v1 = self.getVariableValue(self.enumToAttribute(self.variables.INITIAL_VELOCITY))
                t = self.getVariableValue(self.enumToAttribute(self.variables.TIME))

                # a from d, v1, t
                return ((2*d) / (t**2)) - ((2*v1) / (t))

            else: # not tDefined
                d = self.getVariableValue(self.enumToAttribute(self.variables.DISPLACEMENT))
                v1 = self.getVariableValue(self.enumToAttribute(self.variables.INITIAL_VELOCITY))
                v2 = self.getVariableValue(self.enumToAttribute(self.variables.FINAL_VELOCITY))

                # a from d, v1, v2 formula
                return ((2*v2) / (t)) - ((2*d) / (t**2)) 

    def acceleration_validate(self, value: float) -> bool:
        """Uses appropriate validation functions to ensure acceleration is valid. Currently allowed any positive float value."""
        # TODO: might change to not allow acceleration of 0
        if self.validatePositiveAttribute(value):
            return True
        else:
            return False
