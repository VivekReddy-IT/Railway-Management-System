Write-Host "Starting Streamlit App..."
& "C:\Users\HP\AppData\Local\Microsoft\WindowsApps\python3.11.exe" -m streamlit run streamlit_app.py
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 