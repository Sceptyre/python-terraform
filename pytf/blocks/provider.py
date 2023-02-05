from ..types import TerraformBlockBase

class TerraformProviderBlock(TerraformBlockBase):
    """
        Basic provider block
        provider "type" {}
    """

    _block_category = "provider"
