# Master Documentation: QR Codes (Redirection Router)
This document is an "Append-Only Immutable Ledger" detailing the architecture, API endpoints, and core logic of the QR_codes project. NEVER delete, summarize, or rewrite existing lines. Always append.

## MICROSERVICE IDENTITY
You are the `QR_codes` project. Your primary function is generating premium dynamic QR codes (with vector SVG module-merging aesthetics and central brand logos) and managing the HTML redirection endpoints deployed on Vercel to route physical materials (flyers, signs) to live landing pages.

## APPEND-ONLY LEDGER

### 2026-05-18 - Initial Implementation
- **Script File:** [generate_qr.py](file:///C:/Users/rockn/OneDrive/Desktop/Dk_queens/QR_codes/generate_qr.py) — Python script using `qrcode` and `pillow` to generate Dark Green (`#1A4331`) and Terracotta (`#E2725B`) dynamic QR codes routing to the Vercel app.
- **Routing File:** [index.html](file:///C:/Users/rockn/OneDrive/Desktop/Dk_queens/QR_codes/index.html) — Redirects root traffic to `https://dankley.com/store/`.
- **Routing File:** [events/index.html](file:///C:/Users/rockn/OneDrive/Desktop/Dk_queens/QR_codes/events/index.html) — Redirects traffic to active Eventbrite event pages.

### 2026-05-20 - V2 Update: Premium Aesthetic & Dynamic Consultation Routing
- **Script File:** [generate_qr.py](file:///C:/Users/rockn/OneDrive/Desktop/Dk_queens/QR_codes/generate_qr.py) — Updated generator to use `StyledPilImage` with `RoundedModuleDrawer()` to yield smooth, dotted data pixels. Configured color inversion (Dankley Cream `#fcf3da` data pixels on Dark Green `#2c4d43` or Terracotta `#cd6b48` backgrounds) and embedded the central logo using a circular mask.
- **Routing File:** [consultation/index.html](file:///C:/Users/rockn/OneDrive/Desktop/Dk_queens/QR_codes/consultation/index.html) — Created a new endpoint handling dynamic redirection to the consultation booking page.

### 2026-05-22 - V4 Update: Directions Endpoint Added
- **Script File:** [generate_qr.py](file:///C:/Users/rockn/OneDrive/Desktop/Dk_queens/QR_codes/generate_qr.py) — Added `DIRECTIONS_URL` constant pointing to `/directions` and generated matching QR code assets.
- **Routing File:** [directions/index.html](file:///C:/Users/rockn/OneDrive/Desktop/Dk_queens/QR_codes/directions/index.html) — Handles dynamic redirection to Google Maps directions for the storefront.

### 2026-05-24 - V5 Update: Fading Circle Background & Inverted D Mask
- **Script File:** [generate_qr.py](file:///C:/Users/rockn/OneDrive/Desktop/Dk_queens/QR_codes/generate_qr.py) — Implemented radial gradient masks to allow underlying QR pixels to fade smoothly near the central logo boundary. Configured `d_mask` and `hollow_mask` overlays to keep the inner loop of the 'D' solid while pasting the brand accent color.

### 2026-05-26 - V6 Update: Expanded Faded Circle & Decoupled Sizes
- **Script File:** [generate_qr.py](file:///C:/Users/rockn/OneDrive/Desktop/Dk_queens/QR_codes/generate_qr.py) — Decoupled the size of the fading background circle (scaled to 45% of QR width) from the D logo (35% of QR width), yielding a softer, broader glowing canvas.

### 2026-05-28 - V7 Update: Vector SVG Export Support Added
- **Script File:** [generate_qr.py](file:///C:/Users/rockn/OneDrive/Desktop/Dk_queens/QR_codes/generate_qr.py) — Added a new `generate_qr_svg` function to export vector SVG versions. Utilizes `<radialGradient>`, SVG `<mask>` overlays, and path definitions (`PATH1` and `PATH2` constants) to draw rounded modules (`rx="0.38" ry="0.38"`) and the central logo mark.

### 2026-06-03 - V8 Update: Events Redirection Target URL Updated
- **Routing File:** [events/index.html](file:///C:/Users/rockn/OneDrive/Desktop/Dk_queens/QR_codes/events/index.html) — Updated redirect destination to point to the active Eventbrite page for the "Dankleys 710 on 711" tickets.

### 2026-06-05 - V9 Update: Vector SVG Module Merging & Sharp Eyes
- **Script File:** [generate_qr.py](file:///C:/Users/rockn/OneDrive/Desktop/Dk_queens/QR_codes/generate_qr.py) — Refactored SVG generator to merge adjacent data modules into continuous rounded shapes (corner radius `r = 0.5`) while keeping the outer finder pattern squares sharp and solid.

### 2026-06-08 - V10 Update: Mask Circle Radius Reduced to Remove Thin Ring
- **Script File:** [generate_qr.py](file:///C:/Users/rockn/OneDrive/Desktop/Dk_queens/QR_codes/generate_qr.py) — Reduced mask circle radius from `266.23` to `255` to keep the circle edges inside the logo's bounds, eliminating the anti-aliasing outline artifact.

### 2026-06-10 - V11 Update: QR Code Tuner Tool Added
- **Web UI File:** [tuner.html](file:///C:/Users/rockn/OneDrive/Desktop/Dk_queens/QR_codes/tuner.html) — Created a premium HTML5 canvas interactive tuner tool allowing real-time adjustment of gradient masks and logo proportions.

### 2026-06-20 - Supporting Utilities
- **Script File:** [analyze.py](file:///C:/Users/rockn/OneDrive/Desktop/Dk_queens/QR_codes/analyze.py) — Inspects color metrics of generated images to verify compliance.
- **Script File:** [crop_logo.py](file:///C:/Users/rockn/OneDrive/Desktop/Dk_queens/QR_codes/crop_logo.py) — Crops brand assets into the central round badge dimensions.

### 2026-08-25 - V17 Update: Events Redirection Target URL Updated
- **Routing File:** [events/index.html](file:///C:/Users/rockn/OneDrive/Desktop/Dk_queens/QR_codes/events/index.html) — Updated active event redirect target to `https://www.eventbrite.com/e/1998451944563?aff=oddtdtcreator` for dynamic routing through `https://dankley-queensqr.vercel.app/events`.

