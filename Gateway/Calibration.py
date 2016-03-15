#!/usr/bin/env python
from utils.Observer import Observer
from Camera import Camera
import numpy as np
from parse import *

class Calibration:
    """
    This calibration is aimed at receiving calibration datas from
    the websocket server, and control the calibration sequence.
    It holds the 3D World Coordinates sent over websocket.
    Calls cameras calibration function to save 2D calibration points
    and calculate a new projection matrix on calibration exit
    """

    points2D = []
    world3DPoints = np.array([], dtype=np.float32).reshape(0,3)
    cameras = {}

    def __init__(self, cameras):
        print "Init Calibration"
        self.cameras = cameras
        self.world3DPoints = np.array([], dtype=np.float32).reshape(0,3)

    def push(self, message):
        if message == "enter":
            print "Start calibration"
            self.world3DPoints = np.array([], dtype=np.float32).reshape(0,3)
            for key in self.cameras:
                    if isinstance(self.cameras[key], Camera):
                        self.cameras[key].enterCalibrationMode()

        elif message == "exit":
            print "End calibration, calculates..."
            for key in self.cameras:
                    if isinstance(self.cameras[key], Camera):
                        self.cameras[key].exitCalibrationMode(self.world3DPoints)
        else:
            extracted_data = parse("calib:{}-{}-{}", message)
            if len(extracted_data.fixed) == 3:
                xyz = [int(extracted_data.fixed[0]), int(extracted_data.fixed[1]), int(extracted_data.fixed[2])]
                self.world3DPoints = np.append(self.world3DPoints, [xyz], axis=0)
                for key in self.cameras:
                    if isinstance(self.cameras[key], Camera):
                        self.cameras[key].saveCalibrationPoint2D()
