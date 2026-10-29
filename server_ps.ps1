# Standalone PowerShell Web Server for ChurchView Pro
# No Python or Node.js required - runs on all Windows 10/11 PCs out of the box!
$port = 8765
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path

try {
    $listener = New-Object System.Net.HttpListener
    $listener.Prefixes.Add("http://localhost:$port/")
    $listener.Start()
} catch {
    Write-Host "Port $port is already in use or could not be bound. Opening browser..." -ForegroundColor Yellow
    Start-Process "http://localhost:$port"
    exit
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  ChurchView Pro - Church of God Alappuzha Town" -ForegroundColor Yellow
Write-Host "  Server running at: http://localhost:$port" -ForegroundColor Green
Write-Host "  Keep this window open while presenting Scripture!" -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Cyan

Start-Process "http://localhost:$port"

while ($listener.IsListening) {
    try {
        $context = $listener.GetContext()
        $req = $context.Request
        $res = $context.Response

        $localPath = $req.Url.LocalPath.TrimStart('/')
        if ([string]::IsNullOrEmpty($localPath)) { $localPath = "index.html" }
        $filePath = Join-Path $dir $localPath

        if (Test-Path $filePath -PathType Leaf) {
            $bytes = [System.IO.File]::ReadAllBytes($filePath)
            $ext = [System.IO.Path]::GetExtension($filePath).ToLower()
            switch ($ext) {
                ".html" { $res.ContentType = "text/html; charset=utf-8" }
                ".css"  { $res.ContentType = "text/css; charset=utf-8" }
                ".js"   { $res.ContentType = "application/javascript; charset=utf-8" }
                ".json" { $res.ContentType = "application/json; charset=utf-8" }
                ".png"  { $res.ContentType = "image/png" }
                default { $res.ContentType = "application/octet-stream" }
            }
            $res.Headers.Add("Cache-Control", "no-cache, no-store, must-revalidate")
            $res.Headers.Add("Pragma", "no-cache")
            $res.Headers.Add("Expires", "0")
            $res.ContentLength64 = $bytes.Length
            $res.OutputStream.Write($bytes, 0, $bytes.Length)
        } else {
            $res.StatusCode = 404
        }
        $res.OutputStream.Close()
    } catch {
        # continue loop on client abort
    }
}
