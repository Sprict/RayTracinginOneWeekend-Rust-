# Focus Guard - Distraction Blocker
# 
# 使い方:
# 1. このスクリプトを PowerShell で実行してください: .\guard.ps1
# 2. 停止するには Ctrl+C を押します
# 3. バックグラウンドで常駐させるには、タスクスケジューラ等を利用してください

$SCRIPT_DIR = $PSScriptRoot
$CONFIG_PATH = Join-Path $SCRIPT_DIR "config.json"

Write-Host "🛡️ Focus Guard Initialized..." -ForegroundColor Cyan

$lastConfigTime = $null
$cachedConfig = $null

while ($true) {
    # 1. 負荷軽減: 5秒待機 (CPU使用率ほぼ0%)
    Start-Sleep -Seconds 5

    # 2. Configファイルの更新チェック (軽量なFile System操作のみ)
    if (Test-Path $CONFIG_PATH) {
        $currentItem = Get-Item $CONFIG_PATH
        if ($currentItem.LastWriteTime -ne $lastConfigTime) {
            # ファイルが更新された時だけJSONパース（重い処理）を行う
            try {
                $cachedConfig = Get-Content $CONFIG_PATH -Raw | ConvertFrom-Json
                $lastConfigTime = $currentItem.LastWriteTime
                Write-Host "🔄 Config reloaded." -ForegroundColor Gray
            }
            catch {
                Write-Warning "Config reload failed."
            }
        }
    }

    # Configが無効または読み込めていない場合はスキップ
    if (-not $cachedConfig -or -not $cachedConfig.schedule.enabled) { continue }

    $now = Get-Date

    # 週末スキップ判定
    if ($cachedConfig.schedule.skip_weekends) {
        $day = $now.DayOfWeek
        if ($day -eq [DayOfWeek]::Saturday -or $day -eq [DayOfWeek]::Sunday) {
            # 週末なので何もしない
            continue
        }
    }

    # 3. 時間チェック (メモリ上の計算のみ、超高速)
    $startStr = $cachedConfig.schedule.start_time
    $endStr = $cachedConfig.schedule.end_time

    # 文字列パースを毎回しないように、単純な時刻比較ロジックを使う手もあるが
    # PowerShellのGet-Dateはそこまで重くない。
    # ただし厳密にはここも最適化可能だが、可読性維持のためこのままとする。
    
    $todayStart = Get-Date $startStr
    $todayEnd = Get-Date $endStr
    
    $isBlockedTime = $false
    if ($todayStart -le $todayEnd) {
        if ($now -ge $todayStart -and $now -le $todayEnd) { $isBlockedTime = $true }
    }
    else {
        if ($now -ge $todayStart -or $now -le $todayEnd) { $isBlockedTime = $true }
    }

    # 4. プロセスチェック
    # 時間外なら何もしない (Get-Processすら呼ばない)
    if (-not $isBlockedTime) { continue }

    # 時間内のみプロセスチェックを行う
    $blacklist = $cachedConfig.blacklist
    
    # 最適化: Get-Processを1回だけ呼び、ブラックリストと照合する
    # (毎回 foreach で Get-Process -Name を呼ぶより、全取得してフィルタする方が軽い場合があるが
    #  PowerShellの場合は特定名指定の方が速いことが多い。
    #  ただし、例外発生のオーバーヘッドを避けるため ErrorAction を徹底する)
    
    foreach ($procName in $blacklist) {
        # Get-Process は見つからないと例外を投げるので、それを避けるのが負荷対策の鍵
        # しかし -ErrorAction SilentlyContinue でも内部コストはある。
        # ここはシンプルさを維持しつつ、もし重いようなら改善余地あり。
        
        $procs = Get-Process -Name $procName -ErrorAction SilentlyContinue
        if ($procs) {
            foreach ($p in $procs) {
                Write-Host "🚫 Blocking: $($p.ProcessName)" -ForegroundColor Red
                Stop-Process -InputObject $p -Force -ErrorAction SilentlyContinue
            }
        }
    }
}
