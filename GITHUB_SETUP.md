# Creating the GitHub Repository

I can't create or push to a GitHub account on your behalf — you'll need to do this
part yourself, but it's 5 commands. From inside the `expense_tracker` folder:

```bash
git init
git add .
git commit -m "Expense tracker: CLI app with validation, tests, and README"
git branch -M main
git remote add origin https://github.com/<your-username>/expense-tracker.git
git push -u origin main
```

If you don't have a repo created yet on GitHub:
1. Go to github.com → New repository → name it `expense-tracker` (or similar) → Create (don't initialize with a README, since you already have one)
2. Copy the repository URL it gives you and use it in the `git remote add origin ...` command above

Once pushed, the repo URL to submit will look like:
`https://github.com/<your-username>/expense-tracker`

Files to make sure are in the repo root:
- expense_tracker.py
- test_expense_tracker.py
- README.md
