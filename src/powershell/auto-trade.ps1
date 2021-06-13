cd ~\auto-trade-docker
Get-Date >> .log\windows_execution.log
# サーバーを起動し続けていると時刻がずれてAPIエラーが発生するため、実行前に時刻同期を毎回実施
docker-compose exec app ntpdate time.google.com >> .log\windows_execution.log
docker-compose exec app python src/main.py >> .log\windows_execution.log