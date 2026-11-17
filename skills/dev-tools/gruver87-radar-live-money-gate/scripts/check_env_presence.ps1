# Presence-only check for radar .env — never prints secret values.
param([string]$RadarRoot = "")
$ErrorActionPreference = "Stop"
if (-not $RadarRoot) {
  $RadarRoot = Join-Path (Split-Path (Split-Path (Split-Path $PSScriptRoot))) "dup-market-radar"
  if (-not (Test-Path $RadarRoot)) {
    $RadarRoot = Join-Path $env:USERPROFILE "Desktop\dup-market-radar"
  }
}
$envPath = Join-Path $RadarRoot ".env"
if (-not (Test-Path $envPath)) {
  Write-Host "FAIL missing .env at $RadarRoot"
  exit 1
}
$map = @{}
Get-Content $envPath | ForEach-Object {
  if ($_ -match '^\s*#' -or $_ -notmatch '=') { return }
  $p = $_ -split '=', 2
  $n = $p[0].Trim()
  $v = if ($p.Count -gt 1) { $p[1].Trim().Trim('"').Trim("'") } else { "" }
  if ($n) { $map[$n] = $v }
}
$fail = @()
foreach ($k in @("KUCOIN_API_KEY","KUCOIN_API_SECRET","KUCOIN_API_PASSPHRASE","RADAR_API_KEY")) {
  if (-not $map.ContainsKey($k) -or [string]::IsNullOrWhiteSpace($map[$k])) { $fail += $k }
}
if ($fail.Count) {
  Write-Host "FAIL empty: $($fail -join ', ')"
  exit 1
}
Write-Host "PASS presence keys set (values not shown) root=$RadarRoot"
exit 0
