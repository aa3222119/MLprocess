param(
    [string]$command,
    [int]$count,
    [int]$maxThreads = 6
)

# $command = "D:\Programs\Python\Python39\python.exe E:/simulate_area/MLprocess/console_inner_sc.py"

# 定义线程池
$pool = [System.Collections.ArrayList]@()

# 循环执行命令
for ($i = 1; $i -le $count; $i++) {
    # 等待空闲线程
    while ($pool.Count -ge $maxThreads) {
        Start-Sleep -Milliseconds 100
        $completed = $pool | Where-Object { $_.IsCompleted }
        foreach ($item in $completed) {
            $pool.Remove($item)
        }
    }

    # 创建新线程
    $powerShell = [PowerShell]::Create()
    $powerShell.AddScript($command)
    $pool.Add($powerShell.BeginInvoke())
}

# 等待所有线程执行完毕
$pool | ForEach-Object { $_.EndInvoke() }