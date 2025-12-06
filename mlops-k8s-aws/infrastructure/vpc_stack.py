from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    Tags,
)
from constructs import Construct

class VpcStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # EKS-ready VPC: 2 AZs, 1 NAT Gateway
        self.vpc = ec2.Vpc(
            self,
            "EKSVpc",
            max_azs=2,          # 2 AZs is enough for a demo cluster
            nat_gateways=1,     # key cost saving – default would be 2
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    name="PrivateSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                ),
            ],
        )

        # Helpful for Cost Explorer
        Tags.of(self.vpc).add("project", "mlops-k8s-aws")
        Tags.of(self.vpc).add("environment", "dev")
