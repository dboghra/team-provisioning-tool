# validate-data.py

import csv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_valid_repo_name(repo_name):
    """
    Check if repo_name is valid GitHub format.
    Rules: lowercase letters, numbers, hyphens only
           can't start or end with hyphen
           1-39 chars
    """
    if not repo_name or len(repo_name) < 1 or len(repo_name) > 39:
        return False
    
    if repo_name.startswith('-') or repo_name.endswith('-'):
        return False
    
    # Check all chars are lowercase letters, numbers, or hyphens
    for char in repo_name:
        if not (char.islower() or char.isdigit() or char == '-'):
            return False
    
    return True

def is_valid_email(email):
    """
    Check if email is valid format.
    Simple check: must have @ and .
    """
    return '@' in email and '.' in email

def is_valid_github_username(username):
    """
    Check if github_username is valid.
    Rules: alphanumeric + hyphens only
           can't start with hyphen
           1-39 chars
    """
    if not username or len(username) < 1 or len(username) > 39:
        return False
    
    if username.startswith('-'):
        return False
    
    # Check all chars are alphanumeric or hyphens
    for char in username:
        if not (char.isalnum() or char == '-'):
            return False
    
    return True

def is_valid_member_role(role):
    """
    Check if member_role is either "admin" or "developer"
    """
    return role in ["admin", "developer"]

def validate_row(row, row_number):
    """
    Validate a single row from the CSV.
    
    Args:
        row: dict with keys like project_name, repo_name, etc.
        row_number: line number in CSV (for error reporting)
    
    Returns:
        (is_valid: bool, error_message: str or None)
    """
    # Check all required columns exist
    required_columns = ["project_name", "repo_name", "description", "members", "github_username", "member_roles", "member_email"]
    for col in required_columns:
        if col not in row or not row[col].strip():
            return False, f"Row {row_number}: Missing or empty required column '{col}'"
    
    # Strip whitespace from all values
    for key in row:
        row[key] = row[key].strip()
    
    # Validate repo_name
    if not is_valid_repo_name(row["repo_name"]):
        return False, f"Row {row_number}: Invalid repo_name '{row['repo_name']}'. Must be lowercase, alphanumeric with hyphens, 1-39 chars, can't start/end with hyphen"
    
    # Validate member_email
    if not is_valid_email(row["member_email"]):
        return False, f"Row {row_number}: Invalid email '{row['member_email']}'. Must contain @ and ."
    
    # Validate github_username
    if not is_valid_github_username(row["github_username"]):
        return False, f"Row {row_number}: Invalid github_username '{row['github_username']}'. Must be alphanumeric with hyphens, 1-39 chars, can't start with hyphen"
    
    # Validate member_roles
    if not is_valid_member_role(row["member_roles"]):
        return False, f"Row {row_number}: Invalid member_roles '{row['member_roles']}'. Must be 'admin' or 'developer'"
    
    return True, None

def check_for_duplicates(valid_rows):
    """
    Check if there are duplicate rows (same repo_name + github_username)
    """
    errors = []
    seen = set()
    
    for row in valid_rows:
        key = (row["repo_name"], row["github_username"])
        if key in seen:
            errors.append(f"Duplicate: repo_name '{row['repo_name']}' + github_username '{row['github_username']}' appears more than once")
        seen.add(key)
    
    return errors

def validate_csv(filename): #path to config.csv
    """
    Main validation function.
    Read CSV file, validate each row, check for duplicates.
    returns valid_rowsaand error_rows as a list of dicts 
    """
    valid_rows = []
    error_rows = []
    
    try:
        with open(filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            
            if reader.fieldnames is None:
                error_rows.append("ERROR: CSV file is empty")
                return valid_rows, error_rows

            print(f"\nValidating {filename}...")
            print("-" * 50)
            
            row_number = 1
            for row in reader:
                row_number += 1
                is_valid, error_message = validate_row(row, row_number)
                
                if is_valid:
                    valid_rows.append(row)
                    logging.info(f"Row {row_number}: ✓ valid")
                else:
                    error_rows.append(error_message)
                    logging.error(error_message)

            print("-" * 50)
            print(f"Validation complete: {len(valid_rows)} valid, {len(error_rows)} errors\n")
    
    except FileNotFoundError:
        error_rows.append(f"ERROR: File '{filename}' not found")
        return valid_rows, error_rows
    except Exception as e:
        error_rows.append(f"ERROR: Failed to read CSV: {e}")
        return valid_rows, error_rows
    
    # Check for duplicates in valid rows
    duplicate_errors = check_for_duplicates(valid_rows)
    if duplicate_errors:
        error_rows.extend(duplicate_errors)
        for error in duplicate_errors:
            logging.error(error)

        seen = set()
        valid_rows_filtered = []
        for row in valid_rows:
            key = (row["repo_name"], row["github_username"])
            if key not in seen:
                valid_rows_filtered.append(row)
                seen.add(key)
        valid_rows = valid_rows_filtered

    print("-" * 50)
    print(f"Validation complete: {len(valid_rows)} valid, {len(error_rows)} errors\n")
        
    
    return valid_rows, error_rows