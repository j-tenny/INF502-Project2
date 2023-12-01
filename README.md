# INF502-Project2

This program is a command line application that summarizes information from Github. The application allows users to download data about public repositories and their associated pull requests and users, then create summaries and visualizations.

For each pull request the following is stored:
 - Pull request title
 - Pull request number
 - Body
 - State
 - Date of creation (created_at)
 - Closing date (if the state is different than open)
 - User

The application also pulls data for each author (user) found in the pull requests for this repository. For each user, the following info is collected from the pull requests and/or their profile page on Github:
 - Number of pull requests submitted to this repository
 - Number of contributions in the pull requests
 - Number of followers
 - Number of following

All of this data is saved to CSVs with a reusable save_as_csv function.

Note: Figures and data are stored in a temporary location which will be deleted each time the application runs. To export the data to a permanent location, use the export data tool from the main menu.

## Menu Options:

### Main Menu
 - Option 1: Requests data for a specific repository from GitHub by providing the owner and repository name and a time window in days.
 - Option 2: Select from a list of repositories that have already been requested in this session.
 - Option 3: Summarizes info about all repositories that have been downloaded in this session. This produces visualizations of the following:
    1. A line graph showing the total number of pull requests per day
    2. A line graph comparing number of open and closed pull requests per day
    3. A bar plot comparing the number of users per repository
 - Option 4: Export session
 - Option 5: Exit the program

### Submenus
 - For any repository you have downloaded, you may select that repository, then perform any of the following actions:
   1. Show all pull requests from a certain repository
   2. Show the summary of a repository. Summary contains:
      - Number of pull requests in open state 
      - Number of pull requests in closed state 
      - Number of users 
      - Date of the oldest pull request
      - Correlation between all the numeric data in the pull requests
      
      Additionally, figures are saved to the disk which represent the following:
      - A boxplot that compares closed vs. open pull requests in terms of number of commits 
      - A boxplot that compares closed vs. open pull requests in terms of additions and deletions 
      - A boxplot that compares the number of changed files grouped by the author association 
      - A scatterplot that shows the relationship between additions and deletions 
      
   3. Show correlation between numeric attributes of users