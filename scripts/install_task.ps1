<#
    注册 Windows 计划任务：按固定间隔运行 run.py --once
    用法：
        powershell -ExecutionPolicy Bypass -File .\scripts\install_task.ps1
        powershell -ExecutionPolicy Bypass -File .\scripts\install_task.ps1 -IntervalMinutes 60
        powershell -ExecutionPolicy Bypass -File .\scripts\install_task.ps1 -PythonExe "D:\Anaconda3\pythonw.exe"
#>
param(
    [int]$IntervalMinutes = 30,
    [string]$TaskName = "xsyu-pushplus",
    [string]$PythonExe = ""
)

$ErrorActionPreference = "Stop"

$repo = Split-Path -Parent $PSScriptRoot
$script = Join-Path $repo "run.py"

if (-not (Test-Path $script)) {
    throw "找不到 $script，请在项目里的 scripts 目录下运行本脚本"
}

# 优先用 pythonw.exe：不弹黑框，后台静默跑
if (-not $PythonExe) {
    $pythonw = Get-Command pythonw.exe -ErrorAction SilentlyContinue
    if ($pythonw) {
        $PythonExe = $pythonw.Source
    } else {
        $python = Get-Command python.exe -ErrorAction SilentlyContinue
        if (-not $python) { throw "找不到 python.exe，请用 -PythonExe 指定完整路径" }
        $PythonExe = $python.Source
    }
}

Write-Host "Python : $PythonExe"
Write-Host "脚本   : $script"
Write-Host "间隔   : 每 $IntervalMinutes 分钟"
Write-Host "任务名 : $TaskName"

# 依赖检查：pythonw 拿不到退出码，用 python.exe 同步跑一次
$checkPy = $PythonExe -replace 'pythonw\.exe$', 'python.exe'
if (Test-Path $checkPy) {
    $proc = Start-Process -FilePath $checkPy -ArgumentList '-c "import requests, bs4, lxml, dotenv"' -Wait -PassThru -WindowStyle Hidden
    if ($proc.ExitCode -ne 0) {
        Write-Warning "依赖检查没过，请先执行：pip install -r requirements.txt"
    }
}

$action = New-ScheduledTaskAction -Execute $PythonExe -Argument "`"$script`" --once" -WorkingDirectory $repo
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(2) -RepetitionInterval (New-TimeSpan -Minutes $IntervalMinutes) -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Minutes 60)

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Description "西石大通知爬虫 + PushPlus 推送（pushplus-yu）" -Force | Out-Null

Start-ScheduledTask -TaskName $TaskName
Start-Sleep -Seconds 3
Get-ScheduledTask -TaskName $TaskName | Get-ScheduledTaskInfo | Select-Object TaskName, LastRunTime, LastTaskResult, NextRunTime | Format-List

Write-Host "已创建。日志：$repo\app.log" -ForegroundColor Green
Write-Host "删除任务：powershell -ExecutionPolicy Bypass -File .\scripts\uninstall_task.ps1" -ForegroundColor DarkGray

