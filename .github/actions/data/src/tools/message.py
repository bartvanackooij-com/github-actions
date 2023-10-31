import sys
import os

# class and function to print annotations to GitHub Actions
class GitHubMessage:
    def __init__(self, type='', title='', file='', text=''):
        self.type = type
        self.title = title
        self.file = file
        self.text = text

    def format_message(self):
        formatted_message = f"::{self.type}"
        parameters = []
        if self.title:
            parameters.append(f"title={self.title}")
        if self.file:
            parameters.append(f"file={self.file}")
        if parameters:
            formatted_message += f" {','.join(parameters)}"
        formatted_message += f"::{self.text}"
        return formatted_message

def printmsg(message):
    sys.stdout.write(message + os.linesep)