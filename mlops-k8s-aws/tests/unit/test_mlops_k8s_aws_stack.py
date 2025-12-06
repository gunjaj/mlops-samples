import aws_cdk as core
import aws_cdk.assertions as assertions

from mlops_k8s_aws.mlops_k8s_aws_stack import MlopsK8SAwsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in mlops_k8s_aws/mlops_k8s_aws_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MlopsK8SAwsStack(app, "mlops-k8s-aws")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
