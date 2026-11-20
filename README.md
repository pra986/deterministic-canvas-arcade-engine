# Deterministic Canvas Arcade Engine

Project 32: Frame-rate-independent delta-time browser arcade physics engine with tab-blur pausing, clean restart state, and headless collision verification.

## Architecture
- **Deterministic Fixed-Timestep Core**: Clamps raw frame delta (`dt <= 0.05s`) and steps physics in fixed `1/60s` increments so gameplay is identical at 60Hz, 120Hz, or 144Hz.
- **Browser Visibility & Lifecycle Guard**: Automatically pauses simulation on `visibilitychange` / `blur` to prevent physics tunneling after tab switching.
- **Headless Physics Mirror**: Mirrors Canvas 2D entity math in Python for deterministic `pytest` collision, scoring, and restart verification.

## 6-Stage Workflow
1. **Input Sampling**: Capture keyboard/pointer state without mutating physics mid-step.
2. **Delta-Time Clamping**: Bound elapsed frame time to avoid spiral-of-death jumps.
3. **Fixed-Step Integration**: Advance paddle, ball, and projectile positions deterministically.
4. **AABB & Wall Collision Resolution**: Resolve swept collisions and update score/lives.
5. **Lifecycle & Tab-Blur Gating**: Freeze accumulator on `blur`/`hidden` and resume cleanly.
6. **Clean Restart & Telemetry**: Reset all entity vectors, score, and RNG seed to initial state.

## Data Contract
- `EngineConfig`: `width`, `height`, `fixed_dt`, `max_frame_dt`, `target_score`
- `EntityState`: `x`, `y`, `vx`, `vy`, `width`, `height`
- `GameSnapshot`: `tick`, `score_left`, `score_right`, `paused`, `game_over`, `ball`, `paddles`

## Production Controls
- Clamped delta-time accumulator (`MAX_FRAME_DT = 0.05`)
- Automatic pause on tab blur / `document.hidden`
- Zero-leak `reset()` restoring initial deterministic state
- Headless `pytest` collision & boundary regression suite

## Local Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

## Attribution
Built as Project 32 (X1: Supplement / AI Coder - Browser game: 3D shooter or Pong), inspired by **Ed Donner's AI Coder** course.
 clean restart state, and headless collision verification.
