#!/bin/sh -l

python /src/openai-summary/__main__.py --github_token "$1" --github_pr_number "$2" --open_ai_key "$3"