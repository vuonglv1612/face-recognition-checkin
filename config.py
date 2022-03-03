from environs import Env

env = Env()
env.read_env()

CSV_LOG_FILE_PATH = env.str("CSV_LOG_FILE_PATH", "./logs/csv_logfile.csv")
LOG_IMAGES_PATH = env.str("LOG_IMAGES_PATH", "./logs/log_images")
CHECK_IN_INTERVAL = env.int("CHECK_IN_INTERVAL", 60)  # in seconds
REDIS_URI = env.str("REDIS_URI", "redis://localhost:6379")
WORKER_QUEUE = env.str("WORKER_QUEUE", "telegram")
TELEGRAM_CHAT_ID = env.str("TELEGRAM_CHAT_ID", "")
TELEGRAM_BOT_TOKEN = env.str("TELEGRAM_BOT_TOKEN", "")
