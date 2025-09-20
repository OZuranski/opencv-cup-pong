import cv2, os, time
from tracker import detect_centers_by_id
from face_detection import detect_faces
from snapshot import save_snapshot
import winsound

ELBOW_ID = 0
TABLE_ID = 1
CAPTURE_DIR = os.path.join(os.path.dirname(__file__), "..", "captures")

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cap.set(cv2.CAP_PROP_FPS, 60)           # try for higher FPS
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # smaller frames = shorter exposure sometimes
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Try manual exposure (Windows often uses these magic values)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # DSHOW: 0.25=manual, 0.75=auto
    cap.set(cv2.CAP_PROP_EXPOSURE, -6)         # scale varies by camera; try -4..-8
    cap.set(cv2.CAP_PROP_GAIN, 0)              # reduce gain noise if exposure is short
    
    last_crossed = None
    last_capture_ts = 0
    COOLDOWN = 0.5

    while True:
        ret, frame = cap.read()
        if not ret: break

        centers = detect_centers_by_id(frame)
        faces = detect_faces(frame)

        if ELBOW_ID in centers and TABLE_ID in centers:
            elbow_x = centers[ELBOW_ID][0]
            table_x = centers[TABLE_ID][0]
            crossed = elbow_x <= table_x

            if crossed != last_crossed:
                print("CROSSED" if crossed else "OK")
                
                last_crossed = crossed

                if crossed and time.time() - last_capture_ts > COOLDOWN:
                    winsound.Beep(1000, 2000)
                    out_path = save_snapshot(frame, centers, faces,
                                             ELBOW_ID, TABLE_ID, CAPTURE_DIR)
                    try: os.startfile(out_path)
                    except: pass
                    last_capture_ts = time.time()

        cv2.imshow("live", frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()