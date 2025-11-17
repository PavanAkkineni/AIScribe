# Email Configuration for AIscribe
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EMAIL_CONFIG = {
    "smtp": {
        "server": os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com"),
        "port": int(os.getenv("EMAIL_SMTP_PORT", "587")),
        "username": os.getenv("EMAIL_USERNAME"),
        "password": os.getenv("EMAIL_PASSWORD")
    },
    "imap": {
        "server": os.getenv("EMAIL_IMAP_SERVER", "imap.gmail.com"),
        "port": int(os.getenv("EMAIL_IMAP_PORT", "993")),
        "username": os.getenv("EMAIL_USERNAME"),
        "password": os.getenv("EMAIL_PASSWORD")
    },
    "from_email": os.getenv("EMAIL_USERNAME"),
    "from_name": os.getenv("EMAIL_FROM_NAME", "AIscribe Medical Team")
}



