import gitdata

jabref_repo = gitdata.Repository('jabref', 'jabref',token = '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')
n_users = jabref_repo.total_user()
tot_pull_close = jabref_repo.total_pulls_closed()
tot_pull_open = jabref_repo.total_pulls_open()
old = jabref_repo.oldest()
print(n_users)
print(tot_pull_open)
print(tot_pull_close)
print(old)
#jabref_repo.box_closed_open_commit()
#jabref_repo.box_addition_deletion()
#jabref_repo.scatter_addition_deletion()
