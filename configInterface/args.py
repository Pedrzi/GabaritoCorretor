from dataclasses import dataclass, field, KW_ONLY


@dataclass
class Args:
    _: KW_ONLY
    _input_path: str = "Nothing"
    _output_path: str = "Nothing"
    _debug: bool = field(default=True, repr=False, init=False)
    _auto_align: bool = field(default=False, repr=False, init=False)
    _set_layout: bool = field(default=False, repr=False, init=False)

    @property
    def properties(self) -> dict:
        return {
            "input_paths": self._input_path,
            "debug": self._debug,
            "output_dir": self.output_path,
            "autoAlign": self._auto_align,
            "setLayout": self._set_layout,
        }

    @property
    def input_path(self) -> str:
        return self._input_path

    @input_path.setter
    def input_path(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Input path must be a string.")
        self._input_path = value

    @property
    def output_path(self) -> str:
        return self._output_path

    @output_path.setter
    def output_path(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Output path must be a string.")
        self._output_path = value

    def toggle_debug(self):
        self._debug = not self._debug
