"""Pytest suite for DeterministicArcadeEngine."""

import pytest
from arcade_engine.engine import DeterministicArcadeEngine


def test_movement_distance_invariance_30fps_vs_120fps() -> None:
    """Player movement distance over 1 second is invariant across 30fps and 120fps."""
    engine_30 = DeterministicArcadeEngine()
    engine_30.set_input(right=True)
    for _ in range(30):
        engine_30.step(1.0 / 30.0)

    engine_120 = DeterministicArcadeEngine()
    engine_120.set_input(right=True)
    for _ in range(120):
        engine_120.step(1.0 / 120.0)

    assert engine_30.state.player_pos.x == pytest.approx(
        engine_120.state.player_pos.x, abs=1e-6
    )
    assert engine_30.state.player_pos.x == pytest.approx(640.0, abs=1e-6)
    assert engine_30.state.elapsed_time == pytest.approx(1.0, abs=1e-6)
    assert engine_120.state.elapsed_time == pytest.approx(1.0, abs=1e-6)


def test_collision_boundary_score_update_and_projectile_clearing() -> None:
    """Projectile hitting a target updates score and clears both projectile and target."""
    engine = DeterministicArcadeEngine()
    engine.spawn_target(x=380.0, y=400.0, width=40.0, height=24.0)
    engine.spawn_projectile()

    # Step 10 times at dt=0.025s -> projectile y moves from 524.0 to 424.0 (strict boundary, no overlap yet)
    for _ in range(10):
        engine.step(0.025)

    assert engine.state.score == 0
    assert len(engine.state.projectiles) == 1
    assert len(engine.state.targets) == 1

    # One more step crosses into the target AABB
    engine.step(0.025)

    assert engine.state.score > 0
    assert len(engine.state.projectiles) == 0
    assert len(engine.state.targets) == 0


def test_clean_restart_resets_state_and_input_flags() -> None:
    """Restarting the engine resets position, score, entities, tick, and input flags."""
    engine = DeterministicArcadeEngine()
    engine.set_input(left=True, up=True, fire=True)
    engine.spawn_target(x=100.0, y=100.0)
    engine.spawn_projectile()
    engine.step(1.0 / 60.0)

    engine.restart()

    assert engine.state.tick == 0
    assert engine.state.elapsed_time == 0.0
    assert engine.state.score == 0
    assert engine.state.player_pos.x == 400.0
    assert engine.state.player_pos.y == 540.0
    assert engine.state.projectiles == []
    assert engine.state.targets == []
    assert engine.state.input_flags.left is False
    assert engine.state.input_flags.right is False
    assert engine.state.input_flags.up is False
    assert engine.state.input_flags.down is False
    assert engine.state.input_flags.fire is False


def test_tab_blur_pauses_simulation_step() -> None:
    """Tab blur pauses simulation steps until focus returns."""
    engine = DeterministicArcadeEngine()
    engine.set_input(right=True)
    engine.set_tab_blurred(True)

    engine.step(1.0 / 60.0)

    assert engine.state.tab_blurred is True
    assert engine.state.tick == 0
    assert engine.state.elapsed_time == 0.0
    assert engine.state.player_pos.x == 400.0

    engine.set_tab_blurred(False)
    engine.step(1.0 / 60.0)

    assert engine.state.tab_blurred is False
    assert engine.state.tick == 1
    assert engine.state.player_pos.x > 400.0
