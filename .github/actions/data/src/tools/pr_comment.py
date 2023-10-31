import sys
import os

from github import Github

init_text = "### Barts PR Bot :rocket:\n"

def write(github_token, repository, pr_number, text):
    g = Github(github_token)
    repo = g.get_repo(repository)
    pull_request = repo.get_pull(int(pr_number))
    comments = pull_request.get_issue_comments()
    for comment in comments:
        if comment.user.login == "github-actions[bot]":
            bot_comment = comment
            break
    body = bot_comment.body + text
    bot_comment.edit(body=body)

def new(github_token, repository, pr_number):
    g = Github(github_token)
    repo = g.get_repo(repository)
    pull_request = repo.get_pull(int(pr_number))
    comments = pull_request.get_issue_comments()
    for comment in comments:
        if comment.user.login == "github-actions[bot]":
            comment.delete()
    pull_request.create_issue_comment(init_text)


