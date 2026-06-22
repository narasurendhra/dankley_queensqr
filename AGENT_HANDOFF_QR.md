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


### V8 Update: Events Redirection Target URL Updated (Append-Only Ledger)
- **Events Redirection Destination Update**: Changed the redirect destination in `events/index.html` from the Jadakiss event page to the new Eventbrite tickets page for the "Dankleys 710 on 711" event: `https://www.eventbrite.com/e/dankleys-710-on-711-tickets-1992293029081?aff=oddtdtcreator`.


### V9 Update: Vector SVG Module Merging & Sharp Eyes (Append-Only Ledger)
- **Module Merging Logic**: Refactored `generate_qr_svg` to dynamically check the four neighbors (North, South, East, West) of each active data module and draw custom merging SVG paths with a corner radius of `r = 0.5`. This causes adjacent modules to merge seamlessly into continuous rounded shapes, matching Pillow's `RoundedModuleDrawer` behavior.
- **Finder Patterns (Eyes)**: Configured the finder patterns to remain sharp, solid squares by mapping modules using an `is_eye` coordinate check and drawing them as standard `1x1` square paths.
- **Asset Regeneration**: Regenerated all 10 `.svg` files in the `qr assets/` subfolders.


### V10 Update: Mask Circle Radius Reduced to Remove Thin Ring (Append-Only Ledger)
- **Mask Circle Radius Reduction**: Changed the white background circle radius in the SVG `<mask>` from `266.23` to `255`. This keeps the circle edge inside the black region of `PATH1` (radius 266.23), completely eliminating subpixel anti-aliasing artifacts (the thin outer circle) from rendering around the center 'D' logo.
- **Asset Regeneration**: Regenerated all 10 `.svg` files in the `qr assets/` subfolders.


### V11 Update: QR Code Tuner Tool Added (Append-Only Ledger)
- **Tuner Tool (tuner.html)**: Created a premium, standalone HTML5 Canvas interactive tool (`tuner.html`) that allows real-time tuning of the fading Cream circle gradient (solid core and outer radius) and "D" logo scale.
- **Git Tracking**: Added `tuner.html` to the repository, allowing it to be deployed on Vercel (accessible at `/tuner.html`).


### V12 Update: Visual Tuning to Match Canvas Aesthetic (Append-Only Ledger)
- **Visual Parameters Adjusted**: Refactored `generate_qr.py` to match the canvas aesthetic: circle scale `45%`, logo scale `35%`, and solid core `0%` (which starts the fading cream gradient immediately from the center of the logo).
- **Asset Regeneration**: Regenerated all 10 PNGs and 10 SVGs and copied them to Google Drive.


### V13 Update: Final Tuner Configuration Applied (Append-Only Ledger)
- **Final Tuner Parameters**: Applied the final user-approved parameters from the tuner screenshot: circle scale `60%`, D logo scale `50%`, and solid core `40%`. This renders the D logo significantly larger and more readable, with a wider solid Cream core gradient backing it.
- **Asset Regeneration**: Regenerated all 10 PNGs and 10 SVGs and copied them to Google Drive.


### V14 Update: Home/Website Endpoint Added (Append-Only Ledger)
- **Home/Website Endpoint**: Added a new redirect endpoint for the main `dankley.com/queens/` website. Created `home/index.html` to handle the redirection to `https://dankley.com/queens/`.
- **Home QR Generation**: Configured `generate_qr.py` with `HOME_URL = "https://dankley-queensqr.vercel.app/home"` and output directory `qr assets/queens_home`.
- **Asset Regeneration**: Generated both PNG and SVG formats under `qr assets/queens_home` and copied them to Google Drive.

### V15 Update: Verification & Sync of Home Redirection to /queens/ (Append-Only Ledger)
- **Live Redirection Verified**: Successfully confirmed that requests to the live Vercel route `https://dankley-queensqr.vercel.app/home` serve the updated redirect headers targeting `https://dankley.com/queens/`.
- **Google Drive Synchronization**: Regenerated all QR code files locally and copied the completed suite of PNG and SVG assets for all endpoints (including the newly confirmed `queens_home` redirection) to Google Drive.
