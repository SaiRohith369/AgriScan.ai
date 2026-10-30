"""Start the AgriScan.ai web app:  python run.py"""
import logging

import config
from agriscan.webapp import create_app

logging.basicConfig(level=logging.INFO)
app = create_app()

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=False)
