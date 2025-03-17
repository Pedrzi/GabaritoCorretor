from dataclasses import dataclass

class Utils:

    @staticmethod
    def validate_positive_integer(v: any) -> None:
        if not isinstance(v, int):
            raise ValueError("value must be a integer")
        if v < 0:
            raise ValueError("value must be a positive integer")

    @staticmethod
    def has_value(v: any) -> bool:
        if v is None:
            raise ValueError(f"Variable must be set")
        return True

@dataclass
class Vector2D:
    x: int
    y: int

    def __call__(self) -> list[int]:
        return [self.x, self.y]

