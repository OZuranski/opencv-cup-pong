import cv2 # pulls opencv lib

cap = cv2.VideoCapture(0) # camera object at index 0 (most likely default camera)

while True: # infinite loop
    ret, frame = cap.read() #returns a bool (ret) if frame is readable, frame is the image data
    cv2.imshow('webcam', frame) # display the frame in a window named 'webcam'

    if cv2.waitKey(1) & 0xFF == ord('q'): # wait 1ms for a keypress, if 'q' is pressed, break the loop
        break


cap.release() # release the camera
cv2.destroyAllWindows() # close all OpenCV windows
