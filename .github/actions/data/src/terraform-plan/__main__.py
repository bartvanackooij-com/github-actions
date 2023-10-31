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
    comment_pr = os.getenv('update_comment')

    plan_command = f"cd {working_dir} && terraform plan -no-color -out=tfplan"
    show_command = f"cd {working_dir} && terraform show tfplan -no-color"

    try:
        subprocess.check_output(plan_command, shell=True, stderr=subprocess.STDOUT, text=True)
        show_output = subprocess.check_output(show_command, shell=True, stderr=subprocess.STDOUT, text=True)
        summary = show_output.split("\n")[-2]
        if comment_pr:
            pr_comment.write(github_token, repository, pr_number, f"<details><summary><b>Terraform plan:</b> :+1: <i>{summary}</i></summary>\n\n```{show_output}\n```\n</details>\n")
    except subprocess.CalledProcessError as e:
        data_objects = e.output.strip().split("\n")
        data = json.loads(data_objects[1])
        print("Error running 'terraform plan':", data["diagnostic"]["detail"])
        if comment_pr:
            pr_comment.write(github_token, repository, pr_number, f"<details open><summary><b>Terraform plan:</b> :skull:</summary>\n\n{data['diagnostic']['summary']}:\n```{data['diagnostic']['detail']}\n```\n\n</details>\n")
        sys.exit(1)

if __name__ == '__main__':
    main()