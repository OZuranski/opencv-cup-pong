import cv2
aruco = cv2.aruco
dict_ = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

for id in [0, 1]:  
    img = aruco.generateImageMarker(dict_, id, 200)  # 200px
    cv2.imwrite(f"marker_{id}.png", img)