import cv2
import numpy as np

aruco = cv2.aruco
DICT = aruco.getPredefinedDictionary(aruco.DICT_4X4_50) # using 4x4 markers, 50 unique ids
PARAMS = aruco.DetectorParameters() # default parameters
DETECTOR = aruco.ArucoDetector(DICT, PARAMS) # create detector object using set dictionary and parameters

def detect_markers(frame):
    
    corners, ids, _ = DETECTOR.detectMarkers(frame) # detect markers in the frame, corners is a list of corner points, ids is a list of marker ids
                                                    # _ is a rejected candidates list (not used here)
                                                    #corners is a list of 4 coordinates for the corners of each detected marker
    results = []

    if ids is not None: # if markers were detected
        for i, c in enumerate(corners): # add index to iterate over both corners and ids
            pts = c[0] # returns just the corner points , 4x2 array of (x,y) coordinates as opposed to a list of 1x4x2 array
            cx = int(np.mean(pts[:, 0])) # center of x coords
            cy = int(np.mean(pts[:, 1])) # center of y coords
            results.append((int(ids[i]), (cx, cy))) # results becomes a list like (id, (cx, cy))

            # Draw marker & center
            cv2.aruco.drawDetectedMarkers(frame, [c], ids[i]) # draws a box around the marker
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1) # draws a red dot at the center of the marker
            cv2.putText(frame, f"id={int(ids[i])} x={cx}", # label the marker with its id and x coordinate
                        (cx + 8, cy - 8), # position of text
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, # font, size
                        (0, 0, 255), 1, cv2.LINE_AA) # color, thickness, line type
    return results