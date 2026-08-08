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

def write_archive_log(successes, failures):
    """Write provisioning results to archive.log"""
    try:
        with open("archive.log", "w") as f:
            f.write("=" * 60 + "\n")
            f.write("PROVISIONING RESULTS\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Total Successes: {len(successes)}\n")
            f.write(f"Total Failures: {len(failures)}\n\n")
            
            if successes:
                f.write("SUCCESSES:\n")
                f.write("-" * 60 + "\n")
                for success in successes:
                    repo = success['repo_name']
                    action = success['action']
                    details = success['details']
                    f.write(f" {repo} - {action}\n")
                    f.write(f"  {details}\n\n")
            
            if failures:
                f.write("\nFAILURES:\n")
                f.write("-" * 60 + "\n")
                for failure in failures:
                    repo = failure['repo_name']
                    action = failure['action']
                    error = failure['error']
                    f.write(f"✗ {repo} - {action}\n")
                    f.write(f"  Error: {error}\n\n")
        
        print(f"\n Archive log written to archive.log")
    except Exception as e:
        print(f"ERROR: Failed to write archive log: {e}")






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


    write_archive_log(successes, failures)


if __name__ == "__main__":
    main()