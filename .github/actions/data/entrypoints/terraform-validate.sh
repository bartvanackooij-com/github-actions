#!/bin/sh -l

python /src/terraform-validate/__main__.py --github_token "$1" --github_pr_number "$2"