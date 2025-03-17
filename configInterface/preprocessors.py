from dataclasses import dataclass


class PreProcessor:

    @property
    def name(self) -> str:
        return self.__class__.__name__


@dataclass
class Levels(PreProcessor):
    low: int
    high: int

    @property
    def options(self) -> dict:
        return {
            "low": self.low,
            "high": self.high
        }

@dataclass
class GaussianBlur(PreProcessor):
    ksizex: int
    ksizey: int
    sigmax: int

    @property
    def options(self) -> dict:
        return {
        "kSize": [self.ksizex, self.ksizey],
        "sigmaX": self.sigmax
        }

@dataclass
class CropPage(PreProcessor):
    morph_kernelx: int
    morph_kernely: int

    @property
    def options(self) -> dict:
        return {
            "morphKernel": [self.morph_kernelx, self.morph_kernely]
        }
@dataclass
class CropOnMarkers(PreProcessor):
    path_to_marker: str
    ratio: int

    @property
    def options(self) -> dict:
        return {
            "relativePath": self.path_to_marker,
            "sheetToMarkerWidthRatio": self.ratio
        }