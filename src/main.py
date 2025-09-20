import cv2 # pulls opencv lib
from tracker import detect_centers_by_id
import os, time
from datetime import datetime

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

    CAPTURE_DIR = os.path.join(os.path.dirname(__file__), "..", "captures")
    os.makedirs(CAPTURE_DIR, exist_ok=True)

    last_crossed = None
    last_capture_ts = 0.0           # for cooldown
    CAPTURE_COOLDOWN_S = 0.5        # adjust if needed

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

                if crossed:
                    now = time.time()
                    if now - last_capture_ts >= CAPTURE_COOLDOWN_S: # cooldown check so we don't spam captures when sitting still on the 'line'
                        # timestamped filename
                        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # ms precision
                        out_path = os.path.join(CAPTURE_DIR, f"cross_{stamp}.jpg")
                        
                        stamp_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        cv2.putText(frame, f"CROSSED! {stamp_text}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3, cv2.LINE_AA)
                        # write the current frame
                        cv2.imwrite(out_path, frame)

                        # open it (Windows: default app). On mac use 'open', on linux 'xdg-open'
                        try:
                            os.startfile(out_path)  # Windows
                        except Exception:
                            pass  # ignore if not on Windows

                        last_capture_ts = now

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