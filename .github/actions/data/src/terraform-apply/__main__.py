import subprocess
import os
import argparse
import sys
from tools.message import GitHubMessage
import tools.message as message
import tools.pr_comment as pr_comment

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--github_token', required=True, help='Your Github Token')
    parser.add_argument('--github_pr_number', required=True, help='Your Github PR ID')
    args = parser.parse_args()
    pr_number = args.github_pr_number
    github_token = args.github_token

    repository = os.getenv('GITHUB_REPOSITORY')
    working_dir = os.getenv('wd_tf_infra')
    
    apply_command = f"cd {working_dir} && terraform apply -no-color -auto-approve tfplan"

    try:
        result = subprocess.run(apply_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            output = result.stdout
            pr_comment.write(github_token, repository, pr_number, f"<details><summary><b>Terraform apply:</b> :+1:</summary>\n\n```{output}\n```\n</details>\n")
        else:
            error_message = result.stderr
            print(f"Error running Terraform apply: {error_message}")
            sys.exit(1)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        sys.exit(1)

if __name__ == '__main__':
    main()
