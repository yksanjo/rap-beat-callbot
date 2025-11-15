# Setup GitHub Repository

## Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `rap-beat-callbot` (or your preferred name)
3. Description: "Voice-enabled AI call bot for creating custom rap beats using Soundraw API"
4. Choose: **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **"Create repository"**

## Step 2: Connect and Push

After creating the repository, GitHub will show you commands. Use these:

```bash
cd /Users/yoshikondo/awesome-generative-ai/rap-beat-callbot

# Add your GitHub repository as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/rap-beat-callbot.git

# Push to GitHub
git push -u origin main
```

## Alternative: Using SSH

If you prefer SSH:

```bash
git remote add origin git@github.com:YOUR_USERNAME/rap-beat-callbot.git
git push -u origin main
```

## Quick Setup Script

Or run this script (update YOUR_USERNAME first):

```bash
#!/bin/bash
USERNAME="YOUR_USERNAME"  # Change this!
REPO_NAME="rap-beat-callbot"

cd /Users/yoshikondo/awesome-generative-ai/rap-beat-callbot
git remote add origin https://github.com/${USERNAME}/${REPO_NAME}.git
git push -u origin main
```

## After Pushing

Your repository will be available at:
`https://github.com/YOUR_USERNAME/rap-beat-callbot`

Share this link with your team!

