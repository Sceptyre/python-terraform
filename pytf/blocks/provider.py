from ..types import BaseTypedTerraformBlock

class TerraformProviderBlock(BaseTypedTerraformBlock):
    """
        Basic provider block
        provider "type" {}
    """

    _block_category = "provider"
