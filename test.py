import gitdata

jabref_repo = Repository('jabref', 'jabref')
n_users = jabref_repo.total_user()
print(n_users)
