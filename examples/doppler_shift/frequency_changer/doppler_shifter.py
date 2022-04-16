"""
This file is the utilities related to the doppler shift logic applied to correct signals
"""
import numpy as np
import skyfield
from skyfield.api import load
from skyfield.functions import length_of
from skyfield.sgp4lib import EarthSatellite

from satellite_tle import SatelliteTLE


class DopplerShifter:
    """
    The class that produces the calculation for doppler shift. Done with numpy
    """
    OBSERVER = skyfield.api.Topos(latitude=45.520403, longitude=-73.393918, elevation_m=10)

    def __init__(self, sat_tle: SatelliteTLE):
        self.satellite = EarthSatellite(sat_tle.tle1, sat_tle.tle2)
        self.frequency = sat_tle.frequency

    def get_doppler_shift(self):
        """
        Calculates the doppler shift with the given parameters of TLE data upon creation of the class
        :return: doppler_shift in hz
        """
        self.satellite.ts = load.timescale()
        los1 = (self.satellite - self.OBSERVER).at(self.satellite.ts.now())
        rate = np.sum(los1.velocity.km_per_s * los1.position.km) / length_of(los1.position.km)

        return (rate * 1000 / 299792458. * self.frequency).item()
