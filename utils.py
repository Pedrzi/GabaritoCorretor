from dataclasses import dataclass
import math
from math import floor


@dataclass
class Vector2D:
    x: int | float
    y: int | float

    def __call__(self) -> tuple[int, int]:
        return self.x, self.y

    def __repr__(self) -> str:
        return f"Vector2D({self.x}, {self.y})"

    def __add__(self, other: "Vector2D") -> "Vector2D":
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        raise TypeError("Unsupported operand type for +: 'Vector2D' and '{}'".format(type(other)))

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        raise TypeError("Unsupported operand type for -: 'Vector2D' and '{}'".format(type(other)))

    def __mul__(self, other) -> "Vector2D":
        if isinstance(other, (int, float)):  # Scalar multiplication
            return Vector2D(self.x * other, self.y * other)
        elif isinstance(other, Vector2D):  # Element-wise multiplication
            return Vector2D(self.x * other.x, self.y * other.y)
        raise TypeError("Unsupported operand type for *: 'Vector2D' and '{}'".format(type(other)))

    def __truediv__(self, other) -> "Vector2D":
        if isinstance(other, (int, float)) and other != 0:
            return Vector2D(self.x / other, self.y / other)
        raise ValueError("Cannot divide by zero" if other == 0 else "Invalid type for division")

    def magnitude(self) -> float:
        """Returns the magnitude (length) of the vector."""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self) -> "Vector2D":
        """Returns a unit vector (same direction, magnitude of 1)."""
        mag = self.magnitude()
        return self / mag if mag != 0 else Vector2D(0, 0)

    def dot(self, other: "Vector2D") -> float:
        """Returns the dot product of two vectors."""
        if isinstance(other, Vector2D):
            return self.x * other.x + self.y * other.y
        raise TypeError("Unsupported operand type for dot product: '{}'".format(type(other)))

    def distance_to(self, other: "Vector2D") -> float:
        """Calculates the Euclidean distance between two vectors."""
        if isinstance(other, Vector2D):
            return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        raise TypeError("Unsupported operand type for distance_to: '{}'".format(type(other)))


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

    @staticmethod
    def calculate_rectangle_size(point_a: tuple[int, int], point_b: tuple[int, int]) -> Vector2D:
        height: int
        width: int

        height = max(point_a[1], point_b[1]) - min(point_a[1], point_b[1])
        width = max(point_a[0], point_b[0]) - min(point_a[0], point_b[0])

        return Vector2D(width, height)
