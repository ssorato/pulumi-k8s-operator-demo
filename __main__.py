"""A Python Pulumi program"""

import pulumi
import pulumi
from pulumi_kubernetes import core, apiextensions

# Get the Pulumi API token.
pulumi_config = pulumi.Config()
pulumi_azure_storage_key = pulumi_config.require_secret("pulumiAzureStorageKey")
pulumi_azure_storage_account = pulumi_config.require_secret("pulumiAzureStorageAccount")
#pulumi_github_account_token = pulumi_config.require_secret("pulumiGitHubAccountToken")
pulumi_stack_commit = pulumi_config.require("stackCommit");
pulumi_stack_passphrase = pulumi_config.require_secret("pulumiStackPassphrase")

# Create the Azure Blog credentuals as a Kubernetes Secret.
azure_storage_key = core.v1.Secret("azurestoragekey", string_data={ "storage_key": pulumi_azure_storage_key })
azure_storage_account = core.v1.Secret("azurestorageaccount", string_data={ "storage_account": pulumi_azure_storage_account })
#github_account_token = core.v1.Secret("githubaccounttoken", string_data={ "account_token": pulumi_github_account_token })
stack_passphrase = core.v1.Secret("stackpassphrase", string_data={ "stack_passphrase": pulumi_stack_passphrase })

# Create an NGINX deployment in-cluster.
my_stack = apiextensions.CustomResource("stack-demo",
  api_version="pulumi.com/v1",
  kind="Stack",
  spec={
    "envRefs": {
        "AZURE_STORAGE_KEY": {
            "type": "Secret",
            "secret": {
                "name": azure_storage_key.metadata.name,
                "key": "storage_key",
                "namespace": "default"
            }
        },
        "AZURE_STORAGE_ACCOUNT": {
            "type": "Secret",
            "secret": {
                "name": azure_storage_account.metadata.name,
                "key": "storage_account",
                "namespace": "default"
            }
        },
        "PULUMI_CONFIG_PASSPHRASE": {
            "type": "Secret",
            "secret": {
                "name": stack_passphrase.metadata.name,
                "key": "stack_passphrase",
                "namespace": "default"
            }
        }
    },
    "backend": "azblob://pulumi",
    "stack": "dev",
    "projectRepo": "https://github.com/ssorato/pulumi-k8s-nginx-demo",
    # "gitAuth": {
    #   "accessToken": {
    #     "type": "Secret",
    #     "secret": {
    #       "name": github_account_token.metadata.name,
    #       "key": "account_token"
    #     }
    #   }
    # },
    "commit": pulumi_stack_commit,
    "destroyOnFinalize": True
  }
)