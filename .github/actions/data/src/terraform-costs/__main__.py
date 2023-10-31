import subprocess
import os
import argparse
import sys
from tools.message import GitHubMessage
import tools.message as message
import tools.pr_comment as pr_comment
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--github_token', required=True, help='Your Github Token')
    parser.add_argument('--github_pr_number', required=True, help='Your Github PR ID')
    args = parser.parse_args()
    github_token = args.github_token
    pr_number = args.github_pr_number

    repository = os.getenv('GITHUB_REPOSITORY')
    working_dir = os.getenv('wd_tf_infra')

    summary_line = "Infracost estimate: "
    summary = ""
    output = ""

    convert_command = f"cd {working_dir} && terraform show -json tfplan > plan.json"
    calculate_command = f"cd {working_dir} && infracost diff --path plan.json --out-file costs.txt"

    try:
        subprocess.check_output(convert_command, shell=True, stderr=subprocess.STDOUT, text=True)
        subprocess.check_output(calculate_command, shell=True, stderr=subprocess.STDOUT, text=True)
        with open(f"{working_dir}/costs.txt", "r") as file:
            output = file.read()
        with open(f"{working_dir}/costs.txt", "r") as file:
            for line in file:
                if line.startswith(summary_line):
                    summary = line.replace(summary_line, "")
                    break
        pr_comment.write(github_token, repository, pr_number, f"<details><summary><b>Terraform costs:</b> :+1: <i>Costs: {summary} </i> :moneybag:</summary>\n\n```{output}\n```\n</details>\n")
    except subprocess.CalledProcessError as e:
        error_message = f"<details><summary><b>Terraform costs:</b> :-1: <i> Error generating cost estimation :moneybag: </summary>\n\n```{e.output}\n```\n</details>\n"
        print(error_message)
        sys.exit(1)
        sys.exit(1)

if __name__ == '__main__':
    main()