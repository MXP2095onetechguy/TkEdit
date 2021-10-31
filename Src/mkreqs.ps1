#!/bin/pwsh

$Command = $(Get-Content mkreqs.sh | Out-String)
Invoke-Expression $Command