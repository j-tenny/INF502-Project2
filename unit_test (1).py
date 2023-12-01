import gitdata
import unittest
import os
import shutil
import datetime
import time
import json

class RepositoryTest(unittest.TestCase):
    def setUp(self):
        self.repos = list()
        self.owner_repos = [('jabref', 'jabref'), ('sethvargo', 'terraform-provider-google'), ('stanGirard', 'Alpine-Powerhouse')]
        self.token = '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'
        for owner, repo in self.owner_repos:
            self.repos.append(gitdata.Repository(owner, repo, self.token))

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
