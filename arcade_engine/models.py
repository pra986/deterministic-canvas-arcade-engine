from pydantic import BaseModel, Field


class Vec2(BaseModel):
    x: float = 0.0
    y: float = 0.0


class Projectile(BaseModel):
    x: float
    y: float
    vx: float = 0.0
    vy: float = -400.0
    width: float = 8.0
    height: float = 16.0


class InputFlags(BaseModel):
    left: bool = False
    right: bool = False
    up: bool = False
    down: bool = False
    fire: bool = False


class GameState(BaseModel):
    player_pos: Vec2 = Field(default_factory=lambda: Vec2(x=400.0, y=540.0))
    player_size: Vec2 = Field(default_factory=lambda: Vec2(x=40.0, y=24.0))
    projectiles: list[Projectile] = Field(default_factory=list)
    targets: list[Projectile] = Field(default_factory=list)
    input_flags: InputFlags = Field(default_factory=InputFlags)
    score: int = 0
    tick: int = 0
    elapsed_time: float = 0.0
    paused: bool = False
    tab_blurred: bool = False
