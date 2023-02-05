import pytf

doc = pytf.TerraformDocument()

provider = pytf.blocks.TerraformProviderBlock(
    block_type  = "aws",
    params      = {
        "region"    : "us-east-1"
    }
)

instance = pytf.blocks.TerraformResourceBlock(
    block_type = "aws_instance",
    block_name = "my_instance",
    params     = {
        "ami"           : "my-ami",
        "instance_type" : "t2.micro"
    }
)
instance_network_interface = pytf.types.BaseTerraformBlock(
    block_category  = "network_interface",
    params          = {
        "network_interface_id"  : "my-interface-id",
        "device_index"          : 0
    }
)

instance.add_child_blocks(instance_network_interface)

doc.add_blocks(
    provider,
    instance
)

print(doc)