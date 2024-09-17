import os
from git import Repo, GitCommandError
from git.exc import InvalidGitRepositoryError, NoSuchPathError


class GitRepo:
    def __init__(self, repo_path):
        try:
            self.repo = Repo(repo_path)
        except (InvalidGitRepositoryError, NoSuchPathError):
            raise ValueError(f"The path {repo_path} is not a valid Git repository.")

    def get_current_branch(self):
        return self.repo.active_branch.name

    def create_branch(self, branch_name):
        try:
            self.repo.git.checkout('-b', branch_name)
            return True
        except GitCommandError as e:
            print(f"Error creating branch: {e}")
            return False

    def get_changes(self, source_branch, target_branch):
        try:
            # Get the common ancestor of the two branches
            common_ancestor = self.repo.merge_base(source_branch, target_branch)[0]

            # Get the differences between the common ancestor and the source branch
            diffs = self.repo.git.diff(common_ancestor, source_branch, name_only=True).split('\n')

            changes = []
            for file_path in diffs:
                if file_path:  # Ignore empty strings
                    commit = next(self.repo.iter_commits(f"{common_ancestor}..{source_branch}", paths=file_path))
                    changes.append({
                        'file': file_path,
                        'commit_hash': commit.hexsha,
                        'message': commit.message.strip(),
                        'diff': self.repo.git.diff(f"{common_ancestor}:{file_path}", f"{source_branch}:{file_path}")
                    })
            return changes
        except GitCommandError as e:
            print(f"Error getting changes: {e}")
            return []

    def apply_change(self, change, branch):
        current_branch = self.get_current_branch()
        try:
            self.repo.git.checkout(branch)
            file_path = os.path.join(self.repo.working_dir, change['file'])
            with open(file_path, 'w') as file:
                file.write(self.repo.git.show(f"{change['commit_hash']}:{change['file']}"))
            self.repo.git.add(change['file'])

            # Check if there are changes to commit
            if self.repo.is_dirty():
                self.repo.git.commit('-m', f"Apply change: {change['message']}")
                return True
            else:
                print("No changes to commit")
                return False
        except GitCommandError as e:
            print(f"Error applying change: {e}")
            return False
        finally:
            self.repo.git.checkout(current_branch)

    def push_branch(self, branch_name):
        try:
            self.repo.git.push('origin', branch_name)
            return True
        except GitCommandError as e:
            print(f"Error pushing branch: {e}")
            return False

    def branch_exists(self, branch_name):
        return branch_name in [ref.name for ref in self.repo.refs]