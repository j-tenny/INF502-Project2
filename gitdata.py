import os


# Define a class to represent a GitHub User
class GitHubUser:
    def __init__(self, login):
        self.login = login

    def __str__(self):
        return f"{self.login}"

    def to_csv_record(self):
        return f"'login'\n'{self.login}'"

    def save_to_csv(self):
        save_as_csv('users.csv', self.to_csv_record())

# Placeholder definition for the GitHubLicense class
class GitHubLicense:
    def __init__(self, name, spdx_id):
        self.name = name
        self.spdx_id = spdx_id

    def __str__(self):
        return f"{self.name} ({self.spdx_id})"


class Repository:
    # TODO: create data structures for github users and add functionality to summarize users who contributed to this repo
    def __init__(self, owner_name, repo_name, token=None):
        # Assign properties
        self.owner_name = owner_name
        self.repo_name = repo_name
        self.__token = token

        # Initialize an empty variable
        self.pull_requests = tuple()

        # Automatically run function to get pull requests
        self.get_pulls()

    def get_pulls_as_json(self):
        # GitHub API endpoint for pull requests
        url = f"https://api.github.com/repos/{self.owner_name}/{self.repo_name}/pulls?state=all"

        pull_requests_json = get_github_api_request(url = url,convert_json=True,token=self.__token)

        return pull_requests_json

    def get_pulls(self,token=None):
        # Get pull requests from github in json format
        pulls_json = self.get_pulls_as_json()

        # Temporarily create an empty list
        pull_requests_list = list()

        # Convert each pull request in the json to a PullRequest object and add it
        # to the list of pull requests stored in this Repository object
        for json_record in pulls_json:
            pull_request_instance = PullRequest(token=self.__token)
            pull_request_instance.fill_from_json(json_record)
            pull_requests_list.append(pull_request_instance)

        # Convert list to tuple so it's safer from accidental changes
        self.pull_requests = tuple(pull_requests_list)

    def pull_requests_to_json(self):
        output_list = list()
        for pull_request in self.pull_requests:
            output_list.append(pull_request.to_dict())

        return output_list

    def pull_requests_to_pandas(self):
        import pandas as pd
        return pd.DataFrame(self.pull_requests_to_json())

    def __repr__(self):
        return f'Repository(owner_name: {self.owner_name}, repo_name: {self.repo_name}, n_pull_requests: {len(self.pull_requests)})'

    def to_csv_record(self):
        return f"'owner_name', 'repo_name'\n'{self.owner_name}', '{self.repo_name}'"

    def save_to_csv(self):
        # Save to repositories.csv
        save_as_csv('repositories.csv', self.to_csv_record())

        # Save to repos/owner-repo.csv
        repo_csv_path = os.path.join('repos', f'{self.owner_name}-{self.repo_name}.csv')
        save_as_csv(repo_csv_path, self.to_csv_record())

