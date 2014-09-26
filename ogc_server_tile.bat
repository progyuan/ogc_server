@echo "-------------------------------------------"
@echo "启动瓦片服务，端口89(可在ogc-config-tile.ini中修改)"
@echo "-------------------------------------------"
@cd /d %~dp0
ogc_server.exe -c ogc-config-tile.ini

