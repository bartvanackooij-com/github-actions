import subprocess
import os
import argparse
import sys
from tools.message import GitHubMessage
import tools.message as message
import tools.pr_comment as pr_comment

def main():
    working_dir = os.getenv('wd_tf_infra')
    init_command = f"cd {working_dir} && terraform init"
    try:
        output = subprocess.check_output(init_command, shell=True, stderr=subprocess.STDOUT, text=True)
        print(output)
    except subprocess.CalledProcessError as e:
        error_message = f"Error running terraform init: {e.output}"
        print(error_message)
        sys.exit(1)

if __name__ == '__main__':
    main()