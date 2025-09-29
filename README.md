# GitHub Repository Analyzer

[![Build Status](https://app.travis-ci.com/parthkishan20/hw03a.svg?token=UxxCxyrzFEycY3FKUe5H&branch=main)](https://app.travis-ci.com/parthkishan20/hw03a)

## What This Program Does

This program connects to GitHub's website and collects information about a user's code projects (called repositories). For each project, it counts how many times the user has saved their work (called commits). Think of it like counting how many times someone has saved a document while working on it.

## Quick Start Guide

### Step 1: Get the Code
Download this program to your computer by typing this in your terminal:
```bash
git clone https://github.com/parthkishan20/hw03a.git
cd hw03a
```

### Step 2: Install Required Tools
Install the tools this program needs:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Program
Try it out with the interactive demo:
```bash
python demo.py
```

The program will ask if you want to continue. Type `y` and press Enter to see it work!

## Example: What You'll See

When you run the program, it shows results like this:
```
Repo: my-website Number of commits: 15
Repo: calculator-app Number of commits: 8
Repo: game-project Number of commits: 23

Summary:
- Total repositories: 3
- Total commits: 46
- Average commits per repo: 15.3
```

## How to Test the Program

Make sure everything works correctly by running these tests:
```bash
python -m pytest tests/ -v
```

This checks that all parts of the program work as expected. You should see "PASSED" next to each test.

## Design Decisions and Testing Strategy

### What I Focused on When Writing This Code

**1. Easy Testing**
I split the program into small, independent pieces so each part can be tested separately. It's like testing each ingredient before making a cake.

**2. Handling Problems Gracefully**
The internet can be unreliable, so I made the program handle common problems:
- When a user doesn't exist on GitHub
- When GitHub limits how many requests we can make
- When the internet connection is slow or fails

**3. Clear Separation of Tasks**
I created different classes for different jobs:
- `GitHubClient`: Talks to GitHub's website
- `GitHubAnalyzer`: Processes the information 
- `format_output`: Makes the results look nice

### Testing Challenges I Faced

**Challenge 1: Testing Without Spam**
GitHub limits how many requests you can make per hour. To test my code without hitting this limit, I used "mock" objects that pretend to be GitHub but don't actually connect to the internet.

**Challenge 2: Testing Real Connections**
I still needed to test that my program actually works with real GitHub data. I created special "integration tests" that make real connections but only run when specifically requested.

**Challenge 3: Testing Error Situations**
I had to test what happens when things go wrong (like when a user doesn't exist). I created fake error situations to make sure my program handles them correctly.

**Solution: Dependency Injection**
I used a technique called "dependency injection" where I can easily swap real GitHub connections with fake ones during testing. This lets me test both the logic and the real connections separately.

### Why This Design Makes Testing Easier

1. **Small Functions**: Each function does one thing, so it's easy to test
2. **Clear Inputs and Outputs**: Functions take specific inputs and return predictable outputs
3. **Mocked External Services**: I can test without depending on GitHub being available
4. **Comprehensive Error Testing**: Every possible error situation is tested
5. **Continuous Integration**: Travis CI automatically runs all tests when code changes

The result is a program that's reliable, well-tested, and easy to modify or extend.

## Technical Details

**Programming Language**: Python 3.8+  
**Main Libraries Used**: 
- `requests` - for connecting to GitHub
- `pytest` - for testing the code
- `typing` - for clearer code documentation

**Files in This Project**:
- `src/github_api.py` - Main program logic
- `demo.py` - Interactive demonstration  
- `tests/test_github_api.py` - All the tests
- `.travis.yml` - Automatic testing configuration

## Project Requirements Met

✅ **Complete Program**: Fetches GitHub repository and commit data  
✅ **Demonstrates Correct Results**: Shows repository names and commit counts  
✅ **Travis CI Integration**: Automatic testing on code changes  
✅ **Build Badge**: Green badge shows tests are passing  
✅ **Comprehensive Testing**: 19 tests covering all functionality

## Repository Information

**GitHub URL**: https://github.com/parthkishan20/hw03a  
**Assignment**: SSW567 - Software Testing  
**Author**: Parth Patel

This project demonstrates professional software development practices including unit testing, continuous integration, and clean code architecture.



Design and Testing Reflection
When designing this project, the main focus was making the code easy to test and maintain. To achieve this, the program was structured so that each part has a clear and simple responsibility — such as fetching data from GitHub, processing that data, and formatting the output separately. This separation helps testers write precise tests for each component independently.

Input validation was carefully implemented to catch errors early, and the functions return structured data instead of printing directly. This design choice makes it straightforward to compare expected results with actual ones during testing. Additionally, custom error handling was added to manage cases like invalid users or network problems, helping tests check for specific errors rather than generic failures.

Testing this project posed some challenges, primarily due to GitHub's API rate limits, which restrict the number of requests that can be made in a short period. To overcome this, most tests use mocking techniques that simulate API responses without making real network calls. Only a few integration tests connect to the live API, and these are run sparingly to avoid exceeding limits.

Another challenge was the dynamic nature of GitHub data—repositories and commits change over time, so tests focus on verifying data structure and types rather than exact numbers. Handling these issues carefully ensures that the code is robust, reliable, and easy to maintain, illustrating the importance of thinking like both a developer and a tester.