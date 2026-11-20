from arcade_engine.models import GameState, InputFlags, Projectile


class DeterministicArcadeEngine:
    def __init__(
        self,
        width: float = 800.0,
        height: float = 600.0,
        player_speed: float = 240.0,
        max_dt: float = 0.05,
    ) -> None:
        self.width = width
        self.height = height
        self.player_speed = player_speed
        self.max_dt = max_dt
        self.state = GameState()

    def set_input(self, **kwargs: bool) -> InputFlags:
        self.state.input_flags = self.state.input_flags.model_copy(update=kwargs)
        return self.state.input_flags

    def set_tab_blurred(self, blurred: bool) -> GameState:
        self.state.tab_blurred = blurred
        if blurred:
            self.state.paused = True
            self.state.input_flags = InputFlags()
        else:
            self.state.paused = False
        return self.state

    def spawn_projectile(
        self,
        x: float | None = None,
        y: float | None = None,
        vx: float = 0.0,
        vy: float = -400.0,
        width: float = 8.0,
        height: float = 16.0,
    ) -> Projectile:
        px = x if x is not None else self.state.player_pos.x + (self.state.player_size.x - width) / 2.0
        py = y if y is not None else self.state.player_pos.y - height
        proj = Projectile(x=px, y=py, vx=vx, vy=vy, width=width, height=height)
        self.state.projectiles.append(proj)
        return proj

    def spawn_target(
        self,
        x: float,
        y: float,
        width: float = 40.0,
        height: float = 24.0,
    ) -> Projectile:
        target = Projectile(x=x, y=y, vx=0.0, vy=0.0, width=width, height=height)
        self.state.targets.append(target)
        return target

    @staticmethod
    def aabb_overlap(a: Projectile, b: Projectile) -> bool:
        return (
            a.x < b.x + b.width
            and a.x + a.width > b.x
            and a.y < b.y + b.height
            and a.y + a.height > b.y
        )

    def step(self, raw_dt: float) -> GameState:
        if self.state.paused or self.state.tab_blurred:
            return self.state

        dt = min(max(raw_dt, 0.0), self.max_dt)
        flags = self.state.input_flags
        dx = (float(flags.right) - float(flags.left)) * self.player_speed * dt
        dy = (float(flags.down) - float(flags.up)) * self.player_speed * dt

        max_x = self.width - self.state.player_size.x
        max_y = self.height - self.state.player_size.y
        self.state.player_pos.x = min(max(self.state.player_pos.x + dx, 0.0), max_x)
        self.state.player_pos.y = min(max(self.state.player_pos.y + dy, 0.0), max_y)

        moved_projectiles: list[Projectile] = []
        for proj in self.state.projectiles:
            nx = proj.x + proj.vx * dt
            ny = proj.y + proj.vy * dt
            if 0.0 <= nx + proj.width and nx <= self.width and 0.0 <= ny + proj.height and ny <= self.height:
                moved_projectiles.append(proj.model_copy(update={"x": nx, "y": ny}))

        remaining_projectiles: list[Projectile] = []
        remaining_targets = list(self.state.targets)
        for proj in moved_projectiles:
            hit_index = next(
                (i for i, target in enumerate(remaining_targets) if self.aabb_overlap(proj, target)),
                None,
            )
            if hit_index is not None:
                remaining_targets.pop(hit_index)
                self.state.score += 100
            else:
                remaining_projectiles.append(proj)

        self.state.projectiles = remaining_projectiles
        self.state.targets = remaining_targets
        self.state.tick += 1
        self.state.elapsed_time += dt
        return self.state

    def restart(self) -> GameState:
        self.state = GameState()
        return self.state
