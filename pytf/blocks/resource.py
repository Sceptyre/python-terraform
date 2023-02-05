from ..types import TerraformBlockBase

class TerraformResourceBlock(TerraformBlockBase):
    """
        Basic resource block
        resource "type" "name" {}
    """

    _block_category = "resource"
