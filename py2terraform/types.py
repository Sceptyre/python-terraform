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
        elif    isinstance(value, TerraformBlockBase):
            if not value.is_named:
                raise Exception(f"Unable to map unamed resource {repr(value)}")

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

    _child_blocks: list['TerraformBlockBase']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._child_blocks = []
        pass

    def add_child_blocks(self, *blocks: 'TerraformBlockBase'):
        self._child_blocks.extend( blocks )

    @staticmethod
    def encode_block(block: 'TerraformBlockBase'):
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

class TerraformBlockBase():
    _block_category     : str = None
    _block_type         : str = None
    _block_name         : str = None

    _block_params       : BlockParams = None

    def __init__(
        self, 
        params          : dict = {}, 
        child_blocks    : list['TerraformBlockBase'] = [],
        
        block_category  : str = "",
        block_type      : str = "",
        block_name      : str = ""
    ):
        self._block_category    = block_category    or self._block_category
        self._block_type        = block_type        or self._block_type
        self._block_name        = block_name        or self._block_name

        self._block_params = BlockParams( params )
        self.add_child_blocks(*child_blocks)

        self.__post_init__()

    def __post_init__(self): pass

    @property
    def _block_params_str(self) -> str:
        return str(self._block_params)

    @property
    def is_named(self) -> bool:
        return bool(self._block_name)

    @property
    def is_typed(self) -> bool:
        return bool(self._block_type)

    def output_value(self, attribute: str) -> str:
        """
            Used to reference any attribute values
        """
        if not self.is_named:
            raise Exception(f"Invalid mapping of output of unnamed resource: {repr(self)}")

        return f"${{{repr(self)}.{attribute}}}"

    def set_params(self, **kwargs: dict) -> None:
        for k,v in kwargs.items():
            self._block_params[k] = v

    def add_child_blocks(self, *blocks: list['TerraformBlockBase']):
        self._block_params.add_child_blocks( *blocks )

    def __repr__(self) -> str:
        rep = f"{self._block_category}"

        if self.is_typed:
            rep += f".{self._block_type}"

        if self.is_named:
            rep += f".{self._block_name}"

        return rep

    def __str__(self) -> str:
        out_str = f"{self._block_category}"

        if self.is_typed:
            out_str += f" \"{self._block_type}\""

        if self.is_named:
            out_str += f" \"{self._block_name}\""

        out_str += f" {self._block_params_str}"

        return out_str

class TerraformDocument():
    """
        Root Document for all terraform blocks to be attached to
    """

    _blocks: list

    def __init__(self) -> None:
        self._blocks = []

    def add_blocks(self, *blocks: list[TerraformBlockBase]):
        self._blocks.extend( blocks )

    def dumps(self) -> str:
        return '\n\n'.join([str(block) for block in self._blocks])

    def __str__(self) -> str:
        return self.dumps()