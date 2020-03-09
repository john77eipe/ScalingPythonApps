import logging

from dotenv import load_dotenv

from modules.bannerwriter import app, celery

load_dotenv()

if __name__ == "__main__":
    app.run(debug=False)