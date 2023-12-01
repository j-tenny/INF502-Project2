import gitdata
import unittest
import os

if os.path.exists('mytoken.txt'):
    with open('mytoken.txt') as f:
        token = f.read()
else:
    token = None
    print('Warning: test probably will not work without a valid github token')

class RepositoryTest(unittest.TestCase):
    def setUp(self):
        self.repos = list()
        self.owner_repos = [('jabref', 'jabref'), ('sethvargo', 'terraform-provider-google'), ('stanGirard', 'Alpine-Powerhouse')]
        self.token = token
        for owner, repo in self.owner_repos:
            self.repos.append(gitdata.Repository(owner, repo,time_window_days=30, token=self.token))

    def test_get_users_as_json(self):
        for repo in self.repos:
            json_data = repo.users_to_json()
            for data in json_data:
                self.assertGreaterEqual(data['followers'], 0)
                self.assertGreaterEqual(data['following'], 0)
                self.assertGreaterEqual(data['public_repos'], 0)
                self.assertGreaterEqual(data['public_gists'], 0)

    def test_get_pulls_as_json(self):
        for repo in self.repos:
            json_data = repo.pull_requests_to_json()
            for data in json_data:
                self.assertGreaterEqual(data['num_additions'], 0)
                self.assertGreaterEqual(data['num_deletions'], 0)
                self.assertGreaterEqual(data['num_changed_files'], 0)
                self.assertGreaterEqual(data['num_commits'], 0)

    def test_total_user(self):
        for repo in self.repos:
            self.assertGreaterEqual(repo.total_user(), 0)

    def test_total_pulls_closed(self):
        for repo in self.repos:
            self.assertGreaterEqual(repo.total_pulls_closed(), 0)

    def test_total_pulls_open(self):
        for repo in self.repos:
            self.assertGreaterEqual(repo.total_pulls_open(), 0)
    
if __name__ == '__main__':
    unittest.main()
