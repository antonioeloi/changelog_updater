#!/usr/bin/env python3

import inquirer
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime

# Constants
TICKET_PREFIX = "RAILS-"
DEFAULT_TICKET = f"{TICKET_PREFIX}XXXX"
CLICKUP_URL = "https://app.clickup.com/t/82723/"

def extract_ticket_id(branch_name):
    """Extract ticket ID from branch name or return default."""
    try:
        # Look for TICKET_PREFIX-XXXX pattern where X is a digit (4 or more digits)
        ticket_pattern = f"{TICKET_PREFIX}\\d{{4,}}"
        match = re.search(ticket_pattern, branch_name)
        if match:
            return match.group(0)

        # If no TICKET_PREFIX-XXXX pattern, look for any 4+ digit number
        number_match = re.search(r'\d{4,}', branch_name)
        if number_match:
            return f"{TICKET_PREFIX}{number_match.group(0)}"

        return DEFAULT_TICKET

    except Exception as e:
        print(f"Error extracting ticket ID: {e}")
        return DEFAULT_TICKET

def get_current_branch():
    try:
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                              capture_output=True,
                              text=True,
                              check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("Not in a git repository, using default ticket ID")
        return None
    except Exception as e:
        print(f"Unexpected error getting git branch: {e}")
        return None

def get_ticket_id():
    branch_name = get_current_branch()
    if not branch_name:
        return DEFAULT_TICKET

    return extract_ticket_id(branch_name)

def get_user_choices():
    questions = [
        inquirer.List('action',
                     message="What would you like to do?",
                     choices=['Hotfix', 'Nope'],
                     ),
    ]
    answers = inquirer.prompt(questions)

    if answers['action'] == 'Hotfix':
        change_type = [
            inquirer.List('type',
                         message="What type of change is this?",
                         choices=['Change', 'Feature', 'Fix', 'Remove'],
                         ),
        ]
        change_answer = inquirer.prompt(change_type)

        # Add message prompt
        message = [
            inquirer.Text('message',
                         message="Enter your changelog message:",
                         ),
        ]
        message_answer = inquirer.prompt(message)

        return answers['action'], change_answer['type'], message_answer['message']

    return answers['action'], None, None

def update_version_file(file_path):
    try:
        # Read current version
        with open(file_path, 'r') as f:
            current_version = f.read().strip()

        # Find the last number and increment it
        version_parts = current_version.split('.')
        if len(version_parts) > 0:
            last_number = int(version_parts[-1])
            version_parts[-1] = str(last_number + 1)
            new_version = '.'.join(version_parts)

            # Write new version
            with open(file_path, 'w') as f:
                f.write(new_version)

            print(f"Version updated from {current_version} to {new_version}")
            return new_version
    except Exception as e:
        print(f"Error updating version file: {e}")
        return None

def update_changelog(file_path, new_version, change_type, ticket_id, message):
    try:
        today = datetime.now().strftime('%Y-%m-%d')

        type_mapping = {
            'Change': 'Changed',
            'Feature': 'Added',
            'Fix': 'Fixed',
            'Remove': 'Removed'
        }

        section = type_mapping.get(change_type)
        new_entry = (
            f"## [{new_version}] - {today}\n\n"
            f"### {section}\n\n"
            f"- {message} - [#{ticket_id}]({CLICKUP_URL}{ticket_id})\n\n"
        )

        with open(file_path, 'r') as f:
            content = f.readlines()

        # Find the first version entry
        for i, line in enumerate(content):
            if re.match(r'^## \[\d+\.\d+\.\d+\.\d+\] - \d{4}-\d{2}-\d{2}', line.strip()):
                content.insert(i, new_entry)
                break

        # Write updated content back to file
        with open(file_path, 'w') as f:
            f.writelines(content)

        print(f"Added new changelog entry for version {new_version} with {section} section")
        return True
    except Exception as e:
        print(f"Error updating changelog: {e}")
        return False

## version ordering
def get_repo_url(content):
    """Extract repository URL from existing references."""
    for line in content:
        if line.startswith('['):
            # Match URL up to before /compare or /-/tree
            match = re.search(r'(https://[^/]+/[^/]+/[^/]+)(?:/compare|-/tree)', line)
            if match:
                return match.group(1)
    return None

def update_version_references(file_path, new_version):
    try:
        with open(file_path, 'r') as f:
            content = f.readlines()

        # Get repository URL from existing references
        repo_url = get_repo_url(content)
        if not repo_url:
            print("ERROR: Could not determine repository URL from existing references")
            return False

        # Check if versions use 'v' prefix by looking at existing references
        has_v_prefix = any(re.search(r'/v\d+\.\d+\.\d+', line) for line in content)
        version_prefix = 'v' if has_v_prefix else ''

        # Collect all version references, using a set to remove duplicates
        version_refs = set()
        start_index = None

        for i, line in enumerate(content):
            if line.startswith('[Unreleased]:'):
                start_index = i

            # Collect version references (without 'v' prefix)
            match = re.match(r'^\[([\d\.]+)\]:', line)
            if match:
                version_refs.add(match.group(1))

        # Convert to list and sort versions in descending order
        version_refs = sorted(list(version_refs),
                            key=lambda v: [int(x) for x in v.split('.')],
                            reverse=True)

        # Create new reference lines with correct version prefix
        new_refs = [
            f'[Unreleased]: {repo_url}/compare/{version_prefix}{new_version}...HEAD\n'
        ]

        # Add the new version reference if not already present
        if new_version not in version_refs:
            new_refs.append(
                f'[{new_version}]: {repo_url}/-/tree/{version_prefix}{new_version}\n'
            )

        # Add all other version references
        for version in version_refs:
            if version != new_version:  # Skip if it's the new version (already added)
                new_refs.append(
                    f'[{version}]: {repo_url}/-/tree/{version_prefix}{version}\n'
                )

        # Replace the old references section
        content = content[:start_index] + new_refs

        # Write back to file
        with open(file_path, 'w') as f:
            f.writelines(content)

        print("Version references updated and ordered (duplicates removed)")
        return True

    except Exception as e:
        print(f"Error updating version references: {e}")
        return False

def main():
    ticket_id = get_ticket_id()
    print(f"Working with ticket: {ticket_id}")

    choice, change_type, message = get_user_choices()

    if choice == 'Hotfix':
        # Check for VERSION and CHANGELOG.md files
        current_dir = os.getcwd()
        version_file = os.path.join(current_dir, 'VERSION')
        changelog_file = os.path.join(current_dir, 'CHANGELOG.md')

        if not os.path.exists(version_file):
            print("ERROR: VERSION file not found in current directory")
            return

        if not os.path.exists(changelog_file):
            print("ERROR: CHANGELOG.md file not found in current directory")
            return

        # Update version
        new_version = update_version_file(version_file)
        if new_version:
            # Update changelog with change type, ticket ID, and message
            if update_changelog(changelog_file, new_version, change_type, ticket_id, message):
                print("Hotfix version update completed")
                update_version_references(changelog_file, new_version)
            else:
                print("Failed to update changelog")
    else:
        print("Operation cancelled")

if __name__ == "__main__":
    main()