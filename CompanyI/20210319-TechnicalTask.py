#!/usr/bin/env python3
"""
This script tries to solve the problem given below:

Download TLEs of a satellite from the Internet and propagte it using 
SGP4 propagation model for n days(where n is an integer) and report the
new TLEs with the epoch.

The solution below is incomplete due to the fact that after submitting
the code to the company, my application was rejected. Due to this, I
lost motivation finalizing the code. Please feel free to build upon and
just give credit to me for being the original author.(Thanks)
"""

__author__ = 'Muhammad Ahsan'
__version__ = '0.1a'
__copyright__ = 'Copyright (C) 2021 Muhammad Ahsan'
__license__ = 'CC BY-NC-SA'

import sys, argparse
from skyfield.api import load, N, W, wgs84, EarthSatellite
from skyfield.elementslib import osculating_elements_of
from dateutil.relativedelta import relativedelta as rd
#from sgp4.api import Satrec
#from sgp4 import exporter

class SimulateX2(object):
    """A class to simulate a satellite with SGP4 propagation model"""

    def __init__(self, catnr, xdays):
        """Initialize the catalog number and number of days attributes."""

        self.catnr = catnr
        self.xdays = xdays

    def getTLEs(self):
        """Get TLEs of a given satellite from Internet and save into a file"""

        url = 'https://celestrak.com/satcat/tle.php?CATNR={}'.format(self.catnr)
        self.filename = 'tle-CATNR-{}.txt'.format(self.catnr)

        try:
            # TODO: Use logger for logging
            print("Fetching TLEs for satellite with catalog number {}.".format(self.catnr))
            tle = load.tle_file(url, filename=self.filename, reload=True)
        except OSError:
            print("An error occurred while fetching the TLEs")
            print("Are you connected to Internet?")
        else:
            print("TLEs are saved in {}".format(self.filename))

    def loadTLEs(self):
        """Load line 1 and 2 of TLEs"""

        try:
            with open(self.filename) as fobj:
                lines = fobj.readlines()
        except FileNotFoundError:
            print("Sorry, the file {} does not exist.".format(self.filename))
        else:
            length = len(lines)
            if length != 3:
                print("The file {} is not in a standard NORAD TLEs format.".format(self.filename))
                print("Cannot continue.")
                sys.exit()
            temp = []
            for line in lines:
                temp.append(line.strip())
            self.line0, self.line1, self.line2 = temp[0], temp[1], temp[2]

    def getEpoch(self):
        """Get epoch from TLEs"""

        self.ts = load.timescale()
        self.satellite = EarthSatellite(self.line1, self.line2, self.line0, self.ts)
        print("TLE epoch: {}".format(self.satellite.epoch.utc_jpl()))

    def getNewEpoch(self):
        """Calculate new epoch based on the number of days"""

        c_epoch = self.satellite.epoch.utc_datetime()
        offset = rd(days=+self.xdays)
        new_epoch = c_epoch + offset
        print("New epoch: {}".format(new_epoch))
        t1 = self.ts.utc(new_epoch)
        return t1

    def getPV(self):
        """Get satellite position(geocentric coordinates) and velocity at new epoch"""

        n_epoch = self.getNewEpoch()

        geocentric = self.satellite.at(n_epoch)
        speed = self.satellite.at(n_epoch).velocity.km_per_s
        return [geocentric, speed]

    def getLonLatAlt(self):
        """Get longitude, latitude, and altitude """

        pv_list = self.getPV()
        subpoint = wgs84.subpoint(pv_list[0])
        print("Longitude: {}".format(subpoint.longitude))
        print("Latitude: {}".format(subpoint.latitude))
        print("Altitude (in kilometers): {}".format(subpoint.elevation.km))

    def getOrbitalElements(self):
        """Get orbital and dynamic elements"""
        
        pv_list = self.getPV()
        elements = osculating_elements_of(pv_list[0])

        # line 2 of new TLEs
        self.inclination = elements.inclination.degrees
        self.raan = elements.longitude_of_ascending_node
        self.eccentricity = elements.eccentricity
        self.aop = elements.argument_of_periapsis
        self.ma = elements.mean_anomaly
        self.mm = elements.mean_motion_per_day
        return [self.inclination, self.raan, self.eccentricity, \
                self.aop, self.ma, self.mm]


    def printResults(self):
        """Print results obtained from various methods"""

        pv_list = self.getPV()
        print("Geocentric x,y,z in GCRS: {}".format(pv_list[0].position.km)) 

        print("Velocity (km/s): {}".format(pv_list[1]))
        
        orbit_elements = self.getOrbitalElements()
        print()
        print(" ========== Line 0 of New TLEs ========== ")
        print("Satellite name: {}".format(self.satellite.name))
        print()
        print(" ========== Line 1 of New TLEs ========== ")
        print("Satellite number: {}".format(self.catnr))
        print("Satellite classification: {}".format(self.satellite.model.classification))
        print("International designator: {}".format(self.satellite.model.intldesg))
        print("Epoch year: {}".format(self.satellite.model.epochyr)) # put updated epoch
        print("Epoch days: {}".format(self.satellite.model.epochdays+self.xdays))
        print("Ballistic drag coefficient: <placeholder>")
        print("2nd Derivative of the mean motion (ignored by SGP4): <placeholder>")
        print("Drag term: <placeholder>")
        print("Ephemeris Type: 0")
        print("Element number: {}".format(self.satellite.model.elnum))

        print()
        print(" ========== Line 2 of New TLEs ========== ")
        print("Satellite number: {}".format(self.catnr))
        print("Inclination (in degrees): {}".format(orbit_elements[0]))
        print("RAAN: {}".format(orbit_elements[1]))
        print("Eccentricity: {}".format(orbit_elements[2]))
        print("Argument of perigee: {}".format(orbit_elements[3]))
        print("Mean Anomaly: {}".format(orbit_elements[4]))
        print("Mean motion: {}".format(orbit_elements[5]))

    def generateTLEs(self):
        """Generate a new set of TLEs based on the new epoch"""

        # TODO: wrap the static and dynamic elements into a new TLEs
        #satrec = satrec()
        #satrec.sgp4init(
        #            WGS84,              # gravity model
        #            'i',                # 'i' = improved mode
        #            self.catnr,         # satnum: Satellite number


        #        )
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="A class to simulate a \
            satellite with SGP4 propagation model")
    parser.add_argument("catnr", help="NORAD catalog number of the satellite.", type=int)
    parser.add_argument("xdays", help="Number of days to propagate the satellite using \
            SGP4 orbit propagator.", type=int)
    args = parser.parse_args()
    new_simulation = SimulateX2(catnr=args.catnr, xdays=args.xdays)
    new_simulation.getTLEs()
    new_simulation.loadTLEs()
    new_simulation.getEpoch()
    new_simulation.getLonLatAlt()
    new_simulation.printResults()
