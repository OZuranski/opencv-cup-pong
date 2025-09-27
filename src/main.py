# src/main.py
import os
import time
import winsound
from datetime import datetime
import numpy as np
import cv2
from tracker import detect_centers_by_id

# EDIT THESE PER YOUR SETUP ================== # THE LOWER EXPOSURE THE BETTER
CAM_INDEXES = [0,2]   # example: 0 = outside laptop cam, 2 = USB webcam for me
CAM_BACKEND_PREFS = {
    0: ["DSHOW", "MSMF", "ANY"],
    2: ["DSHOW", "MSMF", "ANY"],
}
DEFAULT_BACKEND_ORDER = ["DSHOW", "MSMF", "ANY"]  # diff cameras work better with different backends
CAM_SETTINGS = {
    0: {"fps": 60, "width": 640, "height": 480, "exposure": -4},
    1: {"fps": 60, "width": 640, "height": 480, "exposure": -4},
    2: {"fps": 60, "width": 640, "height": 480, "exposure": -7},
}
# ============================================================

ELBOW_ID = 0
TABLE_ID = 1

# per-camera options ------------------------------------
MIRROR = [False, False] # flip frames horizontally for these cams if wanted
EXPECT_ELBOW_RIGHT = [False, True] # True if elbow should be right of table at start

CAPTURE_DIR = os.path.join(os.path.dirname(__file__), "..", "captures")
os.makedirs(CAPTURE_DIR, exist_ok=True)
COOLDOWN = 0.5 # seconds between captures per cam, to avoid multiple shots when crossing
# -------------------------------------------------------

def crossed_state(centers, expect_elbow_right: bool):
    if ELBOW_ID not in centers or TABLE_ID not in centers:
        return None
    ex, tx = centers[ELBOW_ID][0], centers[TABLE_ID][0]
    return (ex <= tx) if expect_elbow_right else (ex >= tx)

def save_cross_snapshot(frame, centers, cam_os_index):
    save_frame = frame.copy()
    ex, tx = centers[ELBOW_ID][0], centers[TABLE_ID][0]
    cv2.line(save_frame, (ex, 0), (ex, save_frame.shape[0]), (255, 0, 0), 2)
    cv2.line(save_frame, (tx, 0), (tx, save_frame.shape[0]), (0, 255, 0), 2)
    cv2.putText(save_frame, f"CROSSED! {datetime.now():%Y-%m-%d %H:%M:%S}",
                (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    out_path = os.path.join(CAPTURE_DIR, f"cross_cam{cam_os_index}_{stamp}.jpg")
    cv2.imwrite(out_path, save_frame)
    try: os.startfile(out_path)
    except: pass
    return out_path

def _backend_const(name: str): 
    return {"MSMF": cv2.CAP_MSMF, "DSHOW": cv2.CAP_DSHOW}.get(name, cv2.CAP_ANY)

def try_open(idx, backend_name):
    cap = cv2.VideoCapture(idx, _backend_const(backend_name))
    return cap if cap.isOpened() else None

def apply_camera_settings(cap, os_idx):
    cfg = CAM_SETTINGS.get(os_idx, {})
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    if "width"  in cfg: cap.set(cv2.CAP_PROP_FRAME_WIDTH,  cfg["width"])
    if "height" in cfg: cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cfg["height"])
    if "fps"    in cfg: cap.set(cv2.CAP_PROP_FPS,          cfg["fps"])
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # DSHOW manual
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.00)  # MSMF manual
    if "exposure" in cfg: cap.set(cv2.CAP_PROP_EXPOSURE,   cfg["exposure"])

def open_capture(idx): 
    for name in CAM_BACKEND_PREFS.get(idx, DEFAULT_BACKEND_ORDER):
        cap = try_open(idx, name)
        if cap:
            apply_camera_settings(cap, idx)
            return (idx, cap, name)
    return None

def main():
    caps = []
    for idx in CAM_INDEXES:
        opened = open_capture(idx)
        if opened:
            caps.append(opened)
        if len(caps) == 2:
            break
    if not caps: return

    print("Keys: t=toggle active, z/x=exposure -/+, q=quit")
    active, last_crossed, last_capture_ts = 0, [None]*len(caps), [0.0]*len(caps)

    while True:
        frames, centers_list = [], []
        for i, (os_idx, cap, _) in enumerate(caps):
            ret, frame = cap.read()
            if not ret:
                frames.append(None); centers_list.append({}); continue
            if i < len(MIRROR) and MIRROR[i]:
                frame = cv2.flip(frame, 1)

            centers = detect_centers_by_id(frame)

            frames.append(frame); centers_list.append(centers)

        for i, frame in enumerate(frames):
            if frame is None: continue
            state = crossed_state(centers_list[i], EXPECT_ELBOW_RIGHT[i])
            txt, color = ("Need IDs", (0,255,255)) if state is None else \
                         ("CROSSED", (0,0,255)) if state else ("OK", (0,255,0))
            cv2.putText(frame, txt, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)
            if i == active and state is not None and state != last_crossed[i]:
                if state:
                    winsound.Beep(1000,200)
                    now = time.time()
                    if now-last_capture_ts[i] > COOLDOWN:
                        save_cross_snapshot(frame, centers_list[i], caps[i][0])
                        last_capture_ts[i] = now
                last_crossed[i] = state

        if frames[active] is not None:
            cv2.putText(frames[active], f"Active: {active}", (20,130),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200,200,200), 1)
            cv2.putText(frames[active], "t=toggle  z/x=exposure  q=quit", (20,160),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (220,220,220), 1)
            cv2.imshow("Active Camera", frames[active])

        key = cv2.waitKey(1) & 0xFF

        # handle keys
        if key == ord('q'): #quit
            break
        elif key == ord('t') and len(caps) >= 2: # toggle active
            active = 1 - active
            print(f"Toggled to {active}")
        elif key == ord('z'):  # exposure down
            os_idx, cap, _ = caps[active]
            cur = cap.get(cv2.CAP_PROP_EXPOSURE)
            cap.set(cv2.CAP_PROP_EXPOSURE, cur - 1)
            print(f"[Cam {os_idx}] Exp {cur:.0f} -> {cap.get(cv2.CAP_PROP_EXPOSURE):.0f}")
        elif key == ord('x'):  # exposure up
            os_idx, cap, _ = caps[active]
            cur = cap.get(cv2.CAP_PROP_EXPOSURE)
            cap.set(cv2.CAP_PROP_EXPOSURE, cur + 1)
            print(f"[Cam {os_idx}] Exp {cur:.0f} -> {cap.get(cv2.CAP_PROP_EXPOSURE):.0f}")

    for _, cap, _ in caps: cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()