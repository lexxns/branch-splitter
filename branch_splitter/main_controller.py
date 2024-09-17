from branch_splitter.branch_manager import BranchManager
from branch_splitter.change_manager import ChangeManager
from branch_splitter.git_repo import GitRepo
from branch_splitter.user_interface import UserInterface


class MainController:
    def __init__(self, repo_path):
        self.git_repo = GitRepo(repo_path)
        self.change_manager = ChangeManager(self.git_repo)
        self.branch_manager = BranchManager(self.git_repo)
        self.ui = UserInterface()

    def run(self):
        pass
        # Main process orchestration
        # 1. Get all changes
        # 2. Prompt for new branches
        # 3. For each change, prompt for assignment
        # 4. Apply changes to branches
        # 5. Confirm and push branches
