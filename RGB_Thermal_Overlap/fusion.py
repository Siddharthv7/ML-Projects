import cv2
import numpy as np
import os

RGB_IMAGE_PATH = "D:/my program/New Projects/py/RGB_Thermal_Overlap/DJI_20250530123003_0002_Z.JPG"
THERMAL_IMAGE_PATH = "D:/my program/New Projects/py/RGB_Thermal_Overlap/DJI_20250530123002_0002_T.JPG"
OUTPUT_DIR = "fusion_output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

rgb = cv2.imread(RGB_IMAGE_PATH)
thermal = cv2.imread(THERMAL_IMAGE_PATH)

if rgb is None or thermal is None:
    raise ValueError("Could not load input images.")

if len(thermal.shape) == 3:
    thermal_gray = cv2.cvtColor(thermal, cv2.COLOR_BGR2GRAY)
else:
    thermal_gray = thermal.copy()

thermal_gray = cv2.resize(thermal_gray, (rgb.shape[1], rgb.shape[0]))
rgb_gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)

orb = cv2.ORB_create(3000)
kp1, des1 = orb.detectAndCompute(rgb_gray, None)
kp2, des2 = orb.detectAndCompute(thermal_gray, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)
matches = sorted(matches, key=lambda x: x.distance)
good = matches[:200]

if len(good) >= 8:
    src = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    dst = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    H, _ = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
    if H is not None:
        aligned = cv2.warpPerspective(thermal_gray, H, (rgb.shape[1], rgb.shape[0]))
    else:
        aligned = thermal_gray.copy()
else:
    aligned = thermal_gray.copy()

norm = cv2.normalize(aligned, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
thermal_color = cv2.applyColorMap(norm, cv2.COLORMAP_JET)
overlay = cv2.addWeighted(rgb, 0.5, thermal_color, 0.5, 0)

cv2.imwrite(os.path.join(OUTPUT_DIR, "thermal_gray.png"), thermal_gray)
cv2.imwrite(os.path.join(OUTPUT_DIR, "aligned.png"), aligned)
cv2.imwrite(os.path.join(OUTPUT_DIR, "thermal_color.png"), thermal_color)
cv2.imwrite(os.path.join(OUTPUT_DIR, "overlay.png"), overlay)

print("Fusion complete. Files saved in:", OUTPUT_DIR)
