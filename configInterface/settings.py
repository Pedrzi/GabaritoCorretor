from dataclasses import  dataclass
from configInterface.propertysetter import PropertySetter
from configInterface.template import Template


class Settings:
    def __init__(self):
        self.properties_holder: PropertySetter = PropertySetter()
        self.template_holder: Template = Template()


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


current_settings: Settings = Settings()