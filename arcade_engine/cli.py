"""Runnable CLI demo entrypoint for the deterministic canvas arcade engine."""

import argparse
import json
from arcade_engine.engine import DeterministicArcadeEngine


def run_demo(fps: int = 60, duration: float = 1.0) -> dict:
    """Run a deterministic simulation demo and return the final state summary."""
    engine = DeterministicArcadeEngine()
    engine.spawn_target(x=400.0, y=200.0, width=40.0, height=24.0)
    engine.set_input(right=True)

    dt = 1.0 / fps
    steps = int(round(duration * fps))
    for step_idx in range(steps):
        if step_idx == steps // 4:
            engine.spawn_projectile()
        engine.step(dt)

    return {
        "fps": fps,
        "steps": steps,
        "tick": engine.state.tick,
        "elapsed_time": round(engine.state.elapsed_time, 6),
        "player_pos": {
            "x": round(engine.state.player_pos.x, 4),
            "y": round(engine.state.player_pos.y, 4),
        },
        "score": engine.state.score,
        "active_projectiles": len(engine.state.projectiles),
        "remaining_targets": len(engine.state.targets),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run deterministic canvas arcade engine CLI demo."
    )
    parser.add_argument("--fps", type=int, default=60, help="Simulation frame rate.")
    parser.add_argument(
        "--duration", type=float, default=1.0, help="Simulation duration in seconds."
    )
    args = parser.parse_args()
    summary = run_demo(fps=args.fps, duration=args.duration)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
