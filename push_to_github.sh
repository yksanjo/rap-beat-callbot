#!/bin/bash
# Script to push rap-beat-callbot to GitHub
# Usage: ./push_to_github.sh YOUR_GITHUB_USERNAME

if [ -z "$1" ]; then
    echo "Usage: ./push_to_github.sh YOUR_GITHUB_USERNAME"
    echo ""
    echo "First, create the repository on GitHub:"
    echo "1. Go to https://github.com/new"
    echo "2. Repository name: rap-beat-callbot"
    echo "3. Description: Voice-enabled AI call bot for creating custom rap beats"
    echo "4. Choose Public or Private"
    echo "5. DO NOT initialize with README/gitignore/license"
    echo "6. Click Create repository"
    echo ""
    echo "Then run this script with your GitHub username"
    exit 1
fi

USERNAME=$1
REPO_NAME="rap-beat-callbot"

echo "🚀 Setting up GitHub repository..."
echo "Repository: https://github.com/${USERNAME}/${REPO_NAME}"

# Check if remote already exists
if git remote get-url origin &>/dev/null; then
    echo "⚠️  Remote 'origin' already exists. Updating..."
    git remote set-url origin https://github.com/${USERNAME}/${REPO_NAME}.git
else
    echo "➕ Adding remote origin..."
    git remote add origin https://github.com/${USERNAME}/${REPO_NAME}.git
fi

echo "📤 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Success! Your repository is now at:"
    echo "   https://github.com/${USERNAME}/${REPO_NAME}"
    echo ""
    echo "Share this link with your team!"
else
    echo ""
    echo "❌ Push failed. Make sure:"
    echo "   1. Repository exists on GitHub"
    echo "   2. You have push access"
    echo "   3. You're authenticated (use GitHub CLI or Personal Access Token)"
fi

