"""Run the open YOLOv8n COCO model (ONNX) on a frame from the CV Test Bench sample clips.

Sample clips: Intel IoT DevKit sample videos, CC BY 4.0
(https://github.com/intel-iot-devkit/sample-videos). Credit them in the figure caption.
Model: Ultralytics YOLOv8n, AGPL-3.0.
"""
import json
import cv2
import numpy as np
import onnxruntime as ort

BENCH = "/home/user/cv-test-dashboard/docs"
SAMPLES = ["safety", "traffic", "retail", "bottles", "people", "demo"]
_sess = None
NAMES = json.load(open(f"{BENCH}/models/yolo/coco-names.json"))


def frame(sample, t=0.5):
    """Return one BGR frame at fraction t (0..1) of samples/<sample>.mp4."""
    cap = cv2.VideoCapture(f"{BENCH}/samples/{sample}.mp4")
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, min(n - 1, int(n * t))))
    ok, img = cap.read()
    cap.release()
    if not ok:
        raise RuntimeError("could not read frame")
    return img


def detect(img, conf=0.25, iou=0.45, nms=True, size=416):
    """Return list of (x1, y1, x2, y2, score, class_name) in image pixels."""
    global _sess
    if _sess is None:
        _sess = ort.InferenceSession(f"{BENCH}/models/yolo/yolov8n-416.onnx", providers=["CPUExecutionProvider"])
    h, w = img.shape[:2]
    r = size / max(h, w)
    nh, nw = int(round(h * r)), int(round(w * r))
    canvas = np.full((size, size, 3), 114, np.uint8)
    canvas[:nh, :nw] = cv2.resize(img, (nw, nh))
    x = canvas[:, :, ::-1].transpose(2, 0, 1)[None].astype(np.float32) / 255
    out = _sess.run(None, {_sess.get_inputs()[0].name: x})[0][0].T  # (N, 4+80)
    scores = out[:, 4:].max(1)
    cls = out[:, 4:].argmax(1)
    keep = scores >= conf
    out, scores, cls = out[keep], scores[keep], cls[keep]
    boxes = np.stack([out[:, 0] - out[:, 2] / 2, out[:, 1] - out[:, 3] / 2,
                      out[:, 0] + out[:, 2] / 2, out[:, 1] + out[:, 3] / 2], 1) / r
    idx = range(len(boxes))
    if nms and len(boxes):
        idx = cv2.dnn.NMSBoxes([[float(a), float(b), float(c - a), float(d - b)] for a, b, c, d in boxes],
                               scores.tolist(), conf, iou)
        idx = np.array(idx).reshape(-1)
    return [(*boxes[i].tolist(), float(scores[i]), NAMES[int(cls[i])]) for i in idx]


def draw(img, dets, color=(92, 107, 11), thick=2, label=True):
    """Draw boxes (BGR color, default site accent) and return a copy."""
    im = img.copy()
    for x1, y1, x2, y2, s, n in dets:
        p1, p2 = (int(x1), int(y1)), (int(x2), int(y2))
        cv2.rectangle(im, p1, p2, color, thick)
        if label:
            t = f"{n} {s:.2f}"
            (tw, th), _ = cv2.getTextSize(t, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(im, (p1[0], p1[1] - th - 8), (p1[0] + tw + 6, p1[1]), color, -1)
            cv2.putText(im, t, (p1[0] + 3, p1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    return im


def save_jpg(img, name, width=1100):
    """Save a BGR image to content/images/<name>.jpg, resized to width."""
    from style import OUT
    h, w = img.shape[:2]
    if w > width:
        img = cv2.resize(img, (width, int(h * width / w)), interpolation=cv2.INTER_AREA)
    OUT.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(OUT / name), img, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return OUT / name
