# Simple test to check models
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession

# Authenticate
$authResponse = Invoke-WebRequest -Uri "http://localhost:8000/auth/token" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"token": "sample_token_1"}' -WebSession $session
Write-Host "Auth: $($authResponse.StatusCode)"

# Scan email
$scanResponse = Invoke-WebRequest -Uri "http://localhost:8000/scan/email" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"email_text": "Your account has been suspended. Click here to verify: http://fake-bank.tk/verify"}' -WebSession $session
Write-Host "Scan: $($scanResponse.StatusCode)"

# Parse results
$scanData = $scanResponse.Content | ConvertFrom-Json
Write-Host "Models found: $($scanData.results.Count)"

foreach ($result in $scanData.results) {
    Write-Host "$($result.model_name): $($result.decision) ($([math]::Round($result.confidence * 100, 1))%)"
} 