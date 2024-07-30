#!/bin/python

import requests
import base64
import math


def is_user_profile_complete(username):
    # Example implementation - fetch user profile and check completeness
    profile_url = f"https://api.github.com/users/{username}"
    response = requests.get(profile_url)
    if response.status_code == 200:
        profile = response.json()
        return bool(profile.get('bio') and profile.get('location') and profile.get('email'))
    return False

def is_user_profile_partial(username):
    # Example implementation - fetch user profile and check for partial information
    profile_url = f"https://api.github.com/users/{username}"
    response = requests.get(profile_url)
    if response.status_code == 200:
        profile = response.json()
        return bool(profile.get('bio') or profile.get('location'))
    return False

def is_user_engaged(username):
    # Example implementation - check user activity or contributions
    contributions_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    response = requests.get(contributions_url)
    if response.status_code == 200:
        repos = response.json()
        return any(repo.get('forks_count', 0) > 5 for repo in repos)
    return False

def is_user_some_engaged(username):
    # Example implementation - check for some level of engagement
    contributions_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    response = requests.get(contributions_url)
    if response.status_code == 200:
        repos = response.json()
        return any(repo.get('forks_count', 0) > 1 for repo in repos)
    return False

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

# Function to fetch all pull requests from a repository
def fetch_pull_requests(repo_full_name):
    prs = {'generated': 0, 'merged': 0}
    page = 1
    while True:
        prs_url = f"https://api.github.com/repos/{repo_full_name}/pulls?state=all&per_page=100&page={page}"
        response = requests.get(prs_url)
        if response.status_code != 200:
            print(f"Error fetching pull requests for {repo_full_name}. Status code: {response.status_code}")
            break
        page_prs = response.json()
        if not page_prs:
            break
        prs['generated'] += len(page_prs)
        for pr in page_prs:
            if pr.get('state') == 'closed':
                prs['merged'] += 1
        page += 1
    return prs

# Function to check if a repository has regular pull requests
def has_regular_pull_requests(repo, min_prs=5):
    if repo is None:
        return False
    
    prs = fetch_all_pull_requests(repo['full_name'])
    return len(prs) >= min_prs

# Function to check if pull requests are merged
def has_merged_pull_requests(repo):
    if repo is None:
        return False
    
    prs = fetch_all_pull_requests(repo['full_name'])
    return any(pr.get('merged_at') for pr in prs)

# Function to check if a repository has forked repositories
def has_forked_repositories(repo):
    if repo is None:
        return False
    
    forks_url = f"https://api.github.com/repos/{repo['full_name']}/forks?per_page=100"
    response = requests.get(forks_url)
    if response.status_code == 200:
        forks = response.json()
        return len(forks) > 0  # Consider forked if there are any forks
    return False

# Function to fetch all forks and their PRs
def analyze_forks_and_prs(repos):
    forked_repos = 0
    pr_generated_count = 0
    pr_merged_count = 0

    for repo in repos:
        if repo is None:
            continue
        
        # Check if the repository is forked
        if repo.get('fork'):
            forked_repos += 1
        
        # Fetch PRs data
        prs = fetch_pull_requests(repo['full_name'])
        pr_generated_count += prs['generated']
        pr_merged_count += prs['merged']

    return forked_repos, pr_generated_count, pr_merged_count

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

def analyze_repositories(repos):
    total_repos = len(repos)
    diverse_languages = set()
    complex_projects = 0
    detailed_docs = 0
    best_practices_count = 0
    forked_repos, pr_generated_count, pr_merged_count = analyze_forks_and_prs(repos)
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
        if is_innovative_project(repo):
            innovative_projects += 1
        if is_high_impact_project(repo):
            high_impact_projects += 1

    return total_repos, diverse_languages, complex_projects, detailed_docs, best_practices_count, forked_repos, pr_generated_count, pr_merged_count, innovative_projects, high_impact_projects

def calculate_scores(total_repos, diverse_languages, complex_projects, detailed_docs, best_practices_count, forked_repos, pr_generated_count, pr_merged_count, innovative_projects, high_impact_projects, username):
    repo_count_score = 5 if total_repos >= 5 else (3 if total_repos >= 3 else 1)
    diversity_score = 10 if len(diverse_languages) >= 5 else (5 if len(diverse_languages) >= 3 else 2)
    complexity_score = 15 if complex_projects >= 3 else (10 if complex_projects >= 1 else 5)
    
    readability_score = 10 if detailed_docs >= 5 else (5 if detailed_docs >= 2 else 2)
    commenting_score = readability_score
    best_practices_score = 10 if best_practices_count >= 5 else (5 if best_practices_count >= 2 else 2)
    
    # Calculate PR scores
    forked_repos_score = min(10, 2 + 8 * math.log1p(forked_repos))  # Exponential increase
    pr_generated_score = min(10, 2 + 8 * math.log1p(pr_generated_count))  # Exponential increase
    pr_merged_score = min(10, 2 + 8 * math.log1p(pr_merged_count))  # Exponential increase
    
    originality_score = 10 if innovative_projects >= 3 else (5 if innovative_projects >= 1 else 2)
    impact_score = 10 if high_impact_projects >= 3 else (5 if high_impact_projects >= 1 else 2)

    profile_completeness_score = 5 if is_user_profile_complete(username) else 3 if is_user_profile_partial(username) else 1
    engagement_score = 5 if is_user_engaged(username) else 3 if is_user_some_engaged(username) else 1

    total_score = (repo_count_score + diversity_score + complexity_score + 
                   readability_score + commenting_score + best_practices_score + 
                   forked_repos_score + pr_generated_score + pr_merged_score + 
                   originality_score + impact_score + profile_completeness_score + 
                   engagement_score)
    return total_score

if __name__ == "__main__":
    username = "Priyansh-666"  # Replace with the GitHub username you want to check
    repos = get_repositories(username)
    total_repos, diverse_languages, complex_projects, detailed_docs, best_practices_count, forked_repos, pr_generated_count, pr_merged_count, innovative_projects, high_impact_projects = analyze_repositories(repos)
    score = calculate_scores(total_repos, diverse_languages, complex_projects, detailed_docs, best_practices_count, forked_repos, pr_generated_count, pr_merged_count, innovative_projects, high_impact_projects, username)
    
    # Print individual scores
    print(f"Total repositories: {total_repos}")
    print(f"Diverse languages: {len(diverse_languages)}")
    print(f"Complex projects: {complex_projects}")
    print(f"Detailed docs: {detailed_docs}")
    print(f"Best practices count: {best_practices_count}")
    print(f"Forked repositories: {forked_repos}")
    print(f"Pull requests generated: {pr_generated_count}")
    print(f"Pull requests merged: {pr_merged_count}")
    print(f"Innovative projects: {innovative_projects}")
    print(f"High impact projects: {high_impact_projects}")
    
    # Print final score
    print(f"The total score for {username} is: {score}")
