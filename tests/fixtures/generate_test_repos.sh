#!/bin/bash

# This script creates a comprehensive set of test repositories for git and hg
# to test the VCS abstraction layer under various conditions.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
# Set the base directory for all test fixtures.
BASE_DIR="test_repos"
# Set a dummy user for the commits to keep them consistent.
export GIT_AUTHOR_NAME="Test User"
export GIT_AUTHOR_EMAIL="test@example.com"
export GIT_COMMITTER_NAME="Test User"
export GIT_COMMITTER_EMAIL="test@example.com"
export HGUSER="Test User <test@example.com>"


# --- Main ---
echo "Creating test repository fixtures in $BASE_DIR..."
# Clean up previous runs and create the base directories.
rm -rf "$BASE_DIR"
mkdir -p "$BASE_DIR/git" "$BASE_DIR/hg" "$BASE_DIR/not_a_repo"


# --- Git Repositories ---
echo "--- Generating Git Repositories ---"

# 1. Git: Clean, empty repo with no commits
echo "Creating git/clean_empty_repo_no_commits..."
DIR="$BASE_DIR/git/clean_empty_repo_no_commits"
mkdir -p "$DIR" && cd "$DIR"
git init -b main > /dev/null
cd - > /dev/null

# 2. Git: Clean repo with one committed file
echo "Creating git/clean_repo_one_committed_file..."
DIR="$BASE_DIR/git/clean_repo_one_committed_file"
mkdir -p "$DIR" && cd "$DIR"
git init -b main > /dev/null
echo "committed" > committed_file.txt
git add .
git commit -m "Initial commit" > /dev/null
cd - > /dev/null

# 3. Git: Dirty repo with one untracked file and no commits
echo "Creating git/dirty_repo_one_file_no_commits..."
DIR="$BASE_DIR/git/dirty_repo_one_file_no_commits"
mkdir -p "$DIR" && cd "$DIR"
git init -b main > /dev/null
echo "uncommitted" > uncommitted_file.txt
cd - > /dev/null

# 4. Git: Dirty repo with one committed and one untracked file
echo "Creating git/dirty_repo_two_files_one_committed..."
DIR="$BASE_DIR/git/dirty_repo_two_files_one_committed"
mkdir -p "$DIR" && cd "$DIR"
git init -b main > /dev/null
echo "committed" > committed_file.txt
git add .
git commit -m "Initial commit" > /dev/null
echo "uncommitted" > uncommitted_file.txt
cd - > /dev/null

# 5. Git: Dirty repo with modified, staged, and untracked files
echo "Creating git/dirty_repo_modified_and_staged..."
DIR="$BASE_DIR/git/dirty_repo_modified_and_staged"
mkdir -p "$DIR" && cd "$DIR"
git init -b main > /dev/null
echo "committed" > committed_file.txt
git add .
git commit -m "Initial commit" > /dev/null
echo "modified" >> committed_file.txt # Modified file
echo "staged" > staged_file.txt
git add staged_file.txt # Staged file
echo "untracked" > untracked_file.txt # Untracked file
cd - > /dev/null

# 6. Git: Clean repo on a feature branch
echo "Creating git/clean_repo_on_feature_branch..."
DIR="$BASE_DIR/git/clean_repo_on_feature_branch"
mkdir -p "$DIR" && cd "$DIR"
git init -b main > /dev/null
git commit --allow-empty -m "Initial commit" > /dev/null
git checkout -b feature-branch > /dev/null
echo "feature" > feature_file.txt
git add .
git commit -m "Commit on feature branch" > /dev/null
cd - > /dev/null

# 7. Git: Repo with tags (for testing detached HEAD)
echo "Creating git/clean_repo_with_tags..."
DIR="$BASE_DIR/git/clean_repo_with_tags"
mkdir -p "$DIR" && cd "$DIR"
git init -b main > /dev/null
echo "first" > file.txt
git add .
git commit -m "Initial commit" > /dev/null
git tag "v1.0.0"
echo "second" >> file.txt
git add .
git commit -m "Second commit" > /dev/null
git tag "v1.1.0"
cd - > /dev/null


# --- Mercurial (hg) Repositories ---
echo "--- Generating Mercurial Repositories ---"

# 8. Hg: Clean, empty repo with no commits
echo "Creating hg/clean_empty_repo_no_commits..."
DIR="$BASE_DIR/hg/clean_empty_repo_no_commits"
mkdir -p "$DIR" && cd "$DIR"
hg init > /dev/null
cd - > /dev/null

# 9. Hg: Clean repo with one committed file
echo "Creating hg/clean_repo_one_committed_file..."
DIR="$BASE_DIR/hg/clean_repo_one_committed_file"
mkdir -p "$DIR" && cd "$DIR"
hg init > /dev/null
echo "committed" > committed_file.txt
hg add
hg commit -m "Initial commit" > /dev/null
cd - > /dev/null

# 10. Hg: Dirty repo with one untracked file and no commits
echo "Creating hg/dirty_repo_one_file_no_commits..."
DIR="$BASE_DIR/hg/dirty_repo_one_file_no_commits"
mkdir -p "$DIR" && cd "$DIR"
hg init > /dev/null
echo "uncommitted" > uncommitted_file.txt
cd - > /dev/null

# 11. Hg: Dirty repo with one committed and one untracked file
echo "Creating hg/dirty_repo_two_files_one_committed..."
DIR="$BASE_DIR/hg/dirty_repo_two_files_one_committed"
mkdir -p "$DIR" && cd "$DIR"
hg init > /dev/null
echo "committed" > committed_file.txt
hg add
hg commit -m "Initial commit" > /dev/null
echo "uncommitted" > uncommitted_file.txt
cd - > /dev/null

# 12. Hg: Dirty repo with modified, staged, and untracked files
echo "Creating hg/dirty_repo_modified_and_staged..."
DIR="$BASE_DIR/hg/dirty_repo_modified_and_staged"
mkdir -p "$DIR" && cd "$DIR"
hg init > /dev/null
echo "committed" > committed_file.txt
hg add
hg commit -m "Initial commit" > /dev/null
echo "modified" >> committed_file.txt # Modified file
echo "staged" > staged_file.txt
hg add # Staged file
echo "untracked" > untracked_file.txt # Untracked file
cd - > /dev/null

# 13. Hg: Clean repo on a feature branch
echo "Creating hg/clean_repo_on_feature_branch..."
DIR="$BASE_DIR/hg/clean_repo_on_feature_branch"
mkdir -p "$DIR" && cd "$DIR"
hg init > /dev/null
hg branch default > /dev/null
echo "initial" > file.txt
hg add
hg commit -m "Initial commit" > /dev/null
hg branch feature-branch > /dev/null
echo "feature" > feature_file.txt
hg add
hg commit -m "Commit on feature branch" > /dev/null
cd - > /dev/null


# --- Non-Repository ---
echo "--- Generating Non-Repository Directory ---"
echo "Creating not_a_repo..."
echo "This is just a random file." > "$BASE_DIR/not_a_repo/a_random_file.txt"



# Package into a single archive for inclusion in tests.
rm -f test_repos.tar.bz2
echo "Packaging all test repositories into test_repos.tar.bz2..."
tar jcf test_repos.tar.bz2 test_repos

echo "Done."