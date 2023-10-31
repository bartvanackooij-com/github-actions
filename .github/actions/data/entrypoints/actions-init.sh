#!/bin/sh -l

# todo: make these named arguments
python /src/action-init/__main__.py --github_token "$1" --github_pr_number "$2"