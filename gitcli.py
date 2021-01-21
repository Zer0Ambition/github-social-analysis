from github import Github


class Gitcli:
    def __init__(self, token, user, repo):
        self.token = token
        self.user = user
        self.repository_name = repo
        self.stargazers = ''
        self.client = ''
        self.repo = ''

    def query(self):
        self.client = Github(self.token, per_page=100)
        self.user = self.client.get_user(self.user)
        self.repo = self.user.get_repo(self.repository_name)
        self.stargazers = [s for s in self.repo.get_stargazers()]