import cv2

# Load Haar cascade once
FACE_CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)

def detect_faces(frame, scaleFactor=1.1, minNeighbors=5, minSize=(40,40)):
    """Return list of (x,y,w,h) face rects in BGR frame."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=minNeighbors, minSize=minSize)
    return faces

def draw_big_x(img, x, y, w, h, color=(0,0,255), thickness=4, pad=4):
    """Draw a big X over the rectangle (x,y,w,h)."""
    x1, y1 = x - pad, y - pad
    x2, y2 = x + w + pad, y + h + pad
    cv2.line(img, (x1, y1), (x2, y2), color, thickness)
    cv2.line(img, (x1, y2), (x2, y1), color, thickness)