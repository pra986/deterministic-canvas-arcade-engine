# Architecture Overview

## Core Design Principles

1. **Frame-Rate-Independent Delta-Time Simulation**
   - Raw frame delta (`dt`) is clamped to `max_dt` (default `0.05s`) to prevent simulation tunneling after frame spikes.
   - Movement integrates velocity over `clamped_dt` so total displacement over a fixed elapsed duration is invariant across 30fps, 60fps, and 120fps.

2. **Automatic Tab-Blur Simulation Pause**
   - `set_tab_blurred(True)` pauses the simulation loop and clears active `InputFlags` so held keys do not stick when focus leaves the browser tab.
   - While `paused` is `True`, `step(dt)` is a no-op and returns the unchanged `GameState`.

3. **Deterministic AABB Collision Detection**
   - Projectiles and targets use axis-aligned bounding box (AABB) overlap checks.
   - Colliding projectiles are deterministically cleared and `score` is incremented without floating-point drift.

4. **Clean Restart State**
   - `restart()` resets `player_pos`, `score`, `tick`, `paused`, `tab_blurred`, clears all active `projectiles`, and resets `InputFlags` to all `False`.

## Module Layout

- `arcade_engine/models.py`: Pydantic data models (`Vec2`, `Projectile`, `InputFlags`, `GameState`).
- `arcade_engine/engine.py`: `DeterministicArcadeEngine` simulation core.
- `arcade_engine/cli.py`: Headless CLI demo entrypoint.
- `tests/test_engine.py`: Pytest verification suite.
