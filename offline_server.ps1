param([switch]$NoBrowser)
$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath($PSScriptRoot) + [IO.Path]::DirectorySeparatorChar
$snapshot = '{"live":null,"holding":null}'
$listener = [Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback,8765)
try { $listener.Start() } catch { Write-Host "Cannot start ChurchView on port 8765: $_"; exit 1 }
Write-Host 'ChurchView: http://localhost:8765 - Keep this window open. Close it to stop.'
if (-not $NoBrowser) { Start-Process 'http://localhost:8765' }
try {
    while ($true) {
        $client = $listener.AcceptTcpClient()
        try {
            $client.ReceiveTimeout = 3000
            $stream = $client.GetStream()
            $headerBuffer = [Collections.Generic.List[byte]]::new()
            while ($headerBuffer.Count -lt 16384) {
                $nextByte = $stream.ReadByte()
                if ($nextByte -lt 0) { throw 'Incomplete request' }
                $headerBuffer.Add([byte]$nextByte)
                $n = $headerBuffer.Count
                if ($n -ge 4 -and $headerBuffer[$n-4] -eq 13 -and $headerBuffer[$n-3] -eq 10 -and $headerBuffer[$n-2] -eq 13 -and $headerBuffer[$n-1] -eq 10) { break }
            }
            $lines = [Text.Encoding]::ASCII.GetString($headerBuffer.ToArray()).Split(@("`r`n"),[StringSplitOptions]::None)
            $request = $lines[0]
            $requestHeaders = @{}
            foreach ($line in $lines | Select-Object -Skip 1) {
                $colon = $line.IndexOf(':')
                if ($colon -gt 0) { $requestHeaders[$line.Substring(0,$colon).ToLowerInvariant()] = $line.Substring($colon+1).Trim() }
            }
            $parts = $request.Split(' ')
            $method = $parts[0]
            $relative = [Uri]::UnescapeDataString(($parts[1].Split('?')[0])).TrimStart('/')
            if (-not $relative) { $relative = 'index.html' }
            $path = [IO.Path]::GetFullPath((Join-Path $root $relative))
            $status = '200 OK'
            $type = 'application/octet-stream'
            $isControl = $relative -in @('__snapshot','__projector')
            if ($isControl) {
                $type = 'application/json; charset=utf-8'
                if ($method -eq 'POST') {
                    if ($requestHeaders['origin'] -notin @('http://localhost:8765','http://127.0.0.1:8765') -or $requestHeaders['x-churchview'] -ne 'local') {
                        $status = '403 Forbidden'; $bytes = [byte[]]@()
                    } else {
                        $length = [int]$requestHeaders['content-length']
                        if ($length -lt 0 -or $length -gt 10000000) { throw 'Invalid request size' }
                        $bodyBytes = New-Object byte[] $length
                        $offset = 0
                        while ($offset -lt $length) {
                            $read = $stream.Read($bodyBytes,$offset,$length-$offset)
                            if ($read -le 0) { throw 'Incomplete request body' }
                            $offset += $read
                        }
                        $bodyText = [Text.Encoding]::UTF8.GetString($bodyBytes)
                        if ($relative -eq '__snapshot') {
                            $null = $bodyText | ConvertFrom-Json
                            $snapshot = $bodyText
                        } else {
                            $position = $bodyText | ConvertFrom-Json
                            & (Join-Path $PSScriptRoot 'launch_projector.ps1') -Left ([int]$position.left) -Top ([int]$position.top)
                        }
                        $bytes = [Text.Encoding]::UTF8.GetBytes('{"ok":true}')
                    }
                } elseif ($method -eq 'GET' -and $relative -eq '__snapshot') {
                    $bytes = [Text.Encoding]::UTF8.GetBytes($snapshot)
                } else { $status = '405 Method Not Allowed'; $bytes = [byte[]]@() }
            } elseif ($method -notin @('GET','HEAD')) {
                $status = '405 Method Not Allowed'; $bytes = [byte[]]@()
            } elseif (-not $path.StartsWith($root,[StringComparison]::OrdinalIgnoreCase) -or -not [IO.File]::Exists($path)) {
                $status = '404 Not Found'; $bytes = [byte[]]@()
            } else {
                $bytes = [IO.File]::ReadAllBytes($path)
                switch ([IO.Path]::GetExtension($path).ToLowerInvariant()) {
                    '.html' { $type = 'text/html; charset=utf-8' }
                    '.css' { $type = 'text/css; charset=utf-8' }
                    '.js' { $type = 'application/javascript; charset=utf-8' }
                    '.json' { $type = 'application/json; charset=utf-8' }
                    '.png' { $type = 'image/png' }
                    '.ttf' { $type = 'font/ttf' }
                }
            }
            $headers = "HTTP/1.1 $status`r`nContent-Type: $type`r`nContent-Length: $($bytes.Length)`r`nConnection: close`r`nCache-Control: no-cache`r`n`r`n"
            $headerBytes = [Text.Encoding]::ASCII.GetBytes($headers)
            $stream.Write($headerBytes,0,$headerBytes.Length)
            if ($method -ne 'HEAD' -and $bytes.Length) { $stream.Write($bytes,0,$bytes.Length) }
            $stream.Flush()
        } catch { Write-Verbose $_ } finally { $client.Close() }
    }
} finally { $listener.Stop() }
