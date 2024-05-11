from dataclasses import InitVar, dataclass, field
from random import random
from uuid import UUID, uuid4

from physqgen.database import executeOnDatabase


@dataclass(slots=True)
class Variable:
    """
    A Variable relevant to a Question subclass. Contains display information. Randomizes value on creation and generates a unique uuid.\n
    Attributes:\n
        variableName (str): which variable in the specific question this refers to. this is the internal name of the variable,\n
        units (str): appended to the end of the variable when converted to str,\n
        displayName (str): character(s) used to refer to the variable in the question text, and so the name it will be given when converted to str,\n
        decimalPlaces (int): decimal places of precision to round to when converting to str,\n
        value (float): the value of the variable,\n
        varID (UUID): unique uuid for this variable, used when storing it in database
    """
    variableName: str

    # if is not None, value will be randomized using it, overriding any given value
    range: InitVar[list[float | int] | None] = None
    # can be left as None if will be randomized
    value: float | None = None

    # defaults used for answer variables, which do not have display info
    units: str = ""
    displayName: str = ""

    # default is actual set in the VariableConfig dataclass
    decimalPlaces: int = 3
    uuid: UUID = field(default_factory=uuid4)

    def __post_init__(self, range: tuple[float | int, float | int] | None) -> None:
        """If range is not None, sets a random value based on it. If both range and value are None, raised a TypeError."""
        if range is not None:
            self.value = self.randomizeValue(range)
        elif self.value is None:
            raise TypeError("Both range and value were None on Variable construction, so no vallid value could be assigned.")
        return

    @staticmethod
    def randomizeValue(range: tuple[float | int, float | int]) -> float:
        """Returna a randomized value within the given range."""
        return range[0] + random() * (range[1] - range[0])

    def __str__(self) -> str:
        """Assembles the variable as it should be displayed to a student, with its value to the correct decimal places, units, and correct display variable name."""
        return f"{self.displayName} = {self.value:.{self.decimalPlaces}f}{self.units}"
    
    @classmethod
    def fromDatabase(cls, databasePath: str, variableUUID: str | UUID):
        """Fetches the variable stored in the database with the given variableUUID and returns an instance of cls populated with it."""
        sql = '''SELECT (
            NAME,
            VALUE,
            UNITS,
            DISPLAY_NAME,
            DECIMAL_PLACES
        ) FROM VARIABLES WHERE VARIABLE_UUID=?'''
        replacements = tuple(str(variableUUID))
        # TODO: check that returned valid result
        # index 0 is the first (and only) row that met the criteria
        results = executeOnDatabase(databasePath, sql, replacements)[0]

        return cls(
            variableName=results[0],
            value=results[1],
            units=results[2],
            displayName=results[3],
            decimalPlaces=results[4],
            uuid=variableUUID
        )
    
    @classmethod
    def fromConfig(cls, variableConfig):
        """Generates a Variable with random value based on variableConfig (VariableConfig)."""
        return cls(
            range=variableConfig.range,
            variableName=variableConfig.variableName,
            units=variableConfig.units,
            displayName=variableConfig.displayName,
            decimalPlaces=variableConfig.decimalPlaces
        )
