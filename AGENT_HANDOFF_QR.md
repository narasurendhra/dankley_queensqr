# Agent Handoff: Dankley Queens Dynamic QR Codes

## Overview
This repository manages the dynamic QR codes for Dankley Queens. 
Because the physical QR codes are printed on flyers and store materials, we use a **Dynamic URL Redirection Architecture** via Vercel instead of hardcoding destination URLs into the QR images themselves.

## Architecture
1. **The QR Codes:**
   The printed QR codes route to a Vercel application (e.g., `https://dankley-queensqr.vercel.app/`).
2. **The Vercel Server:**
   The Vercel server hosts simple `index.html` pages containing `<meta http-equiv="refresh">` tags and JavaScript fallbacks.
3. **The Destination:**
   The HTML pages instantly forward the user to the live URLs (e.g., `https://dankley.com/store/` or Eventbrite).

## How to Generate QR Codes
If you need to generate new QR codes or change the color variants, run the `generate_qr.py` script located in the root of the `QR_codes` workspace.

```bash
# 1. Install dependencies
pip install qrcode pillow

# 2. Run the generator
python generate_qr.py
```

### Script Features
- Generates **Dark Green** (`#1A4331`) and **Terracotta** (`#E2725B`) variations of each URL.
- Automatically saves the outputs into the `qr assets/` directory.
- Currently configured for three endpoints:
  - `Store`: Points to the Vercel root.
  - `Events`: Points to the Vercel `/events` route.
  - `Consultation`: Points directly to `https://dankley.com`.

## To Update a Destination
Do **NOT** regenerate the QR codes if a URL changes. Instead, update the corresponding `index.html` file in the repository (either the root `index.html` or `events/index.html`) and let Vercel deploy the update. 

*Exception:* If you are adding a completely new endpoint (like `Consultation`), you must update `generate_qr.py` to add the new URL constant and run the script to output the PNGs.

### V2 Update: Premium Aesthetic & Dynamic Consultation Routing (Append-Only Ledger)
- **Aesthetic Overhaul**: Generator updated to use `StyledPilImage` with `RoundedModuleDrawer()` to yield smooth, dotted data pixels.
- **Color Inversion & Logos**: The background color is now solid Dark Green (`#2c4d43`) or Terracotta (`#cd6b48`), and the QR data pixels are Dankley Cream (`#fcf3da`). The central logo uses the inverse color 'D' sitting on a circular solid cream mask.
- **Dynamic Consultation Routing**: The `Consultation` QR code logic was updated to point to the dynamic Vercel route (`https://dankley-queensqr.vercel.app/consultation`) instead of hardcoding `dankley.com`. A new `consultation/index.html` file was created to handle the redirection.
- **Git Tracking Rules**: The Python generator scripts and original logo images are explicitly excluded from Git commits. Only the generated PNGs in qr assets/ and the routing HTML files should be staged and pushed to Vercel.

### V4 Update: Directions Endpoint Added (Append-Only Ledger)
- **Directions QR Added**: Configured `generate_qr.py` with a new `DIRECTIONS_URL` constant (`/directions`) and generated matching QR codes into `qr assets/queens_directions/`.
- **Directions Routing File**: Created a new `directions/index.html` file to handle dynamic redirection to the Google Maps destination.

### V5 Update: Fading Circle Background & Inverted D Mask (Append-Only Ledger)
- **Mask Extraction Logic**:
  - `d_mask`: Extracted by color-thresholding the Cream pixels of the logo (which represent the stylized 'D' itself).
  - `hollow_mask`: Extracted by flood-filling the inverse of the Cream pixels starting from `(0, 0)` to clear the badge background and corners, isolating the hollow region inside the D loop.
- **Radial Gradient Background**:
  - Replaced the solid Cream circle with a radial gradient mask (`gradient_mask`) that is 100% opaque Cream within `inner_r` (32% of logo size) and fades linearly to 0% opacity at `outer_r` (50% of logo size).
- **Layer Stacking**:
  - Layer 1: Paste solid Cream background using the fading `gradient_mask` to allow underlying QR pixels to show through near the edges.
  - Layer 2: Paste solid Cream using the `hollow_mask` to keep the inside loop of the D solid.
  - Layer 3: Paste the solid inverted color D (Terracotta or Green) using the `d_mask`.


### V6 Update: Expanded Faded Circle & Decoupled sizes (Append-Only Ledger)
- **Decoupled Sizes**:
  - Reconfigured `generate_qr.py` to decouple the size of the fading background circle from the size of the D logo.
  - The Cream fading circle mask is scaled to **45%** of the QR code width.
  - The stylized 'D' logo size is kept at **35%** of the QR code width, centered inside the 45% canvas (using offset calculations).
  - The solid core radius is set to **14%** of the circle canvas size, yielding a much broader and softer fading glow blending into the QR code pixels.
- **Asset Regeneration**:
  - Regenerated all 10 dynamic QR codes across the Category folders (`store`, `fidi`, `events`, `consultation`, and `directions`) using these approved proportions.


### V7 Update: Vector SVG Export Support Added (Append-Only Ledger)
- **Vector SVG Generation**:
  - Added a new `generate_qr_svg` function to `generate_qr.py` to output native vector SVG versions of each QR code alongside the raster PNGs.
- **SVG Styling Details**:
  - **Rounded Modules**: Drawn as `<rect>` tags with `rx="0.38" ry="0.38"` for a smooth, rounded module aesthetic.
  - **Embedded Vector Logo**: Uses exact path data extracted from the brand's master assets (`PATH1` and `PATH2` constants) scaled and translated to center inside the QR code.
  - **Fading Radial Gradient**: Implemented using an SVG `<radialGradient>` with stops configured to match the approved 45% circle scale and 14% solid core ratio.
  - **Inverted D Mask**: Created an SVG `<mask>` that dynamically clips a solid rectangle of the brand accent color (`d_color`) to the exact shape of the stylized 'D' lettermark.
- **Regenerated Assets**:
  - Automatically exports `.svg` versions of all 10 QR codes into the respective category folders in `qr assets/` alongside the PNGs.



