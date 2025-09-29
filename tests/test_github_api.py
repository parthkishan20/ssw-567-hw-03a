import json
import os
# Import our modules (adjust path as needed)
import sys
from unittest.mock import MagicMock, Mock, patch

import pytest
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from github_api import (GitHubAnalyzer, GitHubAPIError, GitHubClient,
                        RateLimitError, format_output)


class TestGitHubClient:

    def setup_method(self):
        self.client = GitHubClient()

    def test_client_initialization_default(self):
        client = GitHubClient()
        assert client.base_url == "https://api.github.com"
        assert client.timeout == 10
        assert isinstance(client.session, requests.Session)

    def test_client_initialization_custom(self):
        custom_session = requests.Session()
        client = GitHubClient(
            base_url="https://custom.api.com/", session=custom_session, timeout=30
        )
        assert client.base_url == "https://custom.api.com"
        assert client.session == custom_session
        assert client.timeout == 30

    @patch("requests.Session.get")
    def test_get_user_repositories_success(self, mock_get):
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"name": "repo1", "description": "First repo"},
            {"name": "repo2", "description": "Second repo"},
        ]
        mock_response.headers = {"X-RateLimit-Remaining": "4999"}
        mock_get.return_value = mock_response

        result = self.client.get_user_repositories("testuser")

        # Assertions
        assert len(result) == 2
        assert result[0]["name"] == "repo1"
        assert result[1]["name"] == "repo2"
        mock_get.assert_called_once_with(
            "https://api.github.com/users/testuser/repos", timeout=10
        )

    @patch("requests.Session.get")
    def test_get_user_repositories_not_found(self, mock_get):
        """Test handling of user not found (404)"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.headers = {"X-RateLimit-Remaining": "4999"}
        mock_get.return_value = mock_response

        with pytest.raises(GitHubAPIError, match="User 'nonexistentuser' not found"):
            self.client.get_user_repositories("nonexistentuser")

    @patch("requests.Session.get")
    def test_get_user_repositories_rate_limit(self, mock_get):
        """Test handling of rate limit exceeded"""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.headers = {
            "X-RateLimit-Remaining": "0",
            "X-RateLimit-Reset": "1640995200",
        }
        mock_get.return_value = mock_response

        with pytest.raises(RateLimitError, match="Rate limit exceeded"):
            self.client.get_user_repositories("testuser")

    @patch("requests.Session.get")
    def test_get_user_repositories_timeout(self, mock_get):
        """Test handling of request timeout"""
        mock_get.side_effect = requests.exceptions.Timeout()

        with pytest.raises(GitHubAPIError, match="Timeout while fetching repositories"):
            self.client.get_user_repositories("testuser")

    @patch("requests.Session.get")
    def test_get_repository_commits_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"sha": "abc123", "commit": {"message": "First commit"}},
            {"sha": "def456", "commit": {"message": "Second commit"}},
            {"sha": "ghi789", "commit": {"message": "Third commit"}},
        ]
        mock_response.headers = {"X-RateLimit-Remaining": "4998"}
        mock_get.return_value = mock_response

        result = self.client.get_repository_commits("testuser", "testrepo")

        assert len(result) == 3
        assert result[0]["sha"] == "abc123"
        mock_get.assert_called_once_with(
            "https://api.github.com/repos/testuser/testrepo/commits", timeout=10
        )

    @patch("requests.Session.get")
    def test_get_repository_commits_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.headers = {"X-RateLimit-Remaining": "4998"}
        mock_get.return_value = mock_response

        with pytest.raises(
            GitHubAPIError, match="Repository 'testuser/nonexistent' not found"
        ):
            self.client.get_repository_commits("testuser", "nonexistent")

    @patch("requests.Session.get")
    def test_get_repository_commits_network_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")

        with pytest.raises(GitHubAPIError, match="Network error"):
            self.client.get_repository_commits("testuser", "testrepo")


class TestGitHubAnalyzer:

    def test_analyzer_initialization_default(self):
        """Test analyzer initializes with default client"""
        analyzer = GitHubAnalyzer()
        assert isinstance(analyzer.client, GitHubClient)

    def test_analyzer_initialization_custom_client(self):
        """Test analyzer initializes with custom client"""
        custom_client = GitHubClient()
        analyzer = GitHubAnalyzer(client=custom_client)
        assert analyzer.client == custom_client

    def test_get_user_repo_commit_info_success(self):
        # Create mock client
        mock_client = Mock()

        # Mock repository data
        mock_client.get_user_repositories.return_value = [
            {"name": "repo1", "description": "First repo"},
            {"name": "repo2", "description": "Second repo"},
        ]

        # Mock commit data
        mock_client.get_repository_commits.side_effect = [
            [{"sha": "abc"}, {"sha": "def"}],  # 2 commits for repo1
            [{"sha": "ghi"}, {"sha": "jkl"}, {"sha": "mno"}],  # 3 commits for repo2
        ]

        analyzer = GitHubAnalyzer(client=mock_client)
        result = analyzer.get_user_repo_commit_info("testuser")

        # Assertions
        assert len(result) == 2
        assert result[0] == {"repo_name": "repo1", "commit_count": 2}
        assert result[1] == {"repo_name": "repo2", "commit_count": 3}

        # Verify client methods were called correctly
        mock_client.get_user_repositories.assert_called_once_with("testuser")
        assert mock_client.get_repository_commits.call_count == 2

    def test_get_user_repo_commit_info_empty_repositories(self):
        mock_client = Mock()
        mock_client.get_user_repositories.return_value = []

        analyzer = GitHubAnalyzer(client=mock_client)
        result = analyzer.get_user_repo_commit_info("emptyuser")

        assert result == []

    def test_get_user_repo_commit_info_commit_error_handling(self):
        mock_client = Mock()

        # Mock repository data
        mock_client.get_user_repositories.return_value = [
            {"name": "repo1", "description": "First repo"},
            {"name": "repo2", "description": "Second repo"},
        ]

        # Mock commit data - first succeeds, second fails
        mock_client.get_repository_commits.side_effect = [
            [{"sha": "abc"}, {"sha": "def"}],  # 2 commits for repo1
            GitHubAPIError("Repository not accessible"),  # Error for repo2
        ]

        analyzer = GitHubAnalyzer(client=mock_client)

        # Capture printed output
        with patch("builtins.print") as mock_print:
            result = analyzer.get_user_repo_commit_info("testuser")

        # Should still return data for successful repo, with 0 commits for failed repo
        assert len(result) == 2
        assert result[0] == {"repo_name": "repo1", "commit_count": 2}
        assert result[1] == {"repo_name": "repo2", "commit_count": 0}

        # Should have printed warning
        mock_print.assert_called_once()
        assert "Warning: Could not get commits for repo2" in mock_print.call_args[0][0]


class TestFormatOutput:

    def test_format_output_multiple_repos(self):
        repo_info = [
            {"repo_name": "Triangle567", "commit_count": 10},
            {"repo_name": "Square567", "commit_count": 27},
        ]

        expected = "Repo: Triangle567 Number of commits: 10\nRepo: Square567 Number of commits: 27"
        assert format_output(repo_info) == expected

    def test_format_output_single_repo(self):
        repo_info = [{"repo_name": "SingleRepo", "commit_count": 5}]

        expected = "Repo: SingleRepo Number of commits: 5"
        assert format_output(repo_info) == expected

    def test_format_output_empty_list(self):
        repo_info = []
        expected = "No repositories found."
        assert format_output(repo_info) == expected

    def test_format_output_zero_commits(self):
        repo_info = [{"repo_name": "EmptyRepo", "commit_count": 0}]

        expected = "Repo: EmptyRepo Number of commits: 0"
        assert format_output(repo_info) == expected


class TestIntegration:

    @pytest.mark.integration
    def test_real_api_call_known_user(self):
        # Only run if explicitly requested to avoid rate limiting during regular tests
        client = GitHubClient()

        try:
            repos = client.get_user_repositories("octocat")
            assert isinstance(repos, list)
            assert len(repos) > 0

            # Test getting commits for first repo
            first_repo = repos[0]["name"]
            commits = client.get_repository_commits("octocat", first_repo)
            assert isinstance(commits, list)

        except RateLimitError:
            pytest.skip("Rate limit reached - skipping integration test")
        except GitHubAPIError:
            pytest.skip("API error - skipping integration test")


# Test configuration
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "integration: mark test as integration test (may hit real APIs)"
    )


if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__, "-v"])
