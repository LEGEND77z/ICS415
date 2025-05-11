# Project 4 – Bézier Curve Editor

## Overview

This project is a visual Bézier curve editor built with HTML5 Canvas and JavaScript. It allows users to interactively create and manipulate Bézier curves using draggable control points. The editor supports zooming, panning, and chaining multiple Bézier segments (poly Bézier support).

## Features

- 🖱️ **Drag-and-drop control points** to reshape curves
- ➕ **Add new Bézier segments** that continue from the previous one
- 🔍 **Zoom in/out** using the mouse wheel (centered on cursor)
- ✋ **Pan the view** by right-clicking and dragging
- 🔄 **Reset** the canvas to start over

## How to Use

1. Open `bezier-editor.html` in a browser.
2. Left-click and drag the red points to reshape a curve.
3. Click **“Add New Curve”** to continue drawing a new segment.
4. Scroll to zoom in/out.
5. Right-click + drag to pan.
6. Click **“Reset”** to clear all curves.

## Technologies

- HTML5 Canvas
- Vanilla JavaScript

## Future Enhancements (Ideas)

- Export/import curve data (JSON)
- Save as PNG image
- Curve continuity smoothing across segments

---

🎓 *Developed for ICS415 – Computer Graphics*
