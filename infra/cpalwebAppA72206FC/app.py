#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cpalweb_app_a72206_fc.cpalweb_app_a72206_fc_stack import CpalwebAppA72206FcStack
from lib.deployment_environment_config import DeploymentEnvironmentConfig


AWS_ACCOUNT_ID = '818214664804'
AWS_REGION = 'us-east-2'
ECR_REPOSITORY_NAME = os.getenv("ECR_REPOSITORY_NAME", default='cpal-web')
ECR_REGISTRY_DOMAIN_NAME = os.getenv("ECR_REGISTRY_DOMAIN_NAME",
                                     default=f'{AWS_ACCOUNT_ID}.dkr.ecr.{AWS_REGION}.amazonaws.com')

# Define configuration based on the deployment environment.
# NOTE: The `deployment-environment` MUST be provided at runtime via CDK context.
# Example: `cdk synth --context deployment-environment=dev`

deployment_environments_configs: dict[str, DeploymentEnvironmentConfig] = {
    "dev": DeploymentEnvironmentConfig(
        site_domain_name = "dev.cpal.cascadiaquakes.org",
        ecr_image_uri = os.getenv("ECR_IMAGE_URI",
                           default=f'{ECR_REGISTRY_DOMAIN_NAME}/{ECR_REPOSITORY_NAME}:dev-latest')
    ),
    "prod": DeploymentEnvironmentConfig(
        site_domain_name = "cpal.cascadiaquakes.org",
        ecr_image_uri = os.getenv("ECR_IMAGE_URI",
                           default=f'{ECR_REGISTRY_DOMAIN_NAME}/{ECR_REPOSITORY_NAME}:prod-latest')
    )
}

app = cdk.App()
# Get runtime deployment environment from CDK context
deployment_environment = app.node.try_get_context("deployment-environment")

if not deployment_environment:
    raise SystemExit(
        "Error: deployment-environment context variable not set."
        " Use '--context deployment-environment=<name of deployment environment>' to set it."
    )

env_config = deployment_environments_configs.get(deployment_environment)

if not env_config:
    raise SystemExit(
        f"Error: No configuration found for deployment environment '{deployment_environment}'."
    )

# CDK uses the stack name as the prefix for nearly all resources created.
# Create a prefix for non-Prod Stacks to avoid naming conflicts between environments.
resource_prefix=f"{deployment_environment}-" if deployment_environment != "prod" else ""

CpalwebAppA72206FcStack(
    app,
    f"{resource_prefix}cpalwebAppA72206FC",
    env=cdk.Environment(account=AWS_ACCOUNT_ID, region=AWS_REGION),
    config=env_config
    )

app.synth()
