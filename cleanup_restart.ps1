# Cleanup script for fresh experiment restart

Write-Host "🧹 Cleaning up old experiment files..." -ForegroundColor Yellow

# Remove old checkpoint and logs
Remove-Item "partA_checkpoint.json" -ErrorAction SilentlyContinue
Remove-Item "partA_progress.log" -ErrorAction SilentlyContinue
Remove-Item "partA_results.json" -ErrorAction SilentlyContinue

Write-Host "✓ Deleted old checkpoint and logs" -ForegroundColor Green

# Verify KB
$kbLines = (Get-Content "partA_kb.jsonl" | Measure-Object -Line).Lines
Write-Host "📊 KB size: $kbLines documents" -ForegroundColor Cyan

if ($kbLines -eq 480) {
    Write-Host "✓ KB has correct size (480 docs = 400 benign + 80 malicious)" -ForegroundColor Green
} else {
    Write-Host "⚠ Warning: Expected 480 docs, got $kbLines" -ForegroundColor Yellow
}

# Check for new attack types
$hasNewAttacks = Select-String -Path "partA_kb.jsonl" -Pattern "delimiter_attack|role_confusion" -Quiet
if ($hasNewAttacks) {
    Write-Host "✓ New attack types detected in KB" -ForegroundColor Green
} else {
    Write-Host "✗ Error: New attack types not found! Re-run: python generate_kb.py" -ForegroundColor Red
    exit 1
}

Write-Host "`n🚀 Ready to restart experiment!" -ForegroundColor Green
Write-Host "Run: python partA_experiment.py" -ForegroundColor Cyan
