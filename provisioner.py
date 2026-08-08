

#call github api to create repo 
    # use repo_name from the row
    #use description from the row
# add members to repo
    #use github_username form the row and check if it exists, if not create it
    #add members to the repo and use member roles from the row to set permisions
        #admin --> admin access
        #developer --> push access
# set the branch protections on main so required reviews and no force push
#commit the run template to the repo(run-test.yml) and set it to run on push 

def create_repo(org, repo_name, description, token):
    # Create repo on GitHub
    # Return success or failure

def add_member(org, repo_name, github_username, member_role, token):
    # Add member to repo with correct permission
    # Return success or failure

def set_branch_protections(org, repo_name, token):
    # Set protections on main branch
    # Return success or failure

def commit_template(org, repo_name, template_path, token):
    # Commit run-test.yml to repo
    # Return success or failure

def provision_all_teams(valid_rows, token, org):
    # Main function that orchestrates everything
    # Keeps track of which repos are done
    # Calls the above functions in the right order
    # Returns successes and failures list




