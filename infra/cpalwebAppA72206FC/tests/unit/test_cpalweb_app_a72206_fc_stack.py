import aws_cdk as core
import aws_cdk.assertions as assertions

from cpalweb_app_a72206_fc.cpalweb_app_a72206_fc_stack import CpalwebAppA72206FcStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cpalweb_app_a72206_fc/cpalweb_app_a72206_fc_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CpalwebAppA72206FcStack(app, "cpalweb-app-a72206-fc")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
