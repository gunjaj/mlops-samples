from aws_cdk import (
    Stack,
)
from aws_cdk import aws_eks as eks
from constructs import Construct


class ArgoStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, cluster: eks.Cluster, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Install Argo Workflows via Helm into the EKS cluster
        cluster.add_helm_chart(
            "ArgoWorkflowsChart",
            chart="argo-workflows",
            release="argo-workflows",
            repository="https://argoproj.github.io/argo-helm",
            namespace="argo-workflows",
            create_namespace=True,
            values={
                # Keep it simple for demo, auth mode 'server'
                "server": {
                    "extraArgs": ["--auth-mode=server"],
                },
            },
        )
