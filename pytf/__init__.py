"""
    Basic module to generate Terraform configurations using python code
"""
from .types    import BaseTerraformBlock
from .          import blocks, types

class TerraformDocument():
    """
        Root Document for all terraform blocks to be attached to
    """

    _blocks: list

    def __init__(self) -> None:
        self._blocks = []

    def add_blocks(self, *blocks: list[BaseTerraformBlock]):
        self._blocks.extend( blocks )

    def dumps(self) -> str:
        return '\n\n'.join([str(block) for block in self._blocks])

    def __str__(self) -> str:
        return self.dumps()