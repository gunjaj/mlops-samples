#!/usr/bin/env python3
import aws_cdk as cdk

from infrastructure.vpc_stack import VpcStack
from infrastructure.eks_cluster_stack import EksClusterStack
from infrastructure.argo_stack import ArgoStack
from infrastructure.bucket_stack import BucketStack
from infrastructure.mlflow_stack import MlflowStack

app = cdk.App()

vpc_stack = VpcStack(app, "VpcStack")
eks_stack = EksClusterStack(
    app,
    "EksClusterStack",
    vpc=vpc_stack.vpc,
)

bucket_stack = BucketStack(app, "BucketStack")
mlflow_stack = MlflowStack(
    app,
    "MlflowStack",
    cluster=eks_stack.cluster,
    bucket=bucket_stack.mlops_bucket,
)
mlflow_stack.add_dependency(eks_stack)
argo_stack = ArgoStack(
    app,
    "ArgoStack",
    cluster=eks_stack.cluster,
)

app.synth()
