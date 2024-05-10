from dataclasses import InitVar, dataclass, field
from random import random
from uuid import UUID, uuid4


@dataclass(slots=True)
class Variable:
    """
    A Variable relevant to a Question subclass. Contains display information. Randomizes value on creation and generates a unique uuid.\n
    Attributes:\n
        name (str): which variable in the specific question this refers to. this is the internal name of the variable,\n
        units (str): appended to the end of the variable when converted to str,\n
        displayName (str): character(s) used to refer to the variable in the question text, and so the name it will be given when converted to str,\n
        decimalPlaces (int): decimal places of precision to round to when converting to str,\n
        value (float): the value of the variable,\n
        varID (UUID): unique uuid for this variable, used when storing it in database
    """
    range: InitVar[list[float | int]]
    name: str
    # these defaults are used when loading answers from database
    units: str = ""
    displayName: str = ""
    # default is actual set in the VariableConfig dataclass
    decimalPlaces: int = 3
    value: float = field(init=False)
    varID: UUID = field(init=False, default_factory=uuid4)

    def __post_init__(self, range: tuple[float | int, float | int]) -> None:
        """Randomizes the variable value within the given range."""
        # randomize within range
        self.value = range[0] + random() * (range[1] - range[0])
        return
    
    def __str__(self) -> str:
        """Assembles the variable as it should be displayed to a student, with its value to the correct decimal places, units, and correct display variable name."""
        return f"{self.displayName} = {self.value:.{self.decimalPlaces}f}{self.units}"
    
    @classmethod
    def fromStored(cls, varID: UUID, value: float, **kwargs):
        """
        Create a Variable from stored data. **kwargs should include all defined values not already in signature. It is separated so that answer values, which don't necessarily have unique values for all attribute, can use this classmethod more easily.\n
        Returns an instance of the class this is called on.
        """
        # create with a stand-in range
        var = cls(range=[1.0, 1.0], **kwargs)
        var.varID = varID
        var.value = value
        return var
