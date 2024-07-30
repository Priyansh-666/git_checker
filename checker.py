#!/bin/python

import requests
import base64
import math

# Function to get all repositories of a user
def get_repositories(username):
    api_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    response = requests.get(api_url)
    
    if response.status_code != 200:
        print(f"Error: Unable to fetch repositories for {username}. Status code: {response.status_code}")
        return []
    
    return response.json()

# Function to check if a repository is complex based on its description
def is_complex_project(repo):
    if repo is None:
        return False
    
    description = repo.get('description', '')
    description = description.lower() if description else ''
    keywords = ['ai', 'machine learning', 'deep learning', 'complex algorithms']
    return any(keyword in description for keyword in keywords)

# Function to check if a repository has detailed documentation
def has_detailed_documentation(repo):
    if repo is None:
        return False
    
    readme_url = f"https://api.github.com/repos/{repo['full_name']}/readme"
    response = requests.get(readme_url)
    if response.status_code == 200:
        readme_content = response.json().get('content', '')
        if readme_content:
            readme_content = base64.b64decode(readme_content).decode('utf-8')
            return len(readme_content) > 1000  # Consider detailed if README is longer than 1000 bytes
    return False

# Function to check if a repository follows best practices
def follows_best_practices(repo):
    if repo is None:
        return False
    
    license_url = f"https://api.github.com/repos/{repo['full_name']}/license"
    contributing_url = f"https://api.github.com/repos/{repo['full_name']}/contents/CONTRIBUTING.md"
    license_response = requests.get(license_url)
    contributing_response = requests.get(contributing_url)
    return license_response.status_code == 200 and contributing_response.status_code == 200

# Function to fetch all commits from a repository
def fetch_all_commits(repo_full_name):
    commits = []
    page = 1
    while True:
        commits_url = f"https://api.github.com/repos/{repo_full_name}/commits?per_page=100&page={page}"
        response = requests.get(commits_url)
        if response.status_code == 404:
            break
        if response.status_code != 200:
            print(f"Error fetching commits for {repo_full_name}. Status code: {response.status_code}")
            break
        page_commits = response.json()
        if not page_commits:
            break
        commits.extend(page_commits)
        page += 1
    return commits

# Function to check if a repository has regular commits
def has_regular_commits(repo, min_commits=10):
    if repo is None:
        return False
    
    commits = fetch_all_commits(repo['full_name'])
    return len(commits) >= min_commits

# Function to check if a repository has collaborative contributions
def has_collaborative_contributions(repo):
    if repo is None:
        return False
    
    contributors_url = f"https://api.github.com/repos/{repo['full_name']}/contributors"
    response = requests.get(contributors_url)
    if response.status_code == 200:
        contributors = response.json()
        return len(contributors) > 1  # Consider collaborative if more than 1 contributor
    return False

# Function to check if a repository is innovative
def is_innovative_project(repo):
    if repo is None:
        return False
    
    description = repo.get('description', '')
    description = description.lower() if description else ''
    keywords = ['novel', 'unique', 'innovative', 'new approach']
    return any(keyword in description for keyword in keywords)

# Function to check if a repository is high impact
def is_high_impact_project(repo):
    if repo is None:
        return False
    
    description = repo.get('description', '')
    description = description.lower() if description else ''
    keywords = ['solves real problem', 'practical use', 'important']
    return any(keyword in description for keyword in keywords)

# Function to check if the profile is complete
def is_user_profile_complete(username):
    api_url = f"https://api.github.com/users/{username}"
    response = requests.get(api_url)
    if response.status_code == 200:
        user_data = response.json()
        return all([user_data.get('name'), user_data.get('email'), user_data.get('bio'), user_data.get('avatar_url')])
    return False

# Function to check if the profile is partially complete
def is_user_profile_partial(username):
    api_url = f"https://api.github.com/users/{username}"
    response = requests.get(api_url)
    if response.status_code == 200:
        user_data = response.json()
        return any([user_data.get('name'), user_data.get('email'), user_data.get('bio'), user_data.get('avatar_url')])
    return False

# Function to check if the user is engaged in the community
def is_user_engaged(username):
    api_url = f"https://api.github.com/users/{username}"
    response = requests.get(api_url)
    if response.status_code == 200:
        user_data = response.json()
        return user_data.get('followers', 0) > 0 or user_data.get('following', 0) > 0
    return False

