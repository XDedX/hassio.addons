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

COUNTRY = os.getenv("COUNTRY", "us")
lpr = Alpr(COUNTRY, "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
lpr.set_default_region(COUNTRY)
if not lpr.is_loaded():
    logging.error(f"Error loading OpenALPR with country {COUNTRY}")
    sys.exit(1)  # Завершаем процесс при ошибке


@app.route('/plate')
def do_it():
    logging.info("Starting recognition")
    try:
        lpr_results = lpr.recognize_file(IMAGE_FILE)
        recognized_plates = ""
        for result in lpr_results["results"]:
            recognized_plates = result["plate"]

        if recognized_plates == "":
            text = "No plates recognized"
        else:
            text = f"Recognized plates {recognized_plates}"
    except Exception as e:
        text = f"Error recognizing plate: {str(e)}"
        logging.error(text)
    logging.info(text)
    return text


def signal_handler(sig, frame):
    logging.info('Received SIGINT. Unloading ALPR')
    lpr.unload()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)
logging.info(f'ALPR loaded with country {COUNTRY}. Ready to recognize')
app.run(host='0.0.0.0')
