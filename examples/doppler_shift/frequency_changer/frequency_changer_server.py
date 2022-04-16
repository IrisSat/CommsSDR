"""
Webserver utilities for http communication with python logic
"""
import json
import logging
import os
import threading
import time
import xmlrpc.client

from bottle import Bottle, request

from doppler_shifter import DopplerShifter
from satellite_tle import SatelliteTLE


class FrequencyChangerServer:
    """
    Webserver class that contains the bottle.py logic and implementation
    """

    FREQUENCY_CHANGER_XMLRPC_SERVER = f"http://{os.getenv('FREQUENCY_CHANGER_SERVER')}"

    def __init__(self, host: str = "0.0.0.0", port: str = "8051"):
        super().__init__()

        self.host = host
        self.port = port
        self._app = Bottle()
        self._routes()

        self._doppler_shift_thread = None

        self._start_webserver()

    def _start_webserver(self):
        self._app.run(host=self.host, port=self.port)

    def _routes(self):
        self._app.route('/frequency', method="PUT", callback=self._set_frequency)
        self._app.route('/start_doppler', method="PUT", callback=self._set_doppler)
        self._app.route('/stop_doppler', method="PUT", callback=self._stop_doppler)

    def _set_frequency(self):
        data = json.load(request.body)
        logging.info("Setting the frequency to: %s", data['frequency'])

        success = False
        while not success:
            try:
                with xmlrpc.client.ServerProxy(self.FREQUENCY_CHANGER_XMLRPC_SERVER) as proxy:
                    proxy.set_frequency_slider(data["frequency"])
                success = True
            except ConnectionRefusedError as error:
                logging.error("Unable to reach the SDR Reader/Writer #1 for frequency change; %s", error.strerror)
            except xmlrpc.client.Fault as error:
                logging.error("Unable to reach the SDR Reader/Writer #1 for frequency change; %s", error.__str__())
        return 0

    def _set_doppler(self):
        sat_tle: SatelliteTLE = json.load(request.body, object_hook=lambda d: SatelliteTLE(**d))

        if self._doppler_shift_thread is not None:
            self._doppler_shift_thread.do_run = False
            self._doppler_shift_thread.join()

        self._doppler_shift_thread = threading.Thread(target=self._doppler_shift, args=(sat_tle,))
        self._doppler_shift_thread.start()

        return 0

    def _stop_doppler(self):
        if self._doppler_shift_thread is not None:
            self._doppler_shift_thread.do_run = False
            self._doppler_shift_thread.join()

        return 0

    def _doppler_shift(self, sat_tle: SatelliteTLE):

        doppler_shifter = DopplerShifter(sat_tle)

        thread = threading.current_thread()
        with xmlrpc.client.ServerProxy(self.FREQUENCY_CHANGER_XMLRPC_SERVER) as proxy:
            while getattr(thread, "do_run", True):
                doppler_shift = doppler_shifter.get_doppler_shift()
                try:
                    proxy.set_doppler(doppler_shift)
                except ConnectionRefusedError as error:
                    logging.error("Unable to reach the SDR Reader/Writer #1 for doppler correction; %s", error.strerror)
                    proxy = xmlrpc.client.ServerProxy(self.FREQUENCY_CHANGER_XMLRPC_SERVER)
                except xmlrpc.client.Fault as error:
                    logging.error("Unable to reach the SDR Reader/Writer #1 for doppler correction. Something bad "
                                  "happened in the proxy client; %s", error.__str__())
                    proxy = xmlrpc.client.ServerProxy(self.FREQUENCY_CHANGER_XMLRPC_SERVER)
                time.sleep(0.1)
