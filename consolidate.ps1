# DEM05 Module - Quick Consolidation Script

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  DEM05 Repository Consolidation Script" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in a git repository
if (-not (Test-Path ".git")) {
    Write-Host "Error: Not a git repository!" -ForegroundColor Red
    Write-Host "Please run this script from your DEM05 project root." -ForegroundColor Yellow
    exit 1
}

Write-Host "Step 1: Creating backup branch..." -ForegroundColor Green
git checkout main 2>$null
if ($LASTEXITCODE -ne 0) {
    git checkout master
    git branch -m master main
}
git branch backup-$(Get-Date -Format "yyyy-MM-dd-HHmmss") 2>$null

Write-Host "Step 2: Checking current structure..." -ForegroundColor Green
$hasTMDB = Test-Path "TMDB-project"
$hasStreaming = Test-Path "Real_streaming"

if ($hasTMDB -and $hasStreaming) {
    Write-Host "✓ Project structure looks good!" -ForegroundColor Green
} else {
    Write-Host "⚠ Warning: Expected folder structure not found" -ForegroundColor Yellow
    Write-Host "Expected: TMDB-project/ and Real_streaming/" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 3: Checking for important files..." -ForegroundColor Green

$files = @(
    "README.md",
    "TMDB-project/README.md",
    "TMDB-project/Python-impl/requirements.txt",
    "TMDB-project/Spark-impl/requirements.txt",
    "Real_streaming/requirements.txt",
    "Real_streaming/README.md"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file (missing)" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Step 4: Adding all files to git..." -ForegroundColor Green
git add .

Write-Host ""
Write-Host "Step 5: Checking git status..." -ForegroundColor Green
git status --short

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Ready to commit!" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

$commit = Read-Host "Do you want to commit these changes? (y/n)"

if ($commit -eq "y" -or $commit -eq "Y") {
    Write-Host ""
    Write-Host "Committing changes..." -ForegroundColor Green
    git commit -m "feat: Consolidate DEM05 module structure

- Add main module README with comprehensive overview
- Organize TMDB project with Python and Spark implementations  
- Structure streaming project with complete documentation
- Include all deliverables and documentation
- Add .gitignore for Python and Spark projects
- Include Git consolidation guide"

    Write-Host ""
    Write-Host "✓ Changes committed!" -ForegroundColor Green
    Write-Host ""
    
    $push = Read-Host "Do you want to push to GitHub? (y/n)"
    
    if ($push -eq "y" -or $push -eq "Y") {
        Write-Host ""
        Write-Host "Pushing to GitHub..." -ForegroundColor Green
        git push origin main
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "==================================================" -ForegroundColor Green
            Write-Host "  ✓ Successfully pushed to GitHub!" -ForegroundColor Green
            Write-Host "==================================================" -ForegroundColor Green
            Write-Host ""
            Write-Host "View your repository at:" -ForegroundColor Cyan
            Write-Host "https://github.com/DE-E-K/DEM05" -ForegroundColor Blue
        } else {
            Write-Host ""
            Write-Host "⚠ Push failed. Please check your credentials and try:" -ForegroundColor Yellow
            Write-Host "  git push origin main" -ForegroundColor White
        }
    }
} else {
    Write-Host ""
    Write-Host "Commit cancelled. You can commit manually with:" -ForegroundColor Yellow
    Write-Host "  git commit -m 'Your message here'" -ForegroundColor White
    Write-Host "  git push origin main" -ForegroundColor White
}

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "1. Verify structure on GitHub" -ForegroundColor White
Write-Host "2. Test that all code runs properly" -ForegroundColor White
Write-Host "3. Create a release tag: git tag v1.0-submission" -ForegroundColor White
Write-Host "4. Push tag: git push origin v1.0-submission" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see: GIT_CONSOLIDATION_GUIDE.md" -ForegroundColor Cyan
Write-Host ""
