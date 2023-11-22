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
            temp_df = self.repos.pull_requests_to_pandas()
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
            temp_df = self.repos.pull_requests_to_pandas()
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
        #import pandas as pd
        #df = self.repos.users_to_pandas()
        #df.plot.bar(x='users', y='repo', rot=0)
        print("I Still need to work on this function")
        return None
        

class Repository:
    # TODO: create data structures for github users and add functionality to summarize users who contributed to this repo
    def __init__(self, owner_name, repo_name):
        # Assign properties
        self.owner_name = owner_name
        self.repo_name = repo_name

        # Initialize empty variables for pull request data and contributing user data
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

