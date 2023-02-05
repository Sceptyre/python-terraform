from ..types import TerraformBlockBase

class TerraformTerraformBlock(TerraformBlockBase):
    """
        Basic resource block
        terraform {}
    """

    _block_category = "terraform"
