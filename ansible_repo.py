from github import Github
import json
import io
from time import gmtime, strftime

def get_latest_commit_sha(repo, branch, path):
    commits = repo.get_commits(sha=branch, path=path)
    page = commits.get_page(0)
    if len(page) > 0:
        return page[0].sha
    else:
        return None


def create_branch(repo):
    role_master_sha = repo.get_branch("master").commit.sha
    new_branch_name = "refs/heads/integration-" + strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    role_repo.create_git_ref(new_branch_name, role_master_sha)
    return new_branch_name


def save_back_to_json(data, file_name):
    print "saving data to " + file_name
    with io.open(file_name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False))


g = Github("2c09286ec369be4a550b558e8dfb94a7df1fbf8d")
ansible_org = g.get_organization("ansible")
ansible_repo = ansible_org.get_repo("ansible")
azure_org = g.get_organization("Azure")
role_repo = azure_org.get_repo("azure_modules")

role_repo.get_contents()