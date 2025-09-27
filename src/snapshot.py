import os, cv2
from datetime import datetime

def save_snapshot(frame, centers, elbow_id, table_id, out_dir):
    
    os.makedirs(out_dir, exist_ok=True)
    save_frame = frame.copy()

    # draw marker lines
    ex = centers[elbow_id][0]
    tx = centers[table_id][0]
    cv2.line(save_frame, (ex,0),(ex,save_frame.shape[0]),(255,0,0),2)
    cv2.line(save_frame, (tx,0),(tx,save_frame.shape[0]),(0,255,0),2)

    # banner text
    stamp_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(save_frame, f"CROSSED! {stamp_text}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 3, cv2.LINE_AA)

    # save
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    out_path = os.path.join(out_dir, f"cross_{stamp}.jpg")
    cv2.imwrite(out_path, save_frame)
    return out_path
