param(
    [Parameter(Mandatory=$true)]
    [string]$FilePath
)

# Check if the file exists
if (-not (Test-Path $FilePath)) {
    Write-Error "File not found: $FilePath"
    exit 1
}

# Define rclone path (adjust this path according to your rclone installation)
$rclonePath = "C:\Tools\rclone\rclone.exe"
$remote_name = "Meggido:"
$drive_directory = "Meggido_filtered"

# Execute rclone copy command
try {
    & $rclonePath copy $FilePath $remote_name$drive_directory
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Successfully copied file to Google Drive"
    } else {
        Write-Error "Failed to copy file. Rclone exit code: $LASTEXITCODE"
    }
} catch {
    Write-Error "An error occurred while copying the file: $_"
    exit 1
}
