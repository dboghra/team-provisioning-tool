import os
import logging
from github import Github
from dotenv import load_dotenv
from validate_data import validate_csv
from provisioner import provision_all_teams


#call provisioner to create repo and add members


# Load .env file
load_dotenv()
#load config file(represents each team)


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def main():
    # Test GitHub authentication
    token = os.getenv("GITHUB_TOKEN") #org_name = os.getenv("GITHUB_ORG")
    username = os.getenv("GITHUB_ORG")

    if not token or not username: #replace with org_name if using org
        print("ERROR: GITHUB_TOKEN or GITHUB_ORG not in .env")
        return
    
    try:
        from github import Auth
        g = Github(auth=Auth.Token(token))
        #org = g.get_organization(org_name)
        user = g.get_user(username)
        print(f"✓ Yay ur not a chud! Authenticated. Organization: {user.name}")
    except Exception as e:
        print(f"ERROR: Authentication failed you chud: {e}")
        return
    
    # Load and validate CSV
    valid_rows, error_rows = validate_csv("config.csv")
    
    if error_rows:
        print("\n⚠️ Validation errors found. Fix them before provisioning:")
        for error in error_rows:
            print(f"  - {error}")
        return
    #print("valid_rows:", valid_rows)
    #print("error_rows:", error_rows)


    #Provision teams
    print("\nProvisioning teams...")
    print("-" * 50)
    successes, failures = provision_all_teams(valid_rows, token, username, "templates/")
    
    # print summary
    print("-" * 50)
    print(f"\n✓ Provisioning complete!")
    print(f"  Successes: {len(successes)}")
    print(f"  Failures: {len(failures)}")

    if failures:
        print("\nFailed operations:")
        for failure in failures:
            print(f"  - {failure['repo_name']}: {failure['action']} - {failure['error']}")



if __name__ == "__main__":
    main()