from branch_splitter.git_repo import GitRepo


class BranchManager:
    def __init__(self, git_repo: GitRepo):
        self.git_repo = git_repo
        self.branches = []

    def create_branch(self, branch_name: str) -> bool:
        """
        Create a new branch and add it to the list of managed branches.

        :param branch_name: Name of the branch to create
        :return: True if branch was created successfully, False otherwise
        """
        if self.git_repo.create_branch(branch_name):
            self.branches.append(branch_name)
            return True
        return False

    def get_branches(self) -> list:
        """
        Get the list of managed branches.

        :return: List of branch names
        """
        return self.branches

    def push_branches(self) -> dict:
        """
        Push all managed branches to the remote repository.

        :return: Dictionary with branch names as keys and push success status as values
        """
        results = {}
        for branch in self.branches:
            results[branch] = self.git_repo.push_branch(branch)
        return results

    def apply_change_to_branches(self, change: dict, target_branches: list) -> dict:
        """
        Apply a specific change to multiple target branches.

        :param change: Dictionary containing change details
        :param target_branches: List of branch names to apply the change to
        :return: Dictionary with branch names as keys and change application success status as values
        """
        results = {}
        for branch in target_branches:
            if branch in self.branches:
                results[branch] = self.git_repo.apply_change(change, branch)
            else:
                results[branch] = False
                print(f"Branch {branch} is not managed by this BranchManager.")
        return results

    def remove_branch(self, branch_name: str) -> bool:
        """
        Remove a branch from the list of managed branches.

        :param branch_name: Name of the branch to remove
        :return: True if branch was removed successfully, False if branch was not in the list
        """
        if branch_name in self.branches:
            self.branches.remove(branch_name)
            return True
        return False