import cv2 # pulls opencv lib
from tracker import detect_centers_by_id

ELBOW_ID = 0   
TABLE_ID = 1  

def main():

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 

    # Camera settings (needed to track properly)
    cap.set(cv2.CAP_PROP_FPS, 60)           
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  
    cap.set(cv2.CAP_PROP_EXPOSURE, -6)         
    cap.set(cv2.CAP_PROP_GAIN, 0)              

    if not cap.isOpened():
        print(" Cannot open camera at index 0 with CAP_DSHOW")
        return
    
    print("Press 'q' to quit")

    last_crossed = None

    while True: 
        ret, frame = cap.read() #returns a bool (ret) if frame is readable, frame is the image data
        if not ret or frame is None:
            print(" Failed to grab frame")
            break

        centers = detect_centers_by_id(frame)

        cv2.putText(frame, f"seen: {sorted(list(centers.keys()))}", (20, 70), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2, cv2.LINE_AA)
        
        if ELBOW_ID in centers and TABLE_ID in centers:
            elbow_x = centers[ELBOW_ID][0]
            table_x = centers[TABLE_ID][0]
            crossed = elbow_x <= table_x

            if crossed != last_crossed:
                if crossed:
                    print(" CROSSED (elbow is NOT to the right of table)")
                else:
                    print(" OK (elbow is to the right of table)")
                last_crossed = crossed

            status_text = "CROSSED" if crossed else "OK"
            color = (0, 0, 255) if crossed else (0, 255, 0)
            cv2.putText(frame, status_text, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3, cv2.LINE_AA)

        else:
            
            cv2.putText(frame, "One or more markers not detected",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
        if cv2.waitKey(1) & 0xFF == ord('q'): # wait for 'q' key to quit
            break

        cv2.imshow("ArUco Tracker", frame)
    
    cap.release() 
    cv2.destroyAllWindows() 

if __name__ == "__main__":
    main()