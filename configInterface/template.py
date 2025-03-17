from configInterface.preprocessors import PreProcessor
from configInterface.utils import Utils
from dataclasses import dataclass, field
from configInterface.utils import Vector2D


@dataclass
class FieldBlocks:
    name: str
    bubbles_gap: int
    labels_gap: int
    origin_x: int
    origin_y: int
    field_labels: list

    _field_type: str = field(default="QTYPE_MCQ5", init=False)
    _bubble_values: list = field(default=None, init=False)
    _direction: str = field(default=None, init=False)

    @property
    def field_type(self) -> str:
        return self._field_type

    @field_type.setter
    def field_type(self, value: str, bubble_values: list[str] = None, direction: str = None) -> None:
        f"""
        Only set bubble_values and direction when using a custom field_type

                    available field_types:

                    QTYPE_INT
                    QTYPE_MCQ4
                    QTYPE_MCQ5
                    CUSTOM
        """
        self._field_type = value
        if value == "CUSTOM" and Utils.has_value(bubble_values) and Utils.has_value(direction):
            self._bubble_values = bubble_values
            self._direction = direction

    @property
    def custom_field_type(self) -> dict[str: str | list[str]]:
        return {
            "bubbleValues": self._bubble_values,
            "direction": self._direction
        }

    @property
    def field(self) -> dict[str: int | str | list[str | int]]:
        f: dict = {
            "bubblesGaps": self.bubbles_gap,
            "fieldLabels": self.field_labels,
            "labelsGap": self.labels_gap,
            "origin": [self.origin_x, self.origin_y]
        }

        if self.field_type == "CUSTOM":
            f.update(self.custom_field_type)
        else:
            f["fieldType"] = self.field_type

        return f


@dataclass
class Template:
    _page_dimensions:   Vector2D = field(init=False)
    _bubble_dimensions: Vector2D = field(init=False)
    _custom_labels:    dict[str: list[str]] = field(default_factory=dict, init=False)
    _field_blocks:     dict[str: dict[any]] = field(default_factory=dict, init=False)
    _preprocessors:    list[any] = field(default_factory=list, init=False)
    _data:             dict[str: any] = field(default_factory=dict, init=False)

    @property
    def data(self):
        self._data = {
            "pageDimensions": self.page_dimensions,
            "bubbleDimensions": self.bubble_dimensions,
            "preProcessors": self._preprocessors,
            "fieldBlocks": self._field_blocks
        }
        if self.custom_labels:
            self._data["customLabels"] = self.custom_labels
        return self._data

    @property
    def page_dimensions(self) -> Vector2D:
        return self._page_dimensions

    @page_dimensions.setter
    def page_dimensions(self, value: Vector2D) -> None:
        self._page_dimensions = value

    @property
    def bubble_dimensions(self) -> Vector2D:
        return self._bubble_dimensions

    @bubble_dimensions.setter
    def bubble_dimensions(self, value: Vector2D) -> None:
        self._bubble_dimensions = value

    @property
    def custom_labels(self):
        return self._custom_labels

    @custom_labels.setter
    def custom_labels(self, *args: FieldBlocks) -> None:
        for field_block in args:
            self._custom_labels[field_block.name] = field_block.field
    @property
    def preprocessor(self):
        return self._preprocessors

    @preprocessor.setter
    def preprocessor(self, preprocessor: PreProcessor) -> None:
        self._preprocessors.append(preprocessor)

current_template = Template()