from dataclasses import dataclass, field

@dataclass
class Config:

    _display_width: int = field(default=900, repr=False)
    _display_height: int = field(default=600, repr=False)
    _image_level: int = field(default=0, repr=False)

    @property
    def dimensions(self) -> dict:
        return {
            "display_width": self._display_width,
            "display_height": self._display_height
        }

    @property
    def outputs(self) -> dict:
        return {
            "show_image_level": self._image_level
        }

    @property
    def data(self) -> dict:
        return {
            "dimensions": self.dimensions,
            "outputs": self.outputs
        }

    def set_display_size(self, width: int, height: int) -> None:
        if width < 0 or height < 0:
            raise ValueError("Width and height must be positive integers.")
        self._display_width = width
        self._display_height = height

    def set_image_level(self, level: int) -> None:
        if level < 0:
            raise ValueError("Image level must be a non-negative integer.")
        self._image_level = level