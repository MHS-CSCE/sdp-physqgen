from dataclasses import InitVar, dataclass, field
from random import random
from uuid import UUID, uuid4


@dataclass(slots=True)
class Variable:
    range: InitVar[list[float | int]]
    name: str
    units: str
    displayName: str
    decimalPlaces: int = 3
    value: float = field(init=False)
    varID: UUID = field(init=False, default_factory=uuid4)

    def __post_init__(self, range: tuple[float | int, float | int]) -> None:
        """Randomizes the variable value within the given range."""
        # randomize within range
        self.value = range[0] + random() * (range[1] - range[0])
        return
    
    @classmethod
    def fromStored(cls, name: str, value: float, units: str, displayName: str, decimalPlaces: int, varID: UUID):
        """Create a Variable from stored data instead of randomizing."""
        # create with a stand-in range
        var = cls(range=[1.0, 1.0], name=name, units=units, displayName=displayName, decimalPlaces=decimalPlaces)
        var.varID = varID
        var.value = value
        return var

