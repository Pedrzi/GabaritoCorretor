from configInterface.config import  Config
from configInterface.args import Args
from configInterface.template import Template
from utils import Vector2D


class Settings:
    def __init__(self):
        self.properties_holder: Args = Args()
        self.template_holder: Template = Template()
        self.config_holder: Config = Config()


    @property
    def input_path(self) -> str:
        return self.properties_holder.input_path

    @input_path.setter
    def input_path(self, value) -> None:
        if isinstance(value, str):
            self.properties_holder.input_path = value

    @property
    def output_path(self) -> str:
        return self.properties_holder.output_path

    @output_path.setter
    def output_path(self, value) -> None:
        if isinstance(value, str):
            self.properties_holder.output_path = value

    @property
    def page_dimensions(self):
        return self.template_holder.page_dimensions

    @page_dimensions.setter
    def page_dimensions(self, value: Vector2D):
        if isinstance(value, Vector2D):
            self.template_holder.page_dimensions = value

    @property
    def bubble_dimensions(self):
        return self.template_holder.bubble_dimensions

    @bubble_dimensions.setter
    def bubble_dimensions(self, value):
        if isinstance(value, Vector2D):
            self.template_holder.bubble_dimensions = value
