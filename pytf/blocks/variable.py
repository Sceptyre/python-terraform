from ..types import TerraformBlockBase

class TerraformVariableBlock(TerraformBlockBase):
    _block_category = "variable"

    def __repr__(self) -> str:
        return f"var.{self._block_name}"
