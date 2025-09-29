
import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from github_api import GitHubAnalyzer, GitHubAPIError, RateLimitError, format_output


def test_user(username):
    print(f"\n{'='*60}")
    print(f"Testing with user: {username}")
    print(f"{'='*60}")
    
    try:
        analyzer = GitHubAnalyzer()
        print(f"Fetching repositories for {username}...")
        
        repo_info = analyzer.get_user_repo_commit_info(username)
        
        if not repo_info:
            print(f"No repositories found for user: {username}")
        else:
            print(f"Found {len(repo_info)} repositories:\n")
            output = format_output(repo_info)
            print(output)
            
            # Summary statistics
            total_commits = sum(info['commit_count'] for info in repo_info)
            print(f"\nSummary:")
            print(f"- Total repositories: {len(repo_info)}")
            print(f"- Total commits: {total_commits}")
            print(f"- Average commits per repo: {total_commits / len(repo_info):.1f}")
        
    except RateLimitError as e:
        print(f"❌ Rate limit exceeded: {e}")
        print("💡 Tip: Wait a while or use a GitHub token for higher rate limits")
        
    except GitHubAPIError as e:
        print(f"❌ GitHub API error: {e}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def main():
    print("GitHub API Repository Information Extractor")
    print("Demonstration Script")
    
    # Test users - you can modify this list
    test_users = [
        "richkempinski",  # From assignment example
        "octocat",        # GitHub's mascot account
    ]
    
    print(f"\nThis will test {len(test_users)} users.")
    print(f"Each user requires 1 + N API calls (where N = number of repos)")
    print("GitHub rate limit: 60 requests/hour without authentication\n")
    
    # Ask for confirmation
    response = input("Continue? (y/n): ").strip().lower()
    if response != 'y':
        print("Cancelled.")
        return
    
    # Test each user
    for username in test_users:
        test_user(username)
        
        # Ask if user wants to continue with next user
        if username != test_users[-1]:  # Not the last user
            response = input(f"\nTest next user? (y/n): ").strip().lower()
            if response != 'y':
                break
    
    print(f"\n{'='*60}")
    print("Testing complete!")


if __name__ == "__main__":
    main()