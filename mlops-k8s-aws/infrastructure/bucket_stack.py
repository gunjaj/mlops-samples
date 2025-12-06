from aws_cdk import (
    Stack,
    aws_s3 as s3,
    RemovalPolicy,
)
from constructs import Construct


class BucketStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Main bucket for MLflow artifacts + datasets
        self.mlops_bucket = s3.Bucket(
            self,
            "MlopsBucket",
            versioned=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,  # remove objects on destroy (for demo)
        )
