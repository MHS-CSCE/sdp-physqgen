from dataclasses import InitVar, dataclass, field
from random import random
from uuid import UUID, uuid4


@dataclass(slots=True)
class Variable:
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
        """Create a Variable from stored data instead of randomizing."""
        # create with a stand-in range
        var = cls(range=[1.0, 1.0], **kwargs)
        var.varID = varID
        var.value = value
        return var

