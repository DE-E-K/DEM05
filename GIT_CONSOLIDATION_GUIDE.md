# Git Repository Consolidation Guide

This guide helps you consolidate your DEM05 project branches into a single, well-organized repository.

## 📋 Current Branch Structure

Based on your setup, you have:

- `main` (or `master`) - Main branch
- `tmdb_project` - TMDB project work
- `python_impl` - Python/Pandas implementation
- `spark_impl` - Spark implementation  
- `streaming` - Real-time streaming project

## 🎯 Goal

Merge all branches into `main` while maintaining the following structure:

```
DEM05/
├── README.md                    # Main module overview
├── TMDB-project/
│   ├── README.md
│   ├── Python-impl/
│   └── Spark-impl/
└── Real_streaming/
```

## 🚀 Step-by-Step Consolidation

### Step 1: Backup Your Work

```bash
# Navigate to your project directory
cd DEM05

# Create a backup branch
git checkout main
git branch backup-before-consolidation
```

### Step 2: Ensure All Branches Are Up to Date

```bash
# Fetch all remote branches
git fetch --all

# Check all branches
git branch -a
```

### Step 3: Create New Main Branch Structure

Create the folder structure if it doesn't exist:

```bash
# On main branch
git checkout main

# Create directories
mkdir -p TMDB-project/Python-impl
mkdir -p TMDB-project/Spark-impl
mkdir -p Real_streaming
```

### Step 4: Merge Streaming Branch

```bash
# Switch to streaming branch
git checkout streaming

# Check the structure
ls

# Switch back to main
git checkout main

# Merge streaming branch into Real_streaming folder
git checkout streaming -- .
mkdir -p Real_streaming
# Manually move streaming files to Real_streaming/ if needed

# OR use subtree merge strategy
git checkout main
git read-tree --prefix=Real_streaming/ -u streaming

git commit -m "Merge streaming branch into Real_streaming folder"
```

### Step 5: Merge Python Implementation

```bash
# Checkout python_impl branch
git checkout python_impl

# Switch back to main
git checkout main

# Merge into TMDB-project/Python-impl/
git read-tree --prefix=TMDB-project/Python-impl/ -u python_impl

git commit -m "Merge python_impl branch into TMDB-project/Python-impl folder"
```

### Step 6: Merge Spark Implementation

```bash
# Checkout spark_impl branch
git checkout spark_impl

# Switch back to main
git checkout main

# Merge into TMDB-project/Spark-impl/
git read-tree --prefix=TMDB-project/Spark-impl/ -u spark_impl

git commit -m "Merge spark_impl branch into TMDB-project/Spark-impl folder"
```

### Step 7: Add Main READMEs

```bash
# Ensure you have the main README files
git add README.md
git add TMDB-project/README.md
git commit -m "Add comprehensive module and project READMEs"
```

### Step 8: Push to Remote

```bash
# Push consolidated main branch
git push origin main --force-with-lease

# Verify on GitHub
```

## 🔄 Alternative Approach: Fresh Consolidation

If you want a cleaner approach without complex merges:

### Option A: Manual Reorganization

```bash
# Create a new branch for consolidation
git checkout main
git checkout -b consolidation

# Copy files manually to correct locations
# From your local workspace, structure is already correct

# Add all files
git add .
git commit -m "Consolidate all projects into structured repository"

# Merge to main
git checkout main
git merge consolidation

# Push
git push origin main
```

### Option B: Using Current Local Structure

Since your local files are already organized correctly:

```bash
# Ensure you're on main
git checkout main

# Add all files in current structure
git add .

# Check what will be committed
git status

# Commit everything
git commit -m "Consolidate DEM05 module: TMDB projects and streaming pipeline"

# Push to GitHub
git push origin main
```

## 📤 Push All Branches (Optional)

If you want to keep individual branches on GitHub:

```bash
# Push each branch
git push origin tmdb_project
git push origin python_impl
git push origin spark_impl
git push origin streaming
```

## 🧹 Clean Up (After Successful Consolidation)

Once you've verified everything is correct on GitHub:

```bash
# Delete local branches (optional)
git branch -d tmdb_project
git branch -d python_impl
git branch -d spark_impl
git branch -d streaming

# Delete remote branches (optional)
git push origin --delete tmdb_project
git push origin --delete python_impl
git push origin --delete spark_impl
git push origin --delete streaming
```

## ✅ Verification Checklist

After consolidation, verify:

- [ ] All files are in correct folders
- [ ] README.md exists at root level
- [ ] TMDB-project/README.md exists
- [ ] Both TMDB implementations are complete
- [ ] Real_streaming project is complete
- [ ] All documentation files are preserved
- [ ] requirements.txt files are in correct locations
- [ ] GitHub repository shows correct structure
- [ ] All commits are pushed

## 🎯 Recommended Git Workflow Going Forward

```bash
# Main branch structure
main/
├── README.md
├── TMDB-project/
│   ├── README.md
│   ├── Python-impl/
│   └── Spark-impl/
└── Real_streaming/
```

For future work:

```bash
# Create feature branches from main
git checkout main
git checkout -b feature/tmdb-enhancements

# Make changes
# ...

# Commit and push
git add .
git commit -m "Add enhancement to TMDB analysis"
git push origin feature/tmdb-enhancements

# Create pull request on GitHub
# Merge to main after review
```

## 🚨 Troubleshooting

### Problem: Merge Conflicts

```bash
# If you encounter conflicts
git status  # Check conflicting files

# Edit files to resolve conflicts
# Then:
git add <resolved-file>
git commit -m "Resolve merge conflicts"
```

### Problem: Wrong Files in Wrong Folders

```bash
# Move files using git
git mv source_path destination_path
git commit -m "Reorganize file structure"
```

### Problem: Want to Start Over

```bash
# Go back to backup
git checkout backup-before-consolidation
git branch -D main  # Delete main branch
git checkout -b main  # Create fresh main
```

## 📝 Recommended Commit Messages

```bash
# Initial consolidation
git commit -m "feat: Consolidate DEM05 module structure

- Add main module README with project overviews
- Organize TMDB project with Python and Spark implementations
- Structure streaming project with docs and tests
- Include all deliverables and documentation"

# Individual merges
git commit -m "merge: Integrate streaming project into Real_streaming/"
git commit -m "merge: Add Python implementation to TMDB-project/"
git commit -m "merge: Add Spark implementation to TMDB-project/"
git commit -m "docs: Add comprehensive module documentation"
```

## 🎓 Best Practices

1. **Keep main branch clean** - Only merge tested, working code
2. **Use descriptive commits** - Explain what and why
3. **Tag releases** - Mark important milestones
4. **Update READMEs** - Keep documentation current
5. **Test before pushing** - Ensure everything works
6. **Use .gitignore** - Exclude unnecessary files

## 📚 Additional Git Commands

```bash
# View commit history
git log --oneline --graph --all

# See changes
git diff

# Undo last commit (keep changes)
git reset --soft HEAD~1

# View remote status
git remote -v

# Create tag for submission
git tag -a v1.0-submission -m "DEM05 Module Submission"
git push origin v1.0-submission
```

## 🎉 Final Steps

After consolidation:

1. ✅ Verify structure on GitHub
2. ✅ Test that all code runs
3. ✅ Update any hardcoded paths
4. ✅ Create a release/tag for submission
5. ✅ Share repository link with instructor

---

**Questions?** Review Git documentation or reach out for help!

**Repository**: https://github.com/DE-E-K/DEM05.git
