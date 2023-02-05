class TerraformDict(dict):
    """
        Basic terraform dictionary of values
    """

    @staticmethod
    def encode_str(value: str) -> str:
        return f'"{value}"'

    @staticmethod
    def encode_bool(value: bool) -> str:
        str(value).lower()

    @staticmethod
    def encode_dict(value: dict) -> str:
        return str(TerraformDict(value)).replace("\n", "\n\t")

    @staticmethod
    def encode_int(value: int) -> str:
        return str(value)

    @staticmethod
    def encode_list(value: list) -> str:
        strings_list = []
        for i in value:
            strings_list.append(
                TerraformDict.encode_value(i)
            )

        list_items_string = ",\n\t\t".join(strings_list)

        return f"[\n\t\t{list_items_string}\n\t]"

    @staticmethod
    def encode_value(value) -> str:
        out = str(value).replace('\n', '\n\t')

        if      isinstance(value, str):
            out = TerraformDict.encode_str(value)
        elif    isinstance(value, bool):
            out = TerraformDict.encode_bool(value)
        elif    isinstance(value, list):
            out = TerraformDict.encode_list(value)
        elif    isinstance(value, BaseNamedTerraformBlock):
            out = repr(value)

        return out

    def __str__(self) -> str:
        params_str = ""

        for k,v in self.items():
            value = self.encode_value( v )

            params_str += f"\n\t{k} \t= {value}"
        
        if not params_str: return "{ }"

        return "{" + params_str + "\n}"

class BlockParams(TerraformDict):
    """
        Terraform block parameters, everything that goes inside brackets when defining a resource

        resource "aws_instance" "my_instance" {
            BlockParams...
        }
    """

    _child_blocks: list['BaseTerraformBlock']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._child_blocks = []
        pass

    def add_child_blocks(self, *blocks: 'BaseTerraformBlock'):
        self._child_blocks.extend( blocks )

    @staticmethod
    def encode_block(block: 'BaseTerraformBlock'):
        return str(block).replace("\n", "\n\t")

    def __str__(self) -> str:
        params_str = super().__str__()

        # If no child blocks, return the regular paramaters only dict string
        if not self._child_blocks: return params_str

        block_strings = [
            self.encode_block(block) 
                for block in self._child_blocks
        ]

        return params_str[:-1] + "\n\t" + ("\n\n\t".join(block_strings)) + "\n}"

class BaseTerraformBlock():
    """
        Base class for representing a block in terraform

        <block_category> {
            ...
        }
    """
    _block_category     : str = ""

    _block_params       : BlockParams

    def __init__(self, params: dict = {}) -> None:
        self._block_params      = BlockParams( params or {} )

    @property
    def _block_params_str_(self) -> str:
        return str(self._block_params)

    def set_param(self, **kwargs):
        for k,v in kwargs.items():
            self._block_params[k] = v

    def add_child_blocks(self, *blocks: list['BaseTerraformBlock']):
        self._block_params.add_child_blocks( *blocks )

    def as_reference_str(self) -> str:
        return self.__repr__()

    def __str__(self) -> str:
        out_str = f"{self._block_category}"

        out_str += f" {self._block_params_str_}"

        return out_str

class BaseNamedTerraformBlock(BaseTerraformBlock):
    """
        Extension of base block that supports named items
        <block_category> "<block_name>" {
            ...
        }
    """

    _block_name: str = None

    def __init__(self, params: dict = {}, block_name: str = "") -> None:
        super().__init__(params)
        self._block_name = self._block_name or block_name
    
    def __repr__(self) -> str:
        return f"{self._block_category}.{self._block_name}"

    def __str__(self) -> str:
        out_str = f"{self._block_category}"

        if self._block_name:
            out_str += f" \"{self._block_name}\""

        out_str += f" {self._block_params_str_}"

        return out_str

class BaseTypedTerraformBlock(BaseNamedTerraformBlock):
    """
        Extension of named blocks that supports types, Such as in the case of resources.

        <block_category> <block_type> <block_name> {
            ...
        }
    """

    _block_type : str = None

    def __init__(self, params: dict = {}, block_type: str = "", block_name: str = "") -> None:
        super().__init__(block_name, params)
        self._block_type = self._block_type or block_type

    def __repr__(self) -> str:
        return f"{self._block_category}.{self._block_type}.{self._block_name}"

    def __str__(self) -> str:
        out_str = f"{self._block_category}"

        if self._block_type:
            out_str += f" \"{self._block_type}\""

        if self._block_name:
            out_str += f" \"{self._block_name}\""

        out_str += f" {self._block_params_str_}"

        return out_str
