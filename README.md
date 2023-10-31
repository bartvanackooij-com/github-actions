# Terraform GitHub Actions

## Description

Terraform GitHub Actions is a collection of re-usable GitHub Actions bundled into a GitHub workflow designed for Terraform projects using Azure. The primary goal of this project is to create a versatile CI/CD pipeline that can be used across different projects. Additionally, it serves as a blueprint for easy understanding, customization, and expansion, making it suitable as a foundation for online tutorials and blogs.

The core idea behind this workflow is to optimize your [GitOps](https://about.gitlab.com/topics/gitops/) process. By ensuring that all infrastructure-related changes are made through merge requests, this workflow provides comprehensive information within the pull request, including Terraform formatting, the plan, cost summary, and a description of the changes, topped with a short AI-generated poem for a touch of whimsy.

![Workflow](/img/workflow.gif)

## Table of Contents

- [Usage](#usage)
- [Workflow](#workflow)
- [Examples](#examples)

## Usage

### Prerequisites

Before using these GitHub Actions, make sure you have the following in place:
- A GitHub account
- An Azure account
- Terraform installed

### Setting Up Secrets

To use these actions, configure the following secrets in your repository settings (Settings > Secrets > New Repository Secret):

| Secret Name           | Description                  |
|-----------------------|------------------------------|
| AZURE_CLIENT_ID       | Your Azure Client ID.        |
| AZURE_SUBSCRIPTION_ID | Your Azure Subscription ID.  |
| AZURE_TENANT_ID       | Your Azure Tenant ID.        |
| GH_PAT                | Your GitHub PAT token.       |
| INFRACOST_API_KEY     | Your Infracost API key.      |
| OPEN_AI_KEY           | Your OpenAI key.             |

## Workflow

There are two workflows in this repository:

### pr-checks.yml

This workflow is triggered when a pull request is opened, synced, re-opened, or changed. It provides you with essential information to determine whether you can merge the pull request. It includes the following steps:

- Checkout the actions in this repository
- Build the Docker images to run the actions
- Checkout the repository containing the Terraform code
- Execute the following tasks:
    - Check Terraform formatting
    - Initialize Terraform
    - Validate the Terraform code
    - Display the changes of the Terraform plan
    - Determine the costs of the changes
    - Provide a brief summary of the changes using OpenAI
    - Upload the Terraform plan

You can set this workflow as a prerequisite in GitHub to ensure that these tasks must succeed for the pull request to be merged.

### merge.yml

This workflow is triggered when a pull request is merged and handles the actual deployment of your code to Azure. It includes the following steps:

- Checkout the actions in this repository
- Build the Docker images to run the actions
- Checkout the repository containing the Terraform code
- Execute the following tasks:
    - Initialize Terraform
    - Validate the Terraform code
    - Execute the Terraform plan
    - Apply the changes from the Terraform plan
    - Update the comment on the pull request with the apply summary.

## Examples

For detailed examples of how to configure and use these workflows, see the provided configuration files:

### pr-check.yml
```yaml
name: pr-check
on:
  pull_request:
    branches:
      - master
    types: [opened, synchronize, reopened, edited]

permissions:
      id-token: write
      contents: read
      pull-requests: write

jobs:
  terraform-pr-check:
    # you can set your fork or own repository here.
    uses: bartvanackooij-com/github-actions/.github/workflows/pr-checks.yml@master
    with:
      # you will need to set the directory your terraform code resides.
      working_directory: "terraform/environments/infra"
      github_pr_number: ${{ github.event.number }}
    secrets:
      inherit
```

### merge.yml
```yaml
name: merge
on:
  pull_request:
    branches: 
      - master
    types: [closed]

permissions:
      id-token: write
      contents: read
      pull-requests: write

jobs:
  merge:
    # to make sure it runs only when a PR is merged:
    if: github.event_name == 'pull_request' && github.event.action == 'closed' && github.event.pull_request.merged == true
    # you can set your fork or own repository here.
    uses: bartvanackooij-com/github-actions/.github/workflows/merge.yml@master
    with:
      # you will need to set the directory your terraform code resides.
      working_directory: "terraform/environments/infra"
      github_pr_number: ${{ github.event.number }}
    secrets:
      inherit
```

