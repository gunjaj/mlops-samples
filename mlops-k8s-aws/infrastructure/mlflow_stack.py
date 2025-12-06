from aws_cdk import (
    Stack,
    aws_eks as eks,
)
from constructs import Construct


class MlflowStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, cluster: eks.Cluster, bucket, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        namespace = "mlflow"

        ns = {
            "apiVersion": "v1",
            "kind": "Namespace",
            "metadata": {
            "name": namespace,
            "labels": {
                "app": "mlflow-namespace" 
            },
            },
        }

        deployment = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": "mlflow", "namespace": namespace},
            "spec": {
                "replicas": 1,
                "selector": {"matchLabels": {"app": "mlflow"}},
                "template": {
                    "metadata": {"labels": {"app": "mlflow"}},
                    "spec": {
                        "containers": [
                            {
                                "name": "mlflow",
                                "image": "ghcr.io/mlflow/mlflow:latest",
                                "ports": [{"containerPort": 5000}],
                                "command": ["mlflow", "server"],
                                "args": [
                                    "--host", "0.0.0.0",
                                    "--port", "5000",
                                    "--backend-store-uri", "sqlite:///mlflow.db",
                                    "--default-artifact-root", "/mlruns",
                                ],
                                "volumeMounts": [
                                    {
                                        "name": "mlflow-artifacts",
                                        "mountPath": "/mlruns",
                                    }
                                ],
                            }
                        ],
                        "volumes": [
                            {
                                "name": "mlflow-artifacts",
                                "emptyDir": {},
                            }
                        ],
                    },
                },
            },
        }

        service = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {"name": "mlflow", "namespace": namespace},
            "spec": {
                "selector": {"app": "mlflow"},
                "ports": [
                    {
                        "protocol": "TCP",
                        "port": 5000,
                        "targetPort": 5000,
                    }
                ],
                "type": "ClusterIP",
            },
        }

        # All MLflow K8s resources in one manifest
        cluster.add_manifest("MlflowResources", ns, deployment, service)
