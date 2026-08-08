import csv
import logging

# def validate_csv takes the csv name
#read entire csv file and parse it line by line into a list of dictionaries
#returns 2 lists: valid_rows and invalid_rows

#def validate_csv(filename):
    #print()
    # Read the CSV file
    # Parse each row
    # Check each row for errors
    # Collect errors
    #check if repo already exists

    #check if members are part of organization
    #check if repo name is valid
    # Return (valid_rows, error_rows)


    # validate-data.py



# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_valid_repo_name(repo_name):
    # Check if repo_name is valid GitHub format
    # (lowercase, hyphens only, no spaces, etc.)
    # Return True or False
    pass

def is_valid_email(email):
    # Check if email is valid format
    # (something@domain.com)
    # Return True or False
    pass

def is_valid_github_username(username):
    # Check if github_username is valid
    # (alphanumeric + hyphens)
    # Return True or False
    pass

def is_valid_member_role(role):
    # Check if member_role is either "admin" or "developer"
    # Return True or False
    pass

def validate_row(row, row_number):
    # Validate a single row
    # Check all required columns exist
    # Check repo_name format
    # Check email format
    # Check github_username format
    # Check member_role is valid
    # Return (is_valid: bool, error_message: str)
    pass

def check_for_duplicates(valid_rows):
    # Check if there are duplicate rows
    # (same repo_name + github_username)
    # Return list of duplicate errors
    pass

def validate_csv(filename):
    # Main validation function
    # Read CSV file
    # Parse each row
    # Validate each row using validate_row()
    # Collect all errors
    # Check for duplicates in valid rows
    # Return (valid_rows: list, error_rows: list)
    pass