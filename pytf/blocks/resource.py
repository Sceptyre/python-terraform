from ..types import BaseTypedTerraformBlock

class TerraformResourceBlock(BaseTypedTerraformBlock):
    """
        Basic resource block
        resource "type" "name" {}
    """

    _block_category = "resource"
