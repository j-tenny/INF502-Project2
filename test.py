import gitdata

jabref_repo = Repository('jabref', 'jabref')
n_users = jabref_repo.total_user()
tot_pull_close = jabref_repo.total_pulls_closed()
tot_pull_open = jabref_repo.total_pulls_opened()
old = jabref_repo.oldest()
print(n_users)
print(tot_pull_close)
print(tot_pull_open)
print(old)
