import gitdata
class Application:
    def __init__(self,menu_width,token=None):
        # Store specified menu width
        self.menu_width = menu_width

        # Initialize token
        self._token = token

        # Initialize an empty list to store repo data
        self.repos = list()

        # Initialize selected repo
        self.selected_repo_index = 0

        # Create an instance of each menu class
        self.welcome_menu = WelcomeMenu(parent_app=self)
        self.main_menu = MainMenu(parent_app=self)
        self.all_repos_menu = AllReposMenu(parent_app=self)
        self.get_repo_menu = GetRepoMenu(parent_app=self)
        self.select_repo_menu = SelectRepoMenu(parent_app=self)
        self.repo_analysis_menu = RepoAnalysisMenu(parent_app=self)




    # Define application functions
    def run(self):
        self.change_menu(self.welcome_menu)
    def refresh(self):
        clear_screen()
        self.current_menu.display()
    def change_menu(self,new_menu):
        clear_screen()
        self.current_menu = new_menu
        self.print_current_menu_name()
        self.current_menu.display()
    def print_current_menu_name(self):
        if self.current_menu.name.upper() != 'WELCOME MENU':
            formatted_name = ' '+self.current_menu.name+' '
            formatted_name = "{:*^{}}".format(formatted_name, self.menu_width)
            print('*'*self.menu_width)
            print(formatted_name)
            print('*'*self.menu_width)


class WelcomeMenu:
    def __init__(self,parent_app:Application):
        self.name = 'Welcome Menu'
        self.app = parent_app
    def display(self):
        clear_screen()
        print('********************************************')
        print('*********** GITHUB DATA BUDDY **************')
        print('************* Version 0.2.1 ****************')
        print()
        print('Updated November 11, 2023')
        print('Developed by...[names]')
        print()
        print()
        input('PRESS ENTER TO CONTINUE')
        self.app.change_menu(self.app.main_menu)
class MainMenu:
    def __init__(self,parent_app:Application):
        self.name = 'Main Menu'
        self.app = parent_app
    def display(self):
        print()
        print('[1] Download data for a repository')
        print('[2] Summarize a repository which has already been downloaded')
        print('[3] Summarize all repositories that have been downloaded in this session')
        print('[4] Exit the program')
        user_input = validate_menu_input(num_options=4)
        self.process_user_input(user_input)

    def process_user_input(self,user_input):
        if user_input==1:
            self.app.change_menu(self.app.get_repo_menu)
        elif user_input == 2:
            self.app.change_menu(self.app.select_repo_menu)
        elif user_input==3:
            self.app.change_menu(self.app.all_repos_menu)
        else:
            import sys
            sys.exit()


class AllReposMenu:
    def __init__(self,parent_app:Application):
        self.name = 'All Repos Tool'
        self.app = parent_app

    def display(self):
        # TODO: Create and hook up functionality for all repos analysis

        # Display title and menu options
        print()
        print('This menu will allow users to summarize data about all repos on github')
        print('[1] Return to main menu')

        user_input = validate_menu_input(num_options=1)
        self.process_user_input(user_input)

    def process_user_input(self,user_input):
        if user_input==1:
            self.app.change_menu(self.app.main_menu)


