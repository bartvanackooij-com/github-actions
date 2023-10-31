# Terraform GitHub Actions

## Description

A collection of re-usable GitHub actions combined in a GitHub workflow for Terraform projects using Azure. Besides having a working ci/cd pipeline to use in different projects. The main goal of this project is to set up a blueprint which is easy to understand, edit, expand and to use as a base for online tutorials and blogs. 

The idea behind this workflow is optimizing your [GitOps](https://about.gitlab.com/topics/gitops/) workflow. If all changes related to the infrastructure is done through merge requests, I'd like to have all the information available in the pull request. This workflow will show you the output of terraform formatting, the plan, summary of the costs and a short description of the pull request. (And as a little bonus a short AI generated poem).

![](/img/workflow.gif)


## Table of Contents

- [Usage](#usage)
- [Workflow](#workflow)
- [Example](#example)
- [License](#license)

## Usage

1. Either fork or use this repository.
2. Set the following secrets in your repository (/settings/secrets/actions): 

| Secret Name           | Description                  |
|-----------------------|------------------------------|
| AZURE_CLIENT_ID       | Your Azure Client ID.        |
| AZURE_SUBSCRIPTION_ID | Your Azure Subscribtion ID.  |
| AZURE_TENANT_ID       | Your Azure Tenant ID.        |
| GH_PAT                | Your GitHub PAT token.       |
| INFRACOST_API_KEY     | Your Infracost API key.      |
| OPEN_AI_KEY           | Your OpenAI key.             |


## Workflow

There are 2 workflows in this repository. 

### pr-checks.yml
This workflow will be triggered when a pull request is opened, synced, re-opened or changed. It will execute the following steps in order to create a comment on your pull request which will provide you with all the information you need to determine whether or not you can merge it. 

- It will checkout the actions in this repository
- It will build the docker images to run the actions
- It will checkout the repository which holds the terraform code. 
- It will: 
    - check terraform formatting.
    - initialise terraform.
    - validate the terraform code.
    - show the changes of the terraform plan.
    - determine the costs of the change.
    - provide a brief summary of the changes using open AI.
    - upload the terraform plan. 

You can set this as a pre-requisite in GitHub that these must succeed in order to merge your pull request. 

### merge.yml
This workflow will only be triggered when a pull request is merged and it will do the actual deploying of your code to Azure. 

- It will checkout the actions in this repository
- It will build the docker images to run the actions
- It will checkout the repository which holds the terraform code. 
- It will: 
    - initialise terraform.
    - validate the terraform code.
    - execute terraform plan.
    - apply the changes from the terraform plan. 
    - update the comment on the pull request with the apply summary.

## Example

Below is an example of both workflows and how they can be configured. Create these files in your `.github/workflows` folder.

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

