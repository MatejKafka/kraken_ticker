cd $PSScriptRoot

$DisableVenv = $false
if (-not $env:VIRTUAL_ENV -and (Test-Path .\venv\Scripts\Activate.ps1)) {
	.\venv\Scripts\Activate.ps1
	$DisableVenv = $true
}

try {
	py -m src "ETH" "EUR" 1.0
} finally {
	if ($DisableVenv) {
		deactivate
	}
}