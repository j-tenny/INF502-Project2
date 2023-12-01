# INF502-Project2

The program builds a command line application that summarizes information from Github. The application creates summaries and visualizations describing several statistics across all repositories on Github, and will also allow the user to request a summary about a specific repository.

For each pull request the following is stored:
 - Pull request title
 - Pull request number
 - Body
 - State
 - Date of creation (created\_at)
 - Closing date (if the state is different than open)
 - User

The application also pulls data for each author (user) found in the pull requests for this repository. For each user, the following info is collected from the pull requests and/or their profile page on Github:
 - Number of pull requests submitted to this repository
 - Number of Repositories the user has contributed to
 - Number of Followers
 - Number of Following
 - Number of contributions across all repositories in the last year.

The function save_as_csv can be reused to convert any object to a csv entry.

## Menu Options:

### Main Menu

 - Option 1: Summarizes info about "all repositories." This produces visualizations of the following:
    1. A line graph showing the total number of pull requests per day
    2. A line graph comparing number of open and closed pull requests per day
    3. A bars plot comparing the number of users per repository

 - Option 2: Requests data for a specific repository from GitHub by providing the owner and repository name.

 - Option 3: View a list of repositories requested in this session.

 - Option 4: Exit the program

### Submenus
 - For any repository data is collected on, you may select that repository, then perform any of the following actions:
   1. Show all pull requests from a certain repository
   2. Show the summary of a repository. Summary contains: A. Number of pull requests in open state B. Number of pull requests in closed state C. Number of users D. Date of the oldest pull request E. Create and store visual representation data about the repository (via pandas) a. A boxplot that compares closed vs. open pull requests in terms of number of commits b. A boxplot that compares closed vs. open pull requests in terms of additions and deletions c. A boxplot that compares the number of changed files grouped by the author association d. A scatterplot that shows the relationship between additions and deletions e. Calculate the correlation between all the numeric data in the pull requests for a repository (and visualize as a matrix?)
   3. Calculate the correlation between the data fields collected about users A. following B. followers C. number of pull requests D. number of contributions