# GitHub API Mocking - HW03b

[![Build Status](https://app.travis-ci.com/parthkishan20/ssw-567-hw-03a.svg?token=UxxCxyrzFEycY3FKUe5H&branch=HW03a_Mocking)](https://app.travis-ci.com/parthkishan20/ssw-567-hw-03a)

## Assignment Overview

This branch (`HW03a_Mocking`) demonstrates the implementation of **API mocking** for the GitHub Repository Analyzer project. The goal was to eliminate external dependencies on the GitHub API during testing, ensuring consistent and reliable unit tests that run independently of network conditions or API rate limits.

## What Was Changed

### ✅ Mocked GitHub API Calls
- **No Real API Calls in Tests**: All HTTP requests to GitHub are mocked using `unittest.mock`
- **Consistent Test Results**: Tests run the same way every time, regardless of network or GitHub status
- **No Rate Limit Issues**: Eliminated Travis CI failures due to GitHub API rate limiting

### ✅ Comprehensive Mock Implementation
- **Repository Fetching**: Mocked `get_user_repositories()` with realistic JSON responses
- **Commit Counting**: Mocked `get_repository_commits()` with predefined commit data
- **Error Scenarios**: Mocked various error conditions (404, rate limits, network failures)
- **Edge Cases**: Mocked empty repositories, invalid users, and timeout scenarios

## Key Mocking Features

### 1. **Realistic Mock Data**
```python
# Example mock repository data
mock_repos = [
    {"name": "test-repo-1", "commits_url": "https://api.github.com/repos/user/test-repo-1/commits{/sha}"},
    {"name": "test-repo-2", "commits_url": "https://api.github.com/repos/user/test-repo-2/commits{/sha}"}
]
```

### 2. **Error Condition Testing**
- Mock 404 responses for non-existent users
- Mock rate limit exceeded scenarios  
- Mock network timeout conditions
- Mock malformed API responses

### 3. **Deterministic Results**
- Same test data every run
- Predictable commit counts
- Consistent error handling validation

## Running the Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests (no external API calls made)
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=src --cov-report=term-missing
```

## Mock Implementation Highlights

### Before (HW03a)
- Tests made real API calls to GitHub
- Failures due to rate limits in CI/CD
- Inconsistent results based on repo changes
- Network dependency issues

### After (HW03b - This Branch)
- **Zero external API calls** during testing
- **100% reliable** test execution in Travis CI
- **Consistent results** regardless of network conditions
- **Faster test execution** (no network delays)

## Technical Implementation

### Mocking Strategy
- Used `unittest.mock.patch` to intercept HTTP requests
- Created realistic mock responses based on actual GitHub API format
- Maintained original code structure (no changes to `src/github_api.py`)
- All mocking implemented in `tests/test_github_api.py`

### Mock Coverage
- ✅ User repository fetching
- ✅ Repository commit counting  
- ✅ Rate limit handling
- ✅ Error responses (404, timeouts)
- ✅ Edge cases (empty repos, malformed data)

## Files Modified for Mocking

1. **`tests/test_github_api.py`** - Added comprehensive mock implementations
2. **`README.md`** - Updated to reflect mocking implementation (this file)

**Note**: The core application code (`src/github_api.py`, `demo.py`) remains **unchanged** - only test implementations were modified.

## Assignment Requirements Met

✅ **Branch Strategy**: All changes on `HW03a_Mocking` branch  
✅ **No API Dependencies**: Zero external API calls during testing  
✅ **Travis CI Success**: Green build status with mocked tests  
✅ **Original Code Preserved**: Core application logic unchanged  
✅ **Comprehensive Mocking**: All GitHub API interactions mocked  

## Benefits Achieved

- **Reliable CI/CD**: No more random test failures due to API limits
- **Faster Tests**: No network delays in test execution  
- **Consistent Results**: Same outcomes every test run
- **Offline Testing**: Tests work without internet connection
- **Cost Effective**: No API quota consumption during testing

## Repository Information

**GitHub URL**: https://github.com/parthkishan20/ssw-567-hw-03a  
**Branch**: `HW03a_Mocking`  
**Assignment**: SSW567 HW03b - API Mocking  
**Author**: Parth Patel

This implementation demonstrates professional testing practices using mock objects to eliminate external dependencies and create reliable, maintainable unit tests.