"""
MODULE 1 — Computer Vision  (YOLOv8 / ultralytics)
--------------------------------------------------
Real object detection on football images. Produces the spec JSON:
    { "players": 14, "ball": true, "celebration": true, "team": "Argentina" }

Tasks covered: player detection, ball detection, crowd detection, jersey recognition.
"""
from __future__ import annotations
import numpy as np
from PIL import Image

import config
from data import nearest_team_by_color


class VisionModule:
    def __init__(self, model_name: str | None = None):
        from ultralytics import YOLO
        self.model = YOLO(model_name or config.YOLO_MODEL)
        self.device = config.DEVICE

    # ---- helpers -------------------------------------------------------
    @staticmethod
    def _dominant_color(crop: np.ndarray):
        """KMeans dominant colour of a person crop (the jersey)."""
        try:
            from sklearn.cluster import KMeans
            pixels = crop.reshape(-1, 3)
            # focus on the torso region: middle vertical band
            if pixels.shape[0] < 10:
                return tuple(int(x) for x in pixels.mean(0))
            km = KMeans(n_clusters=3, n_init=3, random_state=0).fit(pixels)
            counts = np.bincount(km.labels_)
            centre = km.cluster_centers_[counts.argmax()]
            return tuple(int(x) for x in centre)
        except Exception:
            return tuple(int(x) for x in crop.reshape(-1, 3).mean(0))

    # ---- main ----------------------------------------------------------
    def analyze(self, image_path, meta: dict | None = None) -> dict:
        meta = meta or {}
        img = Image.open(image_path).convert("RGB")
        arr = np.array(img)
        H, W = arr.shape[:2]

        res = self.model.predict(source=image_path, verbose=False, device=self.device)[0]
        names = res.names

        players, ball = 0, False
        person_boxes, jersey_colors = [], []
        for b in res.boxes:
            cls = names[int(b.cls)]
            if cls == "person":
                players += 1
                x1, y1, x2, y2 = [int(v) for v in b.xyxy[0].tolist()]
                # torso band of the person box
                ty1 = y1 + int((y2 - y1) * 0.2)
                ty2 = y1 + int((y2 - y1) * 0.55)
                crop = arr[max(0, ty1):min(H, ty2), max(0, x1):min(W, x2)]
                if crop.size:
                    person_boxes.append((x1, y1, x2, y2))
                    jersey_colors.append(self._dominant_color(crop))
            elif cls == "sports ball":
                ball = True

        # crowd: many small persons OR a large person count
        crowd = players >= 8

        # celebration heuristic: a tight cluster of upright persons + a ball or many people
        celebration = False
        if players >= 3:
            xs = [(b[0] + b[2]) / 2 for b in person_boxes]
            if xs:
                spread = (max(xs) - min(xs)) / max(W, 1)
                celebration = spread < 0.5 or players >= 10

        # jersey recognition -> nearest team (only if a colour is confidently present)
        team = meta.get("team")
        if team is None and jersey_colors:
            team = nearest_team_by_color(self._dominant_color(np.array(jersey_colors)))

        detection = {
            "players": players,
            "ball": ball,
            "crowd": crowd,
            "celebration": bool(celebration),
            "team": team,
            "jersey_colors": jersey_colors[:5],
            "image_size": [W, H],
        }
        return detection

    @staticmethod
    def to_spec_json(detection: dict) -> dict:
        """The exact compact contract from the brief."""
        return {
            "players": detection["players"],
            "ball": detection["ball"],
            "celebration": detection["celebration"],
            "team": detection["team"],
        }


if __name__ == "__main__":
    import sys, json
    vm = VisionModule()
    for p in sys.argv[1:]:
        print(p, "->", json.dumps(vm.to_spec_json(vm.analyze(p))))
