from aws_cdk import (
    Stack,
    aws_eks as eks,
    aws_ec2 as ec2,
    aws_iam as iam,
    CfnOutput,
)
from constructs import Construct
from aws_cdk.lambda_layer_kubectl_v34 import KubectlV34Layer


class EksClusterStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # EKS control plane cluster
        self.cluster = eks.Cluster(
            self,
            "MlopsEksCluster",
            version=eks.KubernetesVersion.V1_34,
            vpc=vpc,
            default_capacity=0,  # Add spot nodegroup
            endpoint_access=eks.EndpointAccess.PUBLIC,
            kubectl_layer=KubectlV34Layer(self, "kubectl")
        )
        dev_role = iam.Role.from_role_arn(
            self,
            "DevProfileRole",
            "arn:aws:iam::999999999999:role/AWSReservedSSO_AdministratorAccess_bb61a76484f97beb",
        )
        self.cluster.aws_auth.add_masters_role(dev_role)
        # Spot worker nodes
        self.cluster.add_nodegroup_capacity(
            "SpotNodeGroup",
            desired_size=1,
            min_size=1,
            max_size=2,
            instance_types=[ec2.InstanceType("t3.medium")],
            ami_type=eks.NodegroupAmiType.AL2023_X86_64_STANDARD,
            capacity_type=eks.CapacityType.SPOT,
        )
    
        # Output cluster name for kubectl config
        CfnOutput(
            self,
            "ClusterName",
            value=self.cluster.cluster_name,
            export_name="MlopsEksClusterName",
        )

        # Output kubectl configuration command
        CfnOutput(
            self,
            "KubectlConfigCommand",
            value=f"aws eks update-kubeconfig --region {self.region} --name {self.cluster.cluster_name}",
            description="Run this command to configure kubectl",
        )
