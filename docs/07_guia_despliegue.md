# Guia de Despliegue — SistemaIndicadoresKPI

## Requisitos del Sistema
| Componente | Minimo | Recomendado |
|---|---|---|
| Python | 3.10+ | 3.12+ |
| RAM | 2 GB | 4 GB |
| Disco | 500 MB libres | 2 GB libres |
| OS | Windows 10 / Ubuntu 20.04 | Windows 11 / Ubuntu 22.04 |

## Instalacion Local — Windows
```bash
git clone https://github.com/Bawuis/SistemaIndicadoresKPI.git
cd SistemaIndicadoresKPI
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py --once
```

## Instalacion Local — Linux/Mac
```bash
git clone https://github.com/Bawuis/SistemaIndicadoresKPI.git
cd SistemaIndicadoresKPI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py --once
```

## Despliegue como Servicio — Windows (Tarea Programada)
```powershell
$action  = New-ScheduledTaskAction -Execute "python" -Argument "main.py" -WorkingDirectory "C:\ETL\SistemaIndicadoresKPI"
$trigger = New-ScheduledTaskTrigger -AtStartup
Register-ScheduledTask -TaskName "ETL_SistemaIndicadoresKPI" -Action $action -Trigger $trigger -RunLevel Highest -Force

# Iniciar
Start-ScheduledTask -TaskName "ETL_SistemaIndicadoresKPI"

# Detener
Stop-ScheduledTask -TaskName "ETL_SistemaIndicadoresKPI"
```

## Despliegue como Servicio — Linux (systemd)
Crear archivo /etc/systemd/system/etl-indicadores.service:
```
[Unit]
Description=SistemaIndicadoresKPI - Pipeline ETL
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/SistemaIndicadoresKPI
ExecStart=/opt/SistemaIndicadoresKPI/venv/bin/python main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload
sudo systemctl enable etl-indicadores
sudo systemctl start etl-indicadores
sudo systemctl status etl-indicadores
```

## Despliegue con Docker
Dockerfile:
```
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p input processing output archive logs error
CMD ["python", "main.py"]
```

docker-compose.yml:
```
version: "3.9"
services:
  etl-pipeline:
    build: .
    container_name: sistema_indicadores_kpi
    restart: unless-stopped
    volumes:
      - ./input:/app/input
      - ./output:/app/output
      - ./archive:/app/archive
      - ./logs:/app/logs
      - ./error:/app/error
      - ./config.yaml:/app/config.yaml
```
```bash
docker-compose up -d
docker-compose logs -f
```

## Actualizacion del Sistema
```bash
# 1. Backup de configuracion
copy config.yaml config.yaml.bak

# 2. Detener servicio
Stop-ScheduledTask -TaskName "ETL_SistemaIndicadoresKPI"

# 3. Actualizar codigo
git pull origin main
pip install -r requirements.txt --upgrade

# 4. Reiniciar
Start-ScheduledTask -TaskName "ETL_SistemaIndicadoresKPI"
```

*Documento generado automaticamente — Pipeline ETL v1.0.0*
