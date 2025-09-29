# src/github_api.py

from typing import Dict, List, Optional, Union

import requests


class GitHubAPIError(Exception):
    pass


class RateLimitError(GitHubAPIError):
    pass


class GitHubClient:

    def __init__(
        self,
        base_url: str = "https://api.github.com",
        session: Optional[requests.Session] = None,
        timeout: int = 10,
    ):

        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self.timeout = timeout

    def get_user_repositories(self, username: str) -> List[Dict]:

        url = f"{self.base_url}/users/{username}/repos"

        try:
            response = self.session.get(url, timeout=self.timeout)
            self._handle_rate_limit(response)

            if response.status_code == 404:
                raise GitHubAPIError(f"User '{username}' not found")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            raise GitHubAPIError(f"Timeout while fetching repositories for {username}")
        except requests.exceptions.RequestException as e:
            raise GitHubAPIError(f"Network error: {str(e)}")

    def get_repository_commits(self, username: str, repo_name: str) -> List[Dict]:

        url = f"{self.base_url}/repos/{username}/{repo_name}/commits"

        try:
            response = self.session.get(url, timeout=self.timeout)
            self._handle_rate_limit(response)

            if response.status_code == 404:
                raise GitHubAPIError(f"Repository '{username}/{repo_name}' not found")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            raise GitHubAPIError(
                f"Timeout while fetching commits for {username}/{repo_name}"
            )
        except requests.exceptions.RequestException as e:
            raise GitHubAPIError(f"Network error: {str(e)}")

    def _handle_rate_limit(self, response: requests.Response) -> None:

        if response.status_code == 403:
            rate_limit_remaining = response.headers.get("X-RateLimit-Remaining", "0")
            if rate_limit_remaining == "0":
                reset_time = response.headers.get("X-RateLimit-Reset")
                raise RateLimitError(f"Rate limit exceeded. Reset time: {reset_time}")


class GitHubAnalyzer:

    def __init__(self, client: Optional[GitHubClient] = None):

        self.client = client or GitHubClient()

    def get_user_repo_commit_info(
        self, username: str
    ) -> List[Dict[str, Union[str, int]]]:

        # Get repositories
        repositories = self.client.get_user_repositories(username)

        if not repositories:
            return []

        results = []

        for repo in repositories:
            repo_name = repo["name"]

            try:
                # Get commits for each repository
                commits = self.client.get_repository_commits(username, repo_name)
                commit_count = len(commits)

                results.append({"repo_name": repo_name, "commit_count": commit_count})

            except GitHubAPIError as e:
                # Log error but continue with other repos
                print(f"Warning: Could not get commits for {repo_name}: {e}")
                results.append({"repo_name": repo_name, "commit_count": 0})

        return results


def format_output(repo_info: List[Dict[str, Union[str, int]]]) -> str:

    if not repo_info:
        return "No repositories found."

    lines = []
    for info in repo_info:
        lines.append(
            f"Repo: {info['repo_name']} Number of commits: {info['commit_count']}"
        )

    return "\n".join(lines)


def main():

    # Example usage
    username = "richkempinski"

    try:
        analyzer = GitHubAnalyzer()
        repo_info = analyzer.get_user_repo_commit_info(username)
        output = format_output(repo_info)
        print(output)

    except RateLimitError as e:
        print(f"Rate limit error: {e}")
    except GitHubAPIError as e:
        print(f"GitHub API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
