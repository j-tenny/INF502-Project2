import gitdata
class Application:
    def __init__(self,menu_width):
        # Store specified menu width
        self.menu_width = menu_width

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
        self.current_menu.display()
    def change_menu(self,new_menu):
        self.current_menu = new_menu
        self.current_menu.display()
    def print_current_menu_name(self):
        if self.current_menu.name.upper() != 'WELCOME MENU':
            formatted_name = ' '+self.current_menu.name+' '
            formatted_name = "{:*^{}}".format(formatted_name, self.menu_width)
            print('*'*self.menu_width)
            print(formatted_name)
            print('*'*self.menu_width)
            print()


class WelcomeMenu:
    def __init__(self,parent_app:Application):
        self.name = 'Welcome Menu'
        self.app = parent_app
    def display(self):
        clear_screen()
        print('********************************************')
        print('*********** GITHUB DATA BUDDY **************')
        print('************* Version 0.1.1 ****************')
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
        clear_screen()
        self.app.print_current_menu_name()
        print('[1] Summarize all repositories on Github')
        print('[2] Download data about a specific repository')
        print('[3] Summarize a repository which has already been downloaded')
        print('[4] Exit the program')
        user_input = validate_menu_input(num_options=4)
        self.process_user_input(user_input)

    def process_user_input(self,user_input):
        if user_input==1:
            self.app.change_menu(self.app.all_repos_menu)
        elif user_input == 2:
            self.app.change_menu(self.app.get_repo_menu)
        elif user_input==3:
            self.app.change_menu(self.app.select_repo_menu)
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
        clear_screen()
        self.app.print_current_menu_name()
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
        clear_screen()
        self.app.print_current_menu_name()
        print('Type in Github owner name and repository name below')
        print('   *Or return to main menu by typing EXIT')

        # Let user type in owner and repo name
        owner_name = self.validate_owner_input()
        repo_name = self.validate_repo_input()

        # Use these inputs to download data for a repo
        # TODO: check to see if repo exists in current repos list before downloading/adding it again
        # TODO: Improve error handling when trying to download repo data
        #try:
        repo_data = gitdata.Repository(owner_name,repo_name)
        #except KeyError as e:
            # If an exception occurs, start over
        #    print(str(e))
        #    print('Data for an essential field was not found, try another repository.')
        #    self.display()

        # Append this repo data to the app's stored repo data
        self.app.repos.append(repo_data)

        # Set selected_repo_index to the newly downloaded repo
        self.app.selected_repo_index = len(self.app.repos) - 1

        # Open the repo analysis menu
        self.app.change_menu(self.app.repo_analysis_menu)

    def validate_owner_input(self):
        # TODO: use while loop or try-except to make sure string is valid and owner exists
        owner = input('Input the name of a Github repo owner >> ').strip()
        if owner.upper() == 'EXIT':
            self.app.change_menu(self.app.main_menu)
        return owner

    def validate_repo_input(self):
        # TODO use while loop or try-except to make sure string is valid and owner exists
        repo = input('Input the name of a Github repo >> ').strip()
        if repo.upper() == 'EXIT':
            self.app.change_menu(self.app.main_menu)
        return repo

class RepoAnalysisMenu:
    def __init__(self,parent_app:Application):
        self.name = 'Repo Analysis Tool'
        self.app = parent_app

    def display(self):
        # Get the Repository object for the selected repo index
        selected_repo = self.app.repos[self.app.selected_repo_index]

        # Display menu title and options
        clear_screen()
        self.app.print_current_menu_name()

        print(f'Selected repo: {selected_repo.owner_name}/{selected_repo.repo_name}')
        print('[1] Show all pull requests')
        print('[2] Show summary for this repository')
        print('[3] Show user correlation data')
        print('[4] Return to main menu')

        user_input = validate_menu_input(num_options=4)

        self.process_user_input(user_input)

    def process_user_input(self,user_input):
        if user_input==1:
            # TODO: Hook up function to display pull requests
            print('Function not implemented yet')
            user_input = validate_menu_input(num_options=4)
            self.process_user_input(user_input)

        elif user_input==2:
            # TODO: Hook up function to display repository summary
            print('Function not implemented yet')
            user_input = validate_menu_input(num_options=4)
            self.process_user_input(user_input)

        elif user_input==3:
            # TODO: Hook up function to display user correlation data
            print('Function not implemented yet')
            user_input = validate_menu_input(num_options=4)
            self.process_user_input(user_input)

        else:
            self.app.change_menu(self.app.main_menu)


class SelectRepoMenu:
    def __init__(self,parent_app):
        self.name = 'Select a Repo'
        self.app = parent_app

    def display(self):
        clear_screen()
        self.app.print_current_menu_name()

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
