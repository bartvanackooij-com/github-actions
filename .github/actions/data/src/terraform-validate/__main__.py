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
    pr_number = args.github_pr_number
    github_token = args.github_token

    repository = os.getenv('GITHUB_REPOSITORY')
    working_dir = os.getenv('wd_tf_infra')
    
    fmt_command = f"cd {working_dir} && terraform validate -json"

    try:
        output = subprocess.check_output(fmt_command, shell=True, stderr=subprocess.STDOUT, text=True)
        pr_comment.write(github_token, repository, pr_number, f"<details><summary><b>Terraform validate:</b> :+1:</summary>All files are valid.</details>\n")
    except subprocess.CalledProcessError as e:
        data = json.loads(e.output)
        errors = data["diagnostics"]
        numm_errors = len(errors)
        output = f"<details open><summary><b>Terraform validate: </b>{''.join([':skull:' for _ in range(numm_errors)])}</summary>\n\n"
        
        for i, error in enumerate(errors, start=1):
            summary = error["summary"]
            detail = error["detail"]
            filename = error["range"]["filename"]
            line = error["range"]["start"]["line"]
            
            file_path = os.path.normpath(os.path.join(working_dir, filename))
            url = f"{os.getenv('GITHUB_SERVER_URL')}/{os.getenv('GITHUB_REPOSITORY')}/blob/{os.getenv('GITHUB_SHA')}/{file_path}#L{line}"
            output += f"{1}. {summary}\n{detail}\n[{file_path}]({url})\n\n"

            msg = GitHubMessage(type='error', title='Terraform validate failed', file=file_path, text='File is not valid, breaking the pipeline').format_message()
            message.printmsg(msg)

        output += "</details>"
        pr_comment.write(github_token, repository, pr_number, output)
        sys.exit(1)

if __name__ == '__main__':
    main()