import logging
import signal
import sys
import os

from flask import Flask
from openalpr import Alpr

LOG_FILE = '/config/oalpr/log/oalpr.log'
IMAGE_FILE = '/config/oalpr/data/plate.jpg'

logging.basicConfig(filename=LOG_FILE, filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

app = Flask(__name__)

# Читаем страну из переменной окружения, по умолчанию "us"
COUNTRY = os.getenv("COUNTRY", "ua")
lpr = Alpr(COUNTRY, "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
lpr.set_default_region(COUNTRY)  # Устанавливаем регион по умолчанию
if not lpr.is_loaded():
    logging.error(f"Error loading OpenALPR with country {COUNTRY}")
    sys.exit(1)


@app.route('/plate')
def do_it():
    logging.info("Starting recognition")

    lpr_results = lpr.recognize_file(IMAGE_FILE)
    recognized_plates = ""
    for result in lpr_results["results"]:
        recognized_plates = result["plate"]

    if recognized_plates == "":
        text = "No plates recognized"
    else:
        text = f"Recognized plates {recognized_plates}"

    logging.info(text)

    return text


def signal_handler(sig, frame):
    logging.info('Received SIGINT. Unloading ALPR')
    lpr.unload()
    sys.exit(0)


try:
    signal.signal(signal.SIGINT, signal_handler)
    logging.info(f'ALPR loaded with country {COUNTRY}. Ready to recognize')
    app.run(host='0.0.0.0')
except Exception as e:
    logging.error("Exception occurred", exc_info=True)