# Function to check if the user has some community engagement
def is_user_some_engaged(username):
    api_url = f"https://api.github.com/users/{username}"
    response = requests.get(api_url)
    if response.status_code == 200:
        user_data = response.json()
        return user_data.get('followers', 0) > 0 or user_data.get('following', 0) > 0
    return False

def analyze_repositories(repos):
    total_repos = len(repos)
    diverse_languages = set()
    complex_projects = 0
    detailed_docs = 0
    best_practices_count = 0
    regular_commits_count = 0
    collab_contributions_count = 0
    innovative_projects = 0
    high_impact_projects = 0

    for repo in repos:
        if repo is None:
            continue
        
        languages = requests.get(repo['languages_url']).json()
        diverse_languages.update(languages.keys())

        # Check project complexity and documentation
        if is_complex_project(repo):
            complex_projects += 1
        if has_detailed_documentation(repo):
            detailed_docs += 1
        if follows_best_practices(repo):
            best_practices_count += 1
        if has_regular_commits(repo):
            regular_commits_count += 1
        if has_collaborative_contributions(repo):
            collab_contributions_count += 1
        if is_innovative_project(repo):
            innovative_projects += 1
        if is_high_impact_project(repo):
            high_impact_projects += 1

    return total_repos, diverse_languages, complex_projects, detailed_docs, best_practices_count, regular_commits_count, collab_contributions_count, innovative_projects, high_impact_projects

def calculate_scores(total_repos, diverse_languages, complex_projects, detailed_docs, best_practices_count, regular_commits_count, collab_contributions_count, innovative_projects, high_impact_projects, username):
    repo_count_score = 5 if total_repos >= 5 else (3 if total_repos >= 3 else 1)
    diversity_score = 10 if len(diverse_languages) >= 5 else (5 if len(diverse_languages) >= 3 else 2)
    complexity_score = 15 if complex_projects >= 3 else (10 if complex_projects >= 1 else 5)
    
    readability_score = 10 if detailed_docs >= 5 else (5 if detailed_docs >= 2 else 2)
    commenting_score = readability_score
    best_practices_score = 10 if best_practices_count >= 5 else (5 if best_practices_count >= 2 else 2)
    
    commit_frequency_score = min(10, 2 + 8 * math.log1p(regular_commits_count / 50))  # Exponential increase
    collaborative_work_score = min(10, 2 + 8 * math.log1p(collab_contributions_count / 5))  # Exponential increase
    
    originality_score = 10 if innovative_projects >= 3 else (5 if innovative_projects >= 1 else 2)
    impact_score = 10 if high_impact_projects >= 3 else (5 if high_impact_projects >= 1 else 2)

    profile_completeness_score = 5 if is_user_profile_complete(username) else 3 if is_user_profile_partial(username) else 1
    engagement_score = 5 if is_user_engaged(username) else 3 if is_user_some_engaged(username) else 1

    total_score = (repo_count_score + diversity_score + complexity_score + 
                   readability_score + commenting_score + best_practices_score + 
                   commit_frequency_score + collaborative_work_score + 
                   originality_score + impact_score + profile_completeness_score + 
                   engagement_score)
    return total_score

if __name__ == "__main__":
    username = "username"  # Replace with the GitHub username you want to check
    repos = get_repositories(username)
    total_repos, diverse_languages, complex_projects, detailed_docs, best_practices_count, regular_commits_count, collab_contributions_count, innovative_projects, high_impact_projects = analyze_repositories(repos)
    score = calculate_scores(total_repos, diverse_languages, complex_projects, detailed_docs, best_practices_count, regular_commits_count, collab_contributions_count, innovative_projects, high_impact_projects, username)
    
    # Print individual scores
    print(f"Total repositories: {total_repos}")
    print(f"Diverse languages: {len(diverse_languages)}")
    print(f"Complex projects: {complex_projects}")
    print(f"Detailed docs: {detailed_docs}")
    print(f"Best practices count: {best_practices_count}")
    print(f"Regular commits: {regular_commits_count}")
    print(f"Collaborative contributions: {collab_contributions_count}")
    print(f"Innovative projects: {innovative_projects}")
    print(f"High impact projects: {high_impact_projects}")
    
    # Print final score
    print(f"The total score for {username} is: {score}")
