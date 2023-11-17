class Repository:
    # TODO: create data structures for github users and add functionality to summarize users who contributed to this repo
    def __init__(self, owner_name, repo_name):
        # Assign properties
        self.owner_name = owner_name
        self.repo_name = repo_name

        # Initialize an empty variable
        self.pull_requests = tuple()

        # Automatically run function to get pull requests
        self.get_pulls()

    def get_pulls_as_json(self):
        import requests

        # GitHub API endpoint for pull requests
        url = f"https://api.github.com/repos/{self.owner_name}/{self.repo_name}/pulls"

        # Make a GET request to retrieve pull requests
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            pull_requests_json = response.json()

        else:
            print(f"Failed to retrieve pull requests. Status code: {response.status_code}")
            print(response.text)

        return pull_requests_json

    def get_pulls(self):
        # Get pull requests from github in json format
        pulls_json = self.get_pulls_as_json()

        # Temporarily create an empty list
        pull_requests_list = list()

        # Convert each pull request in the json to a PullRequest object and add it
        # to the list of pull requests stored in this Repository object
        for json_record in pulls_json:
            pull_request_instance = PullRequest()
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
class PullRequest:
  def __init__(self,title:str = None, number:int = None, body:str = None, state:str = None, created_at:str = None, closed_at:str = None):
    self.title = title
    self.number = number
    self.body = body
    self.state = state
    self.created_at = created_at
    self.closed_at = closed_at

  def fill_from_json(self,json):
    self.title = json['title']
    self.number = json['number']
    self.body = json['body']
    self.state = json['state']
    self.created_at = json['created_at']
    self.closed_at = json['closed_at']

  def to_dict(self):
    return {'title':self.title,
            'number':self.number,
            'body':self.body,
            'state':self.state,
            'created_at':self.created_at,
            'closed_at':self.closed_at
            }

  def __str__(self):
    return f'Pull Request #{self.number}: {self.title}'

  def __repr__(self):
    return f'PullRequest(number:{self.number}, title:{self.title})'

