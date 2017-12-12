from github import Github
import json
import io
import os
import shutil
from time import gmtime, strftime
from git import Repo

ansible_repo_path = "/tmp/ansible_repo"
azure_repo_path = "/tmp/azure_repo"
log_file_path = "./commit_history.json"
path_mapping_file_path = "./folder_mapping.json"

def get_latest_commit_sha(repo, branch, path):
    commits = repo.get_commits(sha=branch, path=path)
    page = commits.get_page(0)
    if len(page) > 0:
        return page[0].sha
    else:
        return None


def has_new_content(repo, branch_name, log_file):
    commit_history = json.load(open(log_file))
    for path, sha in commit_history.iteritems():
        new_sha = get_latest_commit_sha(repo, branch_name, path)
        if sha != new_sha:
            return True
    return False


def ansible_repo_has_new_content():
    g = Github("2c09286ec369be4a550b558e8dfb94a7df1fbf8d")
    ansible_org = g.get_organization("ansible")
    remote_ansible_repo = ansible_org.get_repo("ansible")
    return has_new_content(remote_ansible_repo, "devel", log_file_path)


def create_branch(repo):
    role_master_sha = repo.get_branch("master").commit.sha
    new_branch_name = "refs/heads/integration-" + strftime("%Y-%m-%d-%H-%M-%S", gmtime())
    repo.create_git_ref(new_branch_name, role_master_sha)
    return new_branch_name


def save_back_to_json(data, file_name):
    print "saving data to " + file_name
    with io.open(file_name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False))


def create_clean_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)


def clone_repos():
    print "Cloning repos to local..."
    create_clean_dir(ansible_repo_path)
    create_clean_dir(azure_repo_path)

    azure_repo = Repo()
    azure_repo.clone_from("https://github.com/Azure/azure_modules.git", azure_repo_path)

    ansible_repo = Repo()
    ansible_repo.clone_from("https://github.com/ansible/ansible.git", ansible_repo_path)


def copy(path):
    full_path = os.path.join(ansible_repo_path, path)
    if os.path.isdir(full_path):
        copy_folder(path)
    else:
        copy_file(path)


def get_joined_path(path):
    path_map = json.load(open(path_mapping_file_path))
    azure_path = path_map[path]

    src = os.path.join(ansible_repo_path, path)
    dest = os.path.join(azure_repo_path, azure_path)

    return src, dest


def copy_file(path):
    print "Copying file " + path
    src, dest = get_joined_path(path)
    shutil.copy(src, dest)


def copy_folder(path):
    print "Copying folder " + path
    if "test/integration/targets" in path:
        copy_folder_specially(path)
    else:
        copy_folder_normally(path)


def copy_folder_normally(path):
    src, dest = get_joined_path(path)
    shutil.rmtree(dest)
    shutil.copytree(src, dest)


def copy_folder_specially(path):
    src, dest = get_joined_path(path)
    shutil.rmtree(dest)
    for dir_name in os.listdir(src):
        src_dir_path = os.path.join(src, dir_name)
        dest_dir_path = os.path.join(dest, dir_name)
        if os.path.isdir(src_dir_path) and "azure_rm_" in dir_name:
            shutil.copytree(src_dir_path, dest_dir_path)


# azure_org = g.get_organization("Azure")
# role_repo = azure_org.get_repo("azure_modules")

def check_out_new_branch():
    print "ddddd"


def copy_changed_files():
    g = Github("2c09286ec369be4a550b558e8dfb94a7df1fbf8d")
    ansible_org = g.get_organization("ansible")
    remote_ansible_repo = ansible_org.get_repo("ansible")
    commit_history = json.load(open(log_file_path))

    changed = False
    for path, sha in commit_history.iteritems():
        new_sha = get_latest_commit_sha(remote_ansible_repo, "devel", path)
        if sha != new_sha:
            copy(path)
            changed = True
            commit_history[path]=new_sha

    if changed:
        save_back_to_json(commit_history, log_file_path)


def push_changes_to_remote():
    print "dddddd"


def send_pull_request():
    print "dddd"


def migrate_contents():
    check_out_new_branch()
    copy_changed_files()
    push_changes_to_remote()
    send_pull_request()


def main():
    print "Starting..."

    if not ansible_repo_has_new_content():
        print "No new content. Exiting..."
        return
    else:
        print "Migrating content from Ansible repo to Azure modules repo..."

    clone_repos()
    migrate_contents()


if __name__ == "__main__":
    main()