from dataclasses import dataclass


@dataclass(slots=True)
class VariableConfig:
    """
    Configuration for a specific variable in a Question. Can be used to generate random Variables.\n
    Attributes:\n
        range is a list containing the upper and lower bounds the value should be randomized within,\n
        See Variable class for remaining attributes\n
            does not have a uuid
    """
    variableName: str
    range: list[float | int]
    units: str
    displayName: str
    decimalPlaces: int = 3
    
    def nonZero(self) -> bool:
        """Checks if the configured range is allowed, disallowing it from including 0.0. Returns True if valid, False if not valid."""
        # if the bounds are different signs, they will be below 0.0
        # if both bounds are 0.0, they will equal 0.0
        # if one bound is 0.0, the other checks will catch them assuming the first doesn't
        return not any(
            (
                float(self.range[0] * self.range[1]) <= 0.0,
                float(self.range[0]) == 0.0,
                float(self.range[1]) == 0.0
            )
        )
    
    def nonOverlapping(self, other) -> bool:
        """Returns True if the ranges of this VariableConfig and other (also a VariableConfig) do not overlap, False otherwise. Used to check if two VariableConfig ranges are valid in terms of each-other"""
        # all other cases are invalid elsewhere
        r1low = self.range[0]
        r1high = self.range[1]
        r2low = other.range[0]
        r2high = other.range[1]
        return (r1low > r2high or r1high < r2low)
