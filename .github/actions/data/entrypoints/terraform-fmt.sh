#!/bin/sh -l

python /src/terraform-fmt/__main__.py --github_token "$1" --github_pr_number "$2"