class GetRepoMenu:
    def __init__(self,parent_app:Application):
        self.name = 'Download Repo Data'
        self.app = parent_app

    def display(self):
        # Display menu name and options
        print()
        print('Type in Github owner name and repository name below')
        print('   *Or return to main menu by typing EXIT')

        # Let user type in owner and repo name
        owner_name = self.validate_owner_input()
        repo_name = self.validate_repo_input()

        print('Downloading and analyzing Github data. Please wait...')

        # Use these inputs to download data for a repo
        try:
            repo_data = gitdata.Repository(owner_name,repo_name,token=self.app._token)
        except KeyError as e:
            # If an exception occurs, start over
            print(str(e))
            print('Data for an essential field was not found, try another repository.')
            print()
            self.display()

        except PermissionError as e:
            print(str(e))
            print()
            self.display()

        except ConnectionError as e:
            print(str(e))
            print()
            self.display()

        except Exception as e:
            print(str(e))
            print()
            self.display()

        # Append this repo data to the app's stored repo data
        self.app.repos.append(repo_data)

        # Set selected_repo_index to the newly downloaded repo
        self.app.selected_repo_index = len(self.app.repos) - 1

        # Open the repo analysis menu
        self.app.change_menu(self.app.repo_analysis_menu)

    def validate_owner_input(self):
        valid = False
        while not valid:
            print()
            owner = input('Input the name of a Github repo owner (or type EXIT) >> ').strip()
            if owner == 'EXIT':
                valid = True
                self.app.change_menu(self.app.main_menu)
            else:
                if ('/' in owner) or ('.' in owner):
                    print('Input owner name only, do not include / . or other invalid characters')
                else:
                    try:
                        owned_repos_list = list()
                        url = f'https://api.github.com/users/{owner}'
                        json = gitdata.get_github_api_request(url=url,convert_json=True,token = self.app._token)
                        owner = json['login']
                        repos = gitdata.get_github_api_request(url=json["repos_url"],convert_json=True,token=self.app._token)
                        for repo in repos:
                            if repo['owner']['login'] == owner:
                                owned_repos_list.append(repo['name'])
                        if len(owned_repos_list) == 0:
                            print('This user exists but does not own any public repos')
                        else:
                            valid = True
                    except ValueError:
                        print('Could not find this owner on Github. Check spelling, internet connection, or try again.')
                    except Exception as e:
                        print(str(e))

        print(f'Found {len(owned_repos_list)} repositories owned by {owner}. Type LIST to display repo names.')
        self._current_owned_repos_list = owned_repos_list
        self._current_owner = owner
        return owner

    def validate_repo_input(self):
        valid = False
        while not valid:
            print()
            repo = input('Input the name of a Github repository (or type EXIT) >> ').strip()
            if repo == 'EXIT':
                valid = True
                self.app.change_menu(self.app.main_menu)
            elif repo == 'LIST':
                print('\n'.join(self._current_owned_repos_list))
            else:
                if ('/' in repo) or ('.' in repo):
                    print('Input repo name only, do not include / . or other invalid characters')
                else:
                    try:
                        already_downloaded = False
                        for existing_repo in self.app.repos:
                            if (self._current_owner == existing_repo.owner_name) & (repo == existing_repo.repo_name):
                                already_downloaded = True
                        if not already_downloaded:
                            url = f'https://api.github.com/repos/{self._current_owner}/{repo}'
                            gitdata.get_github_api_request(url=url, convert_json=True, token=self.app._token)
                            valid = True
                        else:
                            print('Data for this repository has already been downloaded. Type EXIT to return to main menu.')

                    except ValueError:
                        print(f'Could not find {repo} owned by {self._current_owner}. Type LIST to display valid repo names.')

                    except Exception as e:
                        print(str(e))

        return repo

class RepoAnalysisMenu:
    def __init__(self,parent_app:Application):
        self.name = 'Repo Analysis Tool'
        self.app = parent_app

    def display(self):
        # Get the Repository object for the selected repo index
        selected_repo = self.app.repos[self.app.selected_repo_index]

        # Display options
        print()
        print(f'Selected repo: {selected_repo.owner_name}/{selected_repo.repo_name}')
        print('[1] Show all pull requests')
        print('[2] Show summary for this repository')
        print('[3] Show user correlation data')
        print('[4] Return to main menu')

        user_input = validate_menu_input(num_options=4)

        self.process_user_input(user_input)

    def process_user_input(self,user_input):
        if user_input==1:
            pulls = self.app.repos[self.app.selected_repo_index].pull_requests
            for pull in pulls:
                print(str(pull))
            self.display()

        elif user_input==2:
            # TODO: Hook up function to display repository summary
            print('Function not implemented yet')
            self.display()

        elif user_input==3:
            # TODO: Hook up function to display user correlation data
            print('Function not implemented yet')
            self.display()

        else:
            self.app.change_menu(self.app.main_menu)


class SelectRepoMenu:
    def __init__(self,parent_app):
        self.name = 'Select a Repo'
        self.app = parent_app

    def display(self):
        print()
        # Display menu option for each stored repo
        menu_option_number = 1
        if len(self.app.repos) >= 1:
            for repo in self.app.repos:
                print(f'[{menu_option_number}] {repo.owner_name}/{repo.repo_name}')
                menu_option_number += 1
        else:
            print('No repo data has been downloaded yet')

        print(f'[{menu_option_number}] Return to main menu')

        # Let user select a menu option
        user_input = validate_menu_input(num_options=menu_option_number)

        if user_input == menu_option_number:
            self.app.change_menu(self.app.main_menu)
        else:
            self.process_user_input(user_input)

    def process_user_input(self,user_input):
        # Assign index. Note, menu options started at 1 but repo index starts at 0
        self.app.selected_repo_index = user_input - 1

        # Go to analysis menu
        self.app.change_menu(self.app.repo_analysis_menu)


def clear_screen():
    print('\n'*20)

def validate_menu_input(num_options):
    prompt = '\nSelect an option above >> '
    user_input = -1
    while user_input not in range(1, num_options + 1):
        try:
            user_input = int(input(prompt).strip())
        except:
            print('You must input a valid integer')

        if user_input not in range(1, num_options + 1):
            prompt = f'Input a number between 1 and {num_options} >> '

    return user_input
