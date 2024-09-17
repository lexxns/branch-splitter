class Change:
    def __init__(self, commit_hash, message, diff):
        self.commit_hash = commit_hash
        self.message = message
        self.diff = diff


class ChangeManager:
    def __init__(self, git_repo):
        self.git_repo = git_repo

    def get_all_changes(self):
        pass
        # Get all changes between current and main branch
        # Return list of Change objects

    def apply_change(self, change, branch):
        pass
        # Apply a change to a specific branch
