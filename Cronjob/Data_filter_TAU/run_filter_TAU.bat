@echo off
set LOG_DIR=D:\Above_the_spring_filtered_TAU\logs
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set LOG_FILE=%LOG_DIR%\filter_log.txt

echo. >> "%LOG_FILE%"
echo ======================================== >> "%LOG_FILE%"
echo Run started at: %date% %time% >> "%LOG_FILE%"
echo ======================================== >> "%LOG_FILE%"

powershell.exe -ExecutionPolicy Bypass -File "C:\Users\Jerusalem1_mini\Desktop\Cronjob_code\Data_filter_TAU\filtering_loop_TAU.ps1" >> "%LOG_FILE%" 2>&1 