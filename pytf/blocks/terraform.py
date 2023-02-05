from ..types import BaseTerraformBlock

class TerraformTerraformBlock(BaseTerraformBlock):
    """
        Basic resource block
        terraform {}
    """

    _block_category = "terraform"
