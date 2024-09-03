import os
import sys
import pygit2

# Set up the root directory and change to it
root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)
os.chdir(root)

def update_repository():
    try:
        # Disable owner validation
        pygit2.option(pygit2.GIT_OPT_SET_OWNER_VALIDATION, 0)

        # Initialize the repository
        repo = pygit2.Repository(os.path.abspath(os.path.dirname(__file__)))

        # Get the current branch name
        branch_name = repo.head.shorthand

        # Fetch from the remote
        remote_name = 'origin'
        remote = repo.remotes[remote_name]
        remote.fetch()

        # Get the local and remote branch references
        local_branch_ref = f'refs/heads/{branch_name}'
        local_branch = repo.lookup_reference(local_branch_ref)

        remote_reference = f'refs/remotes/{remote_name}/{branch_name}'
        remote_commit = repo.revparse_single(remote_reference)

        # Determine merge analysis result
        merge_result, _ = repo.merge_analysis(remote_commit.id)

        if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
            print("Already up-to-date")
        elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
            # Perform fast-forward merge
            local_branch.set_target(remote_commit.id)
            repo.head.set_target(remote_commit.id)
            repo.checkout_tree(repo.get(remote_commit.id))
            repo.reset(local_branch.target, pygit2.GIT_RESET_HARD)
            print("Fast-forward merge completed.")
        elif merge_result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
            print("Update failed - Conflicts detected. Did you modify any files?")
        else:
            print("No valid merge strategy found.")
        
        print('Update succeeded.')
        
    except Exception as e:
        print('Update failed.')
        print(str(e))

if __name__ == "__main__":
    update_repository()

    # Import and launch your module after updating the repository
    try:
        from launch import *
        print("Module launched successfully.")
    except ImportError as e:
        print("Failed to launch the module.")
        print(str(e))