class PullRequest:
    def __init__(self,title:str = None, number:int = None, body:str = None, state:str = None, created_at:str = None, closed_at:str = None, user:str=None,  commits:str=None, additions:str=None, deletions:str=None, changed_files:str=None,token=None):

        self.title = title
        self.number = number
        self.body = body
        self.state = state
        self.created_at = created_at
        self.closed_at = closed_at
        self.user = user
        self.num_commits = commits
        self.num_additions = additions
        self.num_deletions = deletions
        self.num_changed_files = changed_files

        self.__token = token #Store token for making API requests. DO NOT INCLUDE IN OUTPUTS.



    def fill_from_json(self,json):
        self.title = json['title']
        self.number = json['number']
        self.body = json['body']
        self.state = json['state']
        self.created_at = json['created_at']
        self.closed_at = json['closed_at']
        self.user = json['user']['login']
        self.commits_url = json['commits_url'] # Don't need to output
        self.diff_url = json['diff_url'] # Don't need to output

        self.get_num_commits()
        self.get_diff_metrics()

    def to_dict(self):
        return {'title':self.title,
                'number':self.number,
                'body':self.body,
                'state':self.state,
                'created_at':self.created_at,
                'closed_at':self.closed_at,
                'user':self.user,
                'num_commits':self.num_commits,
                'num_additions':self.num_additions,
                'num_deletions':self.num_deletions,
                'num_changed_files':self.num_changed_files,
                }

    def get_num_commits(self):
        commits_json = get_github_api_request(url=self.commits_url,convert_json=True,token=self.__token)

        self.num_commits = len(commits_json)

    def get_diff_metrics(self):
        # Download diff data from API
        diff_text = get_github_api_request(url = self.diff_url,convert_json=False,token=self.__token)

        additions = 0
        deletions = 0
        changed_files = 0

  # Count number of lines that start with "diff", "+" or "-"
        for line in diff_text.split('\n'):
          if len(line) > 0:
              if line[0] == '+':
                  if line[0:3] == '+++':
                      pass
                  else:
                      additions += 1
              elif line[0] == '-':
                  if line[0:3] == '---':
                      pass
                  else:
                      deletions += 1
              elif line[0] == 'd':
                  if line[0:4] == 'diff':
                      changed_files += 1

        self.num_additions = additions
        self.num_deletions = deletions
        self.num_changed_files = changed_files


    def __str__(self):
        return f'Pull Request #{self.number}: {self.title}'

    def __repr__(self):
        return f'PullRequest(number:{self.number}, title:{self.title})'

def get_github_api_request(url,convert_json=True, token=None):
    import requests

    if token is None:
        # Make a GET request to retrieve pull requests
        response = requests.get(url)
    else:
        # Headers including the Authorization token
        headers = {"Authorization": f"token {token}"}

        # Make a GET request to retrieve pull requests
        response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        if convert_json:
            return response.json()
        else:
            return response.text
    elif response.status_code == 403:
        raise PermissionError('Server Error 403: Access to Github API denied. Consider creating and using an'
                              ' authentication token https://github.com/settings/tokens?type=beta. Read more: \n\n'+response.text)
    elif response.status_code == 404:
        raise ValueError('Error 404: No data found at this URL')
    else:
        raise ConnectionError(f"Failed to access Github API. Status code: {response.status_code} \n\n"+response.text)


    def to_csv_record(self):
        return f"'title', 'number', 'user'\n'{self.title}', '{self.number}', '{self.user}'"

    def save_to_csv(self, owner_name, repo_name):
        # Save to repos/owner-repo.csv
        repo_csv_path = os.path.join('repos', f'{owner_name}-{repo_name}.csv')
        save_as_csv(repo_csv_path, self.to_csv_record())


def get_github_api_request(url,convert_json=True, token=None):
    import requests

    if token is None:
        # Make a GET request to retrieve pull requests
        response = requests.get(url)
    else:
        # Headers including the Authorization token
        headers = {"Authorization": f"token {token}"}

        # Make a GET request to retrieve pull requests
        response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        if convert_json:
            return response.json()
        else:
            return response.text
    elif response.status_code == 403:
        raise PermissionError('Server Error 403: Access to Github API denied. Consider creating and using an'
                              ' authentication token https://github.com/settings/tokens?type=beta. Read more: \n\n'+response.text)
    elif response.status_code == 404:
        raise ValueError('Error 404: No data found at this URL')
    else:
        raise ConnectionError(f"Failed to access Github API. Status code: {response.status_code} \n\n"+response.text)

def save_as_csv(file_name, csv_record):
    # Check if the file exists
    file_exists = os.path.isfile(file_name)

    # Open the file in append mode
    with open(file_name, 'a') as file:
        # If it's a new file, write the header
        if not file_exists:
            header = csv_record.split("\n")[0]
            file.write(header + '\n')

        # Write the CSV record
        file.write(csv_record + '\n')