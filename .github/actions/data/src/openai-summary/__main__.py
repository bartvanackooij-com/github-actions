import openai
import subprocess
import os
import sys
import json
import argparse
import tools.message as message
import tools.pr_comment as pr_comment

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--github_token', required=True, help='Your Github Token')
    parser.add_argument('--github_pr_number', required=True, help='Your Github PR ID')
    parser.add_argument('--open_ai_key', required=True, help='Your Github PR ID')
    args = parser.parse_args()
    github_token = args.github_token
    pr_number = args.github_pr_number
    open_ai_key = args.open_ai_key

    working_dir = os.getenv('wd_tf_infra')
    repository = os.getenv('GITHUB_REPOSITORY')    

    openai.api_key = open_ai_key

    show_command = f"cd {working_dir} && terraform show tfplan -no-color"

    try:
        show_output = subprocess.check_output(show_command, shell=True, stderr=subprocess.STDOUT, text=True)
        summary = show_output.split("\n")[-2]
    except subprocess.CalledProcessError as e:
        error_message = f"Error running Open AI summary step: {e.output}"
        print(error_message)
        sys.exit(1)
    print(summary)
    ai_summary = openai.Completion.create(
        engine="text-davinci-003",
        prompt=(f"Explain the change in the terraform plan in 1 sentences. Be specific, serious and professional.\n\n"
                f"Terraform Plan summary:\n{show_output}"),
        max_tokens=400,
    )
    ai_poem = openai.Completion.create(
        engine="text-davinci-003",
        prompt=(f"Describe the change in 3-4 sentences, in a poem, and make it rhyme. Make it start and end with :rose: And after each line, add a newline. \n\n"
                f"Terraform Plan summary:\n{show_output}"),
        max_tokens=1000,
    )
    pr_comment.write(github_token, repository, pr_number, f"<details><summary><b>Open AI summary:</b> :+1: <i>{ai_summary['choices'][0]['text']}</i></summary>\n\n<i>\n{ai_poem['choices'][0]['text']}</i>\n\n</details>\n")

if __name__ == '__main__':
    main()