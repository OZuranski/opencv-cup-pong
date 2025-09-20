import cv2
import numpy as np

aruco = cv2.aruco
DICT = aruco.getPredefinedDictionary(aruco.DICT_4X4_50) # using 4x4 markers, 50 unique ids
PARAMS = aruco.DetectorParameters() # default parameters
PARAMS.cornerRefinementMethod = aruco.CORNER_REFINE_SUBPIX

# tweaked parameters for better detection
PARAMS.adaptiveThreshWinSizeMin = 3
PARAMS.adaptiveThreshWinSizeMax = 23
PARAMS.adaptiveThreshWinSizeStep = 10
PARAMS.minMarkerPerimeterRate = 0.02     
PARAMS.maxMarkerPerimeterRate = 4.0      

DETECTOR = aruco.ArucoDetector(DICT, PARAMS) # create detector object using set dictionary and parameters

def detect_centers_by_id(frame):
    
    centers = {} 
    
    corners, ids, _ = DETECTOR.detectMarkers(frame) # detect markers in the frame, corners is a list of corner points, ids is a list of marker ids
                                                    # _ is a rejected candidates list (not used here)
                                                    #corners is a list of 4 coordinates for the corners of each detected marker

    if ids is None:
        return centers  # empty dict if nothing found

    
    for i, c in enumerate(corners): # add index to iterate over both corners and ids
        pts = c[0] # returns just the corner points , 4x2 array of (x,y) coordinates as opposed to a list of 1x4x2 array
        cx = int(np.mean(pts[:, 0])) # center of x coords
        cy = int(np.mean(pts[:, 1])) # center of y coords
        mid = (cx, cy) # center point

        mid_id = int(ids[i])
        centers[mid_id] = mid
            
            # Draw marker & center
        
        cv2.circle(frame, mid, 5, (0, 0, 255), -1)
        cv2.putText(frame, f"id={mid_id} x={cx}",
                    (cx + 8, cy - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 255), 1, cv2.LINE_AA)
    return centers