import json
import cv2
import numpy as np

PARAM_BAWAAN = {
    "lebar": 640,
    "gamma": 1.0,
    "clahe_clip": 2.0,
    "clahe_tile": 8,
    "penapis": "median",
    "kernel": 3,
    "sigma": 1.0,
    "tajam_k": 0.0
}

def praproses(img_bgr, p=None):
    p = {**PARAM_BAWAAN, **(p or {})}
    h, w = img_bgr.shape[:2]
    lebar_baru = p["lebar"]
    tinggi_baru = int(h * lebar_baru / w)
    img = cv2.resize(img_bgr, (lebar_baru, tinggi_baru), interpolation=cv2.INTER_AREA)
    
    if p["gamma"] != 1.0:
        inv_gamma = 1.0 / p["gamma"]
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in range(256)]).astype("uint8")
        img = cv2.LUT(img, table)
        
    if p["clahe_clip"] > 0:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        clahe = cv2.createCLAHE(clipLimit=p["clahe_clip"], tileGridSize=(p["clahe_tile"], p["clahe_tile"]))
        hsv[:, :, 2] = clahe.apply(hsv[:, :, 2])
        img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
    penapis = p["penapis"]
    k = p["kernel"]
    if penapis == "rerata":
        img = cv2.blur(img, (k, k))
    elif penapis == "gaussian":
        img = cv2.GaussianBlur(img, (k, k), p["sigma"])
    elif penapis == "median":
        img = cv2.medianBlur(img, k)
        
    if p["tajam_k"] > 0:
        blur = cv2.GaussianBlur(img, (5, 5), 1.0)
        img = cv2.addWeighted(img, 1.0 + p["tajam_k"], blur, -p["tajam_k"], 0)
        
    return img

def simpan_param(p, path="hasil/param_praproses.json"):
    with open(path, "w") as f:
        json.dump({**PARAM_BAWAAN, **p}, f, indent=2)
