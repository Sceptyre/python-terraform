import py2terraform

doc = py2terraform.TerraformDocument()

provider = py2terraform.blocks.TerraformProviderBlock(
    block_type  = "aws",
    params      = {
        "region"    : "us-east-1"
    }
)

def create_instance(id: str):
    instance = py2terraform.blocks.TerraformResourceBlock(
        block_type = "aws_instance",
        block_name = f"my_instance_{id}",
        params     = {
            "ami"           : f"my-ami-{id}",
            "instance_type" : "t2.micro"
        }
    )
    instance_network_interface = py2terraform.types.TerraformBlockBase(
        block_category  = "network_interface",
        params          = {
            "network_interface_id"  : "my-interface-id",
            "device_index"          : 0
        }
    )

    instance.add_child_blocks(instance_network_interface)

    return instance

instances = [create_instance(x) for x in range(7)]

doc.add_blocks(
    provider,
    *instances
)

print(doc)