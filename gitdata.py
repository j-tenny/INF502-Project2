import os
class AllRepositories:
    def __init__(self, repos):
        self.repos = repos
        self.start_date = None
        self.end_date = None

        self.fill_analysis_dates()
        self.display_pulls_per_day()
        self.display_open_vs_closed_per_day()
        self.display_users_per_repository()

    def fill_analysis_dates(self):
        from datetime import date, timedelta

        # use datetime package to create start and end dates for the last 60 days
        self.end_date = date.today()
        self.start_date = end_date - timedelta(days=59)

    def display_pulls_per_day(self):
        import pandas as pd
        dfs = list()
        for repo in self.repos:
            temp_df = repo.pull_requests_to_pandas()
            dfs.append(temp_df)

        df = pd.concat(dfs)
        
        #this will remove the hours, minutes and seconds data from the created_at field and leave us with just the date
        df['created_at'] = df.created_at.dt.floor('d')

        try:
            #create dataframe of last 60 days
            analysis_days = pd.DataFrame({'date': pd.date_range(start=self.start_date, end = self.end_date, freq='1d')})
            #create a tally column that queries our pull requests to find the number of requests opened for each day
            analysis_days['tally'] = analysis_days['date'].apply( lambda x: len(df.query("created_at == @x")))
            #plot the tallies per day
            analysis_days.plot.line(x='date', y='tally')

        except Exception as e:
            #this is just for troubleshooting our code and testing, we shouldn't need it once we have this perfected
            print('something is wrong with the data, here is the error: ')
            print(e)
        
        return None

    def display_open_vs_closed_per_day(self):
        import pandas as pd
        dfs = list()
        
        for repo in self.repos:
            temp_df = repo.pull_requests_to_pandas()
            dfs.append(temp_df)

        df = pd.concat(dfs)

        #this will remove the hours, minutes and seconds data from the created_at and closed_at fields so we only have the date
        df['created_at'] = df.created_at.dt.floor('d')
        df['closed_at'] = df.created_at.dt.floor('d')

        try:
            #create dataframe of last 60 days
            analysis_days = pd.DataFrame({'date': pd.date_range(start=self.start_date, end = self.end_date, freq='1d')})
            #create an open and close tally column that queries our pull requests to find the number of requests opened and closed for each day
            analysis_days['open_tally'] = analysis_days['date'].apply( lambda x: len(df.query("created_at == @x")))
            analysis_days['close_tally'] = analysis_days['date'].apply( lambda x: len(df.query("closed_at == @x")))
            #plot open vs close per day, this will automatically color between open and close tallies
            analysis_days.plot.line(x='date')

        except Exception as e:
            #this is just for troubleshooting our code and testing, we shouldn't need it once we have this perfected
            print('something is wrong with the data, here is the error: ')
            print(e)
            
        return None

    def display_users_per_repository(self):
        import pandas as pd
        #initialize list of dicts
        repo_users = list()
        #iterate across all repos
        for repo in self.repos:
            initialize dictionary
            temp_dict = dict()
            temp_dict['repo_name'] = repo.repo_name
            temp_dict['users'] = len(repo.users)
            repo_users.append(temp_dict)
            
        #create dataframe from list of dicts and display bar plot    
        df = pd.DataFrame(repo_users)
        df.plot.bar(x='users', y='repo_name', rot=0)
        return None




# Placeholder definition for the GitHubLicense class
class GitHubLicense:
    def __init__(self, name, spdx_id):
        self.name = name
        self.spdx_id = spdx_id

    def __str__(self):
        return f"{self.name} ({self.spdx_id})"


class Repository:
    def __init__(self, owner_name, repo_name, token=None):
        # Assign properties
        self.owner_name = owner_name
        self.repo_name = repo_name
        self.__token = token

        # Initialize empty variables for pull request data and contributing user data
        self.pull_requests = tuple()
        self.users = tuple()

        # Automatically run function to get pull requests and users
        self.get_pulls()
        self.get_users()

    def get_pulls_as_json(self):
        # GitHub API endpoint for pull requests
        url = f"https://api.github.com/repos/{self.owner_name}/{self.repo_name}/pulls"

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


    def get_users_as_json(self, username):
        # GitHub API endpoint for pull requests
        url = f"https://api.github.com/users/{username}"

        users = get_github_api_request(url = url,convert_json=True,token=self.__token)

        return users_json

    def get_users(self,token=None):
        # Temporarily create an empty list
        user_list = list()
        
        #iterate across pull requests
        for pull in self.pull_requests:
            #check if name in user list
            check = [i for i,d in enumerate(user_list) if d['name'] == pull.user]
            
            if len(check) == 0:
                # Get pull requests from github in json format
                user_json = self.get_pulls_as_json( pull.user )

                # Convert each user to a user object and add it
                # to the list of users stored in this Repository object
                user_instance = User(name = pull.user, token=self.__token)
                user_instance.fill_from_json(user_json)
                user_list.append(user_instance)

            else:
                #otherwise add another contribution tally to the user
                user_list[check[0]].contributions += 1

        # Convert list to tuple so it's safer from accidental changes
        self.users = tuple(user_list)

    def users_to_json(self):
        output_list = list()
        for user in self.users:
            output_list.append(user.to_dict())

        return output_list

    def users_to_pandas(self):
        import pandas as pd
        return pd.DataFrame(self.users_to_json())
      
    
    def total_user(self):
        total_users_set = set()
        for pull in self.pull_requests:
            total_users_set.add(pull.user)
        total_users = len(total_users_set) 
        return total_users
    
    def total_pulls_closed(self):
        pull_closed_total = 0
        for pull in self.pull_requests:
            if pull.state == 'closed':
                pull_closed_total += 1
        return pull_closed_total
    
    def total_pulls_open(self):
        pull_open_total = 0
        for pull in self.pull_requests:
            if pull.state == 'open':
                pull_open_total += 1
        return pull_open_total
    
    def oldest(self):
        dates = []
        for pull in self.pull_requests:
            if pull.state == 'open':
                dates.append(pull.created_at)
        dates.sort()
        oldest_date = dates[0]
        return oldest_date
        
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
  def __init__(self,title:str = None, number:int = None, body:str = None, state:str = None, created_at:str = None, closed_at:str = None,
               user:str=None,  commits:str=None, additions:str=None, deletions:str=None, changed_files:str=None,token=None):

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



class User:
  def __init__(self, name, followers:str = None, following:int = None, repos:str = None, gists:str = None, token=None):
      
    self.name = name
    self.followers = followers
    self.following = following
    self.public_repos = public_repos
    self.public_gists = public_gists
    self.contributions = 1

    self.__token = token #Store token for making API requests. DO NOT INCLUDE IN OUTPUTS.

  def fill_from_json(self,json):
    self.followers = json['followers']
    self.following = json['following']
    self.public_repos = json['public_repos']
    self.public_gists = json['public_gists']

  def to_dict(self):
    return {'name':self.name,
            'followers':self.followers,
            'following':self.following,
            'public_repos':self.public_repos,
            'public_gists':self.public_gists,
            'contributions':self.contributions
            }
  
  def to_csv_record(self):
    #TODO: Update this function now that the users class is done
    return f"'login'\n'{self.login}'"

  def save_to_csv(self):
    #TODO: Update this function now that the users class is done
      save_as_csv('users.csv', self.to_csv_record())
      
      
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
