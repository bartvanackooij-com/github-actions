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
    files = []

    fmt_command = "terraform fmt -check -recursive"
    try:
        subprocess.check_output(fmt_command, shell=True, stderr=subprocess.STDOUT, text=True)
        pr_comment.write(github_token, repository, pr_number, f"<details><summary><b>Terraform fmt:</b> :+1:</summary>All files are formatted correctly.</details>\n")
    except subprocess.CalledProcessError as e:
        if e.returncode == 3:
            error_output = e.output
            error_lines = error_output.split("\n")
            for line in error_lines:
                if line.endswith(".tf"):
                    line.replace("$terraform", "")
                    print(line)
                    msg = GitHubMessage(type='notice', title='Terraform fmt', file=line, text='File needs formatting, Please run `terrform fmt -recursive`').format_message()
                    message.printmsg(msg)
                    files.append(line)
            formatted_files = "\n".join(files)
            pr_comment.write(github_token, repository, pr_number, f"<details open><summary><b>Terraform fmt:</b> :-1:</summary> \n\n_These files need formatting:_\n\n```\n{formatted_files}\n# Please run:\n$ terraform fmt -recursive\n```\n</details>")
        else:
            error_message = f"Error running Terraform fmt command: {e.output}"
            print(error_message)
            sys.exit(1)

if __name__ == '__main__':
    main()