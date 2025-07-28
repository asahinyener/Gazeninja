# Gaze‑OS Living Room – Quick README

A **minimal gaze‑controlled dashboard** powered by WebGazer.js.  Look at furniture items to trigger actions; stare at the lamp to switch between dark and light mode.

---

## Files
| File | Purpose |
|------|---------|
| `index.html` | Single‑page demo (HTML + CSS + JS) |
| `livingroom.png` | 1024 × 768 background image |

---

## Requirements
* Desktop Chrome or Edge with webcam permission.
* Place `livingroom.png` in the same folder as `index.html`.

---

## How to Run
1. Open **`index.html`**. The eye data recording starts automatically upon initiation.  
2. The camera video box provides the user with a green box indicating where the head should be placed.  
3. Facial landmarks will be detected and displayed on the camera when the detection is complete.  
4. Once calibration is launched, two dots are displayed: red for raw gaze data and blue for the smoothed cursor.  
5. Complete the 9‑point eye‑tracking calibration. Each point is clicked 3 times while the gaze is on the dot.  
6. Fixate on furniture (~1.2 s) until it glows—then the mapped action fires.

---

## Interaction Cheatsheet
| Look at … | Opens / Does |
|-----------|--------------|
| Lamp | Toggle room lighting |
| TV | Netflix |
| Bookshelf | Wikipedia |
| Sofa (left) | Google search |
| Sofa (right) | Steam store |
| Phone | ChatGPT |
| Files box | Google Drive |

---

## Keyboard Controls (Advanced Features)
| Key | Toggles Feature | Description |
|-----|------------------|-------------|
| `g` | `FEATURES.growingAOI` | Enables/disables growing area-of-interest for hit detection |
| `e` | `FEATURES.emaInHitTest` | Switch between raw vs. smoothed (EMA) gaze for hit-testing |
| `k` | `FEATURES.use_kalman` | Toggle Kalman filter for gaze smoothing |
| `1` | `FEATURES.use_euro` | Reserved toggle for custom "Euro" logic (user-defined) |
| `c` | `startCalibration()` | Re-start calibration and switch to dark mode |

---

## Data Logging
Click **Download CSV** (bottom‑left) to save all raw & smoothed gaze points.

---

## Customise
* **URLs:** edit the `urlMap` object.
* **Hotspots:** edit entries in `furniture[]` and update the PNG artwork.
* **Dwell time:** tweak `DWELL_THRESHOLD` (milliseconds).
* **Start in light mode:** set `darkMode = false` near the top of the script.

---

## Notes
* Desktop‑only; WebGazer has no mobile support yet.
* Accuracy depends on webcam quality and ambient lighting.

---

## License
Code: **MIT** · WebGazer.js: **Apache‑2.0**