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
