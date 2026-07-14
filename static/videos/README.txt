===== VIDEO FILES — Total Tech Serve =====

HOME PAGE HERO BACKGROUND (already wired up — nothing to do):
==========================================
static/videos/hero/hero-1.mp4, hero-2.mp4, hero-3.mp4, hero-4.mp4 are already
in place and play automatically on the homepage, one after another on a loop,
with no pause/stop button. To swap a clip, just replace the file with the
same name (keep it named hero-1.mp4 etc.) — no code changes needed.

SERVICE CARD VIDEOS (Home page "What We Do" grid — already wired up):
==========================================
The 5 service cards on the homepage now play a looping video instead of a
static photo. Add your clips directly into this folder (static/videos/)
using these exact filenames:

1. amc.mp4        → IT AMC explainer video
2. repair.mp4     → Certified Repair Services video
3. network.mp4    → Infrastructure & Surveillance video
4. hardware.mp4   → New & Rental Hardware video
5. insurance.mp4  → Corporate & Individual Insurance video

Until a file is added, the card simply shows the existing thumbnail photo,
so nothing looks broken in the meantime.

HOW TO ADD VIDEOS TO RENDER (live site):
==========================================
Option A — Via GitHub (recommended):
1. Add your .mp4 files to this folder on your computer
2. Upload them to GitHub → static/videos/
3. Render auto-redeploys and videos appear on site

Option B — File size too big for GitHub (>25MB)?
1. Use a video hosting service like:
   - Vimeo (free): vimeo.com
   - YouTube (unlisted): youtube.com
2. Tell the developer to embed the video URL instead

FORMAT REQUIREMENTS:
- Format: MP4 (H.264)
- Resolution: 1920x1080 (Full HD)
- Duration: 30 seconds each
- Max size: 25MB each (for GitHub)
