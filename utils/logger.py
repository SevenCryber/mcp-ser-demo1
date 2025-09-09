import os, sys, logging
from logging.handlers import RotatingFileHandler
from colorama import Fore, Style       # pip install colorama
from pathlib import Path

LOG_DIR   = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE  = LOG_DIR / "app.log"
MAX_BYTES = 10 * 1024 * 1024          # 10 MB
BACKUP_COUNT = 5                      # 保留 5 个滚动文件

class ColorFormatter(logging.Formatter):
    """开发环境彩色日志"""
    LEVEL_COLOR = {
        "DEBUG": Fore.CYAN,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.MAGENTA,
    }
    def format(self, record):
        color = self.LEVEL_COLOR.get(record.levelname, "")
        reset = Style.RESET_ALL
        record.levelname = f"{color}{record.levelname}{reset}"
        return super().format(record)

def get_logger(name: str = None) -> logging.Logger:
    """单例 logger，保证全局只配置一次"""
    name = name or "app"
    logger = logging.getLogger(name)
    if logger.handlers:                 # 已配置过直接返回
        return logger

    logger.setLevel("INFO")

    # 统一格式
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s"
    )

    # 1. 控制台（带颜色）
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(ColorFormatter() if sys.stdout.isatty() else fmt)
    logger.addHandler(console)

    # 2. 文件（自动分割 + 归档）
    file = RotatingFileHandler(
        LOG_FILE, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, encoding="utf-8"
    )
    file.setFormatter(fmt)
    logger.addHandler(file)
    return logger