$SCRIPT_DIR = Split-Path $MyInvocation.MyCommand.Path -Parent

cd $SCRIPT_DIR
if (Test-Path .\venv\Scripts\Activate.ps1) {
	.\venv\Scripts\Activate.ps1
}
try {
	py -m src "ETH" "EUR" 1.0
} finally {
	deactivate # venv
}