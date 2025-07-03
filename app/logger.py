from .AppLogger import AppLogger

logger = AppLogger(
    name="ollama chat",
    log_file="app.log",
    json_format=False
)