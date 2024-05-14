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
        return not any(
            (
                # this check applies if the range crosses 0, or includes 0.0 or 0 as one endpoint
                float(self.range[0] * self.range[1]) <= 0.0,
                # these checks are extra, to ensure that floating point calculations don't make the above not exactly 0.0 even if one bound is
                # afaik, these should never apply if the above doesn't, but it doesn't hurt much to include them given the uncertainty around floating point number equality
                float(self.range[0]) == 0.0,
                float(self.range[1]) == 0.0,
                # these would likely only result from mistyping, but may still mess up the checks above
                float(self.range[0]) == -0.0,
                float(self.range[1]) == -0.0
            )
        )
    
    def nonOverlapping(self, other) -> bool:
        """Returns True if the ranges of this VariableConfig and other (also a VariableConfig) do not overlap, False otherwise."""
        # all other cases are invalid elsewhere
        r1low = self.range[0]
        r1high = self.range[1]
        r2low = other.range[0]
        r2high = other.range[1]
        # check if they are overlapping and reverse it, it's a simpler check
        return not (r1low <= r2high and r1high >= r2low)
