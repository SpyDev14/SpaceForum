$venvScriptPath = ".\.venv\Scripts\Activate.ps1"

if (Test-Path $venvScriptPath) {
    & $venvScriptPath
} else {
    Write-Host "������: �� ������ ���� ��������� ������������ ���������" -ForegroundColor Red
    Write-Host "���������, ��� ����������� ��������� ������� � ����� .venv" -ForegroundColor Yellow
    Write-Host "����� ������� ��� ��������: python -m venv .venv" -ForegroundColor Yellow
}