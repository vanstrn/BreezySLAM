#!/usr/bin/env python3

'''
rpslam.py : BreezySLAM Python with SLAMTECH RP A1 Lidar

Copyright (C) 2018 Simon D. Levy

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This code is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this code.  If not, see <http://www.gnu.org/licenses/>.
'''

MAP_SIZE_PIXELS         = 500
MAP_SIZE_METERS         = 10
LIDAR_DEVICE            = '/dev/ttyUSB0'


# Ideally we could use all 250 or so samples that the RPLidar delivers in one
# scan, but on slower computers you'll get an empty map and unchanging position
# at that rate.
MIN_SAMPLES   = 200

from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA1 as LaserModel
from rplidar import RPLidar as Lidar
from roboviz import MapVisualizer

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class DriveCommandNode(Node):

    def __init__(self):
        super().__init__('cont')

        self.subscriber = self.create_subscription(LaserScan, '/scan', self.slamCallback,10)
        # self.publisher = self.create_publisher(Twist, '/cmd_vel', 1)
        print("Setup Finished")

        self.slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)

        self.viz = MapVisualizer(MAP_SIZE_PIXELS, MAP_SIZE_METERS, 'SLAM')

        self.mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)

        self.previous_distances = None
        self.previous_angles    = None


    def motionCallback(self,data):


        distances = data.ranges
        angles  = [i for i in range(int(self.angle_min),int(self.angle_max))]
        if len(self.angles) != len(self.distances):
            self.angles = self.angles[:len(self.distances)]

        # Update SLAM with current Lidar scan and scan angles if adequate
        if len(distances) > MIN_SAMPLES:
            slam.update(distances, scan_angles_degrees=angles)
            previous_distances = distances.copy()
            previous_angles    = angles.copy()

        # If not adequate, use previous
        elif previous_distances is not None:
            slam.update(previous_distances, scan_angles_degrees=previous_angles)

        # Get current robot position
        x, y, theta = slam.getpos()

        # Get current map bytes as grayscale
        slam.getmap(mapbytes)

        # Display map and robot pose, exiting gracefully if user closes it
        if not viz.display(x/1000., y/1000., theta, mapbytes):
            exit(0)


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = DriveCommandNode()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


def main():
    # Connect to Lidar unit
    lidar = Lidar(LIDAR_DEVICE)

    # Create an RMHC SLAM object with a laser model and optional robot model


    # Set up a SLAM display


    # Initialize empty map



    # We will use these to store previous scan in case current scan is inadequate


    # First scan is crap, so ignore it
    next(iterator)

    while True:

        # Extract (quality, angle, distance) triples from current scan
        items = [item for item in next(iterator)]

        # Extract distances and angles from triples


    # Shut down the lidar connection
    lidar.stop()
    lidar.disconnect()



if __name__ == '__main__':
    main()
