"""Core gameplay logic and simulation for Road Hunter."""

import random
from typing import List, Tuple
from road_hunter.config import (
    Difficulty,
    DIFFICULTY_SETTINGS,
    ROAD_L,
    ROAD_R,
    ROAD_WIDTH,
    ROAD_CENTER,
    LANE_CENTERS,
    CAR_WIDTH,
    CAR_HEIGHT,
    FUEL_RADIUS,
    OIL_RADIUS,
    WIDTH,
    HEIGHT,
    ACCENT_GREEN,
    ACCENT_PURPLE,
    LANE_WIDTH,
)
from road_hunter.models import (
    GameStatus,
    Car,
    CarType,
    Obstacle,
    ObstacleType,
    FuelCanister,
    Particle,
)

class RoadHunterGame:
    def __init__(self) -> None:
        self.status = GameStatus.MENU
        self.difficulty = Difficulty.MEDIUM
        self.score = 0
        self.high_score = 0
        self.fuel = 100.0
        self.max_fuel = 100.0
        self.distance_traveled = 0.0
        
        # Player state
        self.player: Car = Car(ROAD_CENTER, HEIGHT - 120, CarType.PLAYER)
        self.input_left = False
        self.input_right = False
        self.input_accel = False
        self.input_brake = False
        
        # Timers
        self.spinout_timer = 0
        self.crash_timer = 0
        self.invulnerable_timer = 0
        self.spawn_timer = 0
        self.menu_index = 1  # 0: Easy, 1: Medium, 2: Hard
        
        # Entities
        self.opponents: List[Car] = []
        self.obstacles: List[Obstacle] = []
        self.fuel_canisters: List[FuelCanister] = []
        self.particles: List[Particle] = []
        
        # Scrolling road offset (for visuals)
        self.road_offset = 0.0

    def start_game(self, difficulty: Difficulty) -> None:
        self.status = GameStatus.PLAYING
        self.difficulty = difficulty
        self.score = 0
        self.fuel = 100.0
        self.distance_traveled = 0.0
        self.spinout_timer = 0
        self.crash_timer = 0
        self.invulnerable_timer = 60  # Brief shield at start
        self.spawn_timer = 0
        
        self.opponents.clear()
        self.obstacles.clear()
        self.fuel_canisters.clear()
        self.particles.clear()
        
        self.player = Car(ROAD_CENTER, HEIGHT - 120, CarType.PLAYER)
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        self.player.speed = settings["scroll_speed_min"]

    def reset_player(self) -> None:
        self.player.x = ROAD_CENTER
        self.player.vx = 0.0
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        self.player.speed = settings["scroll_speed_min"]
        self.spinout_timer = 0
        self.crash_timer = 0
        self.invulnerable_timer = 120  # 2 seconds shield after crash

    def step(self) -> None:
        """Advance the game simulation by one frame."""
        if self.status != GameStatus.PLAYING:
            return
            
        settings = DIFFICULTY_SETTINGS[self.difficulty]
        
        # Decr timers
        if self.spinout_timer > 0:
            self.spinout_timer -= 1
        if self.crash_timer > 0:
            self.crash_timer -= 1
            if self.crash_timer == 0:
                if self.fuel <= 0:
                    self.status = GameStatus.GAME_OVER
                    if self.score > self.high_score:
                        self.high_score = self.score
                else:
                    self.reset_player()
            self._update_particles()
            # Scroll road and background items slowly during crash to simulate sliding to halt
            self.player.speed = max(0.0, self.player.speed - 0.2)
            self._update_items(self.player.speed)
            self._update_opponents(self.player.speed)
            return

        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1

        # 1. Update Player speed and position
        self._update_player(settings)
        
        # 2. Update entities (obstacles, opponents, fuel, particles)
        self._update_items(self.player.speed)
        self._update_opponents(self.player.speed)
        self._update_particles()
        
        # 3. Check collisions
        self._check_collisions()
        
        # 4. Spawn new entities
        self._spawn_entities(settings)
        
        # 5. Fuel depletion & distance scoring
        if self.status == GameStatus.PLAYING and self.crash_timer == 0:
            # Fuel decays based on time + speed factor
            decay = settings["fuel_decay_rate"]
            if self.input_accel:
                decay *= 1.5  # Burning fuel faster during speed boost
            self.fuel = max(0.0, self.fuel - decay)
            
            if self.fuel <= 0.0:
                # Trigger out of fuel crash/stop
                self.trigger_crash()
                
            # Score updates based on forward speed and difficulty multiplier
            self.distance_traveled += self.player.speed / 60.0
            self.score = int(self.distance_traveled * 10 * settings["score_multiplier"])

    def _update_player(self, settings) -> None:
        # Forward speed physics
        target_speed = settings["scroll_speed_min"]
        accel_rate = 0.05
        
        if self.input_accel:
            target_speed = settings["scroll_speed_max"]
            accel_rate = 0.15
        elif self.input_brake:
            target_speed = settings["scroll_speed_min"] * 0.5
            accel_rate = 0.3
            
        # Smoothly interpolate speed
        if self.player.speed < target_speed:
            self.player.speed = min(target_speed, self.player.speed + accel_rate)
        elif self.player.speed > target_speed:
            self.player.speed = max(target_speed, self.player.speed - accel_rate)
            
        # Lateral movement (steering)
        # Apply inputs if not spinning out
        ax = 0.0
        if self.spinout_timer > 0:
            # Swerve randomly during spinout
            ax = random.choice([-1.2, 1.2])
        else:
            if self.input_left:
                ax -= 0.8
            if self.input_right:
                ax += 0.8
                
        # Update horizontal velocity with inertia and drag
        self.player.vx += ax
        self.player.vx *= 0.82  # Drag friction
        
        # Update position
        self.player.x += self.player.vx
        
        # Keep inside road borders
        half_w = CAR_WIDTH / 2
        min_x = ROAD_L + half_w
        max_x = ROAD_R - half_w
        if self.player.x < min_x:
            self.player.x = min_x
            self.player.vx = 0.0
        elif self.player.x > max_x:
            self.player.x = max_x
            self.player.vx = 0.0
            
        # Road scrolling effect offset
        self.road_offset = (self.road_offset + self.player.speed) % 100

    def _update_items(self, speed: float) -> None:
        # Move items down relative to player speed
        # Oil, barrier, and fuel are stationary on road, so dy = speed
        for item in self.obstacles:
            item.y += speed
        for item in self.fuel_canisters:
            item.y += speed
            
        # Filter out items that scrolled off screen
        self.obstacles = [ob for ob in self.obstacles if ob.y < HEIGHT + 100]
        self.fuel_canisters = [fc for fc in self.fuel_canisters if fc.y < HEIGHT + 100]

    def _update_opponents(self, speed: float) -> None:
        for op in self.opponents:
            # Relative vertical movement: op.base_speed is forward speed of opponent
            # op.y moves down relative to player: speed - op.base_speed
            op.y += (speed - op.base_speed)
            
            # Opponent behaviors
            if op.car_type == CarType.SWERVER:
                op.swerve_timer -= 1
                if op.swerve_timer <= 0:
                    op.swerve_timer = random.randint(40, 80)
                    op.swerve_dir *= -1
                op.vx = op.swerve_dir * 1.5
                op.x += op.vx
            elif op.car_type == CarType.RACER:
                # Racer targets the player's horizontal lane
                op.swerve_timer -= 1
                if op.swerve_timer <= 0:
                    op.swerve_timer = random.randint(30, 60)
                    # Steer slightly toward player x
                    dx = self.player.x - op.x
                    if abs(dx) > 10:
                        op.vx = 2.0 if dx > 0 else -2.0
                    else:
                        op.vx = 0.0
                op.x += op.vx
                
            # Maintain bounds within the road
            half_w = CAR_WIDTH / 2
            min_x = ROAD_L + half_w
            max_x = ROAD_R - half_w
            if op.x < min_x:
                op.x = min_x
                op.vx *= -1
            elif op.x > max_x:
                op.x = max_x
                op.vx *= -1
                
        # Filter out off-screen opponents (both too far ahead or too far behind)
        self.opponents = [op for op in self.opponents if -150 < op.y < HEIGHT + 150]

    def _update_particles(self) -> None:
        for p in self.particles:
            p.x += p.vx
            p.y += p.vy
            p.lifetime -= 1
        self.particles = [p for p in self.particles if p.lifetime > 0]

    def _check_collisions(self) -> None:
        if self.invulnerable_timer > 0 or self.crash_timer > 0:
            return
            
        px_left, py_top, pw, ph = self.player.get_rect()
        
        # 1. Collision with Opponent Cars
        for op in self.opponents:
            ox_left, oy_top, ow, oh = op.get_rect()
            if (px_left < ox_left + ow and px_left + pw > ox_left and
                py_top < oy_top + oh and py_top + ph > oy_top):
                # Crash!
                self.trigger_crash()
                # Spawn explosion particles
                self.spawn_particles(self.player.x, self.player.y, (255, 100, 0), count=25)
                self.spawn_particles(op.x, op.y, (255, 230, 0), count=15)
                # Remove this opponent
                self.opponents.remove(op)
                return

        # 2. Collision with Obstacles
        for ob in self.obstacles:
            ox_left, oy_top, ow, oh = ob.get_rect()
            if (px_left < ox_left + ow and px_left + pw > ox_left and
                py_top < oy_top + oh and py_top + ph > oy_top):
                if ob.obs_type == ObstacleType.BARRIER:
                    self.trigger_crash()
                    self.spawn_particles(self.player.x, self.player.y, (200, 200, 200), count=20)
                    self.obstacles.remove(ob)
                    return
                elif ob.obs_type == ObstacleType.OIL_SLICK:
                    self.trigger_spinout()
                    self.spawn_particles(ob.x, ob.y, ACCENT_PURPLE, count=8)
                    self.obstacles.remove(ob)
                    break

        # 3. Collision with Fuel Canisters
        for fc in self.fuel_canisters:
            fx_left, fy_top, fw, fh = fc.get_rect()
            if (px_left < fx_left + fw and px_left + pw > fx_left and
                py_top < fy_top + fh and py_top + ph > fy_top):
                # Pick up fuel
                self.fuel = min(self.max_fuel, self.fuel + 30.0)
                # Green spark particles
                self.spawn_particles(fc.x, fc.y, ACCENT_GREEN, count=12)
                self.fuel_canisters.remove(fc)
                break

    def trigger_crash(self) -> None:
        self.crash_timer = 60  # Locked for 1 second (60 frames)
        self.fuel = max(0.0, self.fuel - 25.0)  # Heavy penalty
        
    def trigger_spinout(self) -> None:
        self.spinout_timer = 50  # Loss of control for 50 frames
        self.player.speed = max(3.0, self.player.speed - 3.0)  # Slow down

    def spawn_particles(self, x: float, y: float, color: Tuple[int, int, int], count: int = 10) -> None:
        for _ in range(count):
            vx = random.uniform(-4.0, 4.0)
            vy = random.uniform(-4.0, 4.0)
            size = random.uniform(2.0, 5.0)
            lifetime = random.randint(15, 35)
            self.particles.append(Particle(x, y, vx, vy, color, size, lifetime))

    def _spawn_entities(self, settings) -> None:
        self.spawn_timer += 16.67  # roughly 16.67ms per frame at 60fps
        interval = settings["spawn_interval_ms"]
        
        if self.spawn_timer >= interval:
            self.spawn_timer = 0
            
            # Decide what to spawn
            lane = random.choice([0, 1, 2])
            spawn_x = LANE_CENTERS[lane]
            spawn_y = -80.0
            
            # Ensure lane is clear of close objects
            for op in self.opponents:
                if op.lane == lane and op.y < 120:
                    return # Skip spawning to avoid overlay
            for ob in self.obstacles:
                # Approximate lane check
                if abs(ob.x - spawn_x) < LANE_WIDTH / 2 and ob.y < 120:
                    return
            for fc in self.fuel_canisters:
                if abs(fc.x - spawn_x) < LANE_WIDTH / 2 and fc.y < 120:
                    return
                    
            r = random.random()
            
            # Spawning rules:
            # 55% chance opponent car
            # 20% chance fuel canister (spawns more frequently if fuel is low!)
            # 25% chance road obstacle (oil or barrier)
            fuel_threshold = 0.20 if self.fuel < 40.0 else 0.15
            
            if r < settings["traffic_density"]:
                # Spawn opponent car
                car_roll = random.random()
                if car_roll < 0.5:
                    ctype = CarType.CRUISER
                elif car_roll < 0.8:
                    ctype = CarType.SWERVER
                else:
                    ctype = CarType.RACER
                self.opponents.append(Car(spawn_x, spawn_y, ctype, lane))
            elif r < settings["traffic_density"] + fuel_threshold:
                # Spawn fuel
                self.fuel_canisters.append(FuelCanister(spawn_x, spawn_y))
            else:
                # Spawn obstacle
                obs_type = ObstacleType.OIL_SLICK if random.random() < 0.6 else ObstacleType.BARRIER
                self.obstacles.append(Obstacle(spawn_x, spawn_y, obs_type))

    def menu_up(self) -> None:
        self.menu_index = (self.menu_index - 1) % 3

    def menu_down(self) -> None:
        self.menu_index = (self.menu_index + 1) % 3

    def start_from_menu(self) -> None:
        diffs = [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]
        self.start_game(diffs[self.menu_index])

    def toggle_pause(self) -> None:
        if self.status == GameStatus.PLAYING:
            self.status = GameStatus.PAUSED
        elif self.status == GameStatus.PAUSED:
            self.status = GameStatus.PLAYING

    def return_to_menu(self) -> None:
        self.status = GameStatus.MENU

    def reset(self) -> None:
        self.start_game(self.difficulty)

