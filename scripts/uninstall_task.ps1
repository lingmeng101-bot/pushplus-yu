<#
    删除计划任务
    用法：powershell -ExecutionPolicy Bypass -File .\scripts\uninstall_task.ps1
#>
param(
    [string]$TaskName = "xsyu-pushplus"
)

$ErrorActionPreference = "Stop"

$task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if (-not $task) {
    Write-Host "没有名为 $TaskName 的计划任务，无需删除。" -ForegroundColor Yellow
    return
}

Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
Write-Host "已删除计划任务 $TaskName" -ForegroundColor Green
