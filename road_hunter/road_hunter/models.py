"""Data models and entities for Road Hunter."""

from enum import Enum
from typing import NamedTuple

class GameStatus(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

class ObstacleType(Enum):
    OIL_SLICK = "oil_slick"
    BARRIER = "barrier"

class CarType(Enum):
    PLAYER = "player"
    CRUISER = "cruiser"      # Drives straight, slow
    SWERVER = "swerver"      # Drives medium speed, swerves lanes
    RACER = "racer"          # Drives fast, moves toward player's lane

class Car:
    def __init__(self, x: float, y: float, car_type: CarType, lane: int = 1) -> None:
        self.x = x
        self.y = y
        self.car_type = car_type
        self.lane = lane
        self.width = 26
        self.height = 48
        
        # Physics attributes
        self.vx = 0.0
        self.speed = 0.0  # Forward speed (0 to max_speed)
        
        # AI/behavior attributes
        self.base_speed = 0.0
        self.swerve_timer = 0
        self.swerve_dir = 1
        
        # Initialize speed based on type
        if car_type == CarType.CRUISER:
            self.base_speed = 5.0
        elif car_type == CarType.SWERVER:
            self.base_speed = 8.0
            self.swerve_timer = 60  # swerve every 60 frames
        elif car_type == CarType.RACER:
            self.base_speed = 12.0
            self.swerve_timer = 40

    def get_rect(self) -> tuple[float, float, float, float]:
        """Returns the bounding box (x_left, y_top, width, height) of the car."""
        return self.x - self.width / 2, self.y - self.height / 2, self.width, self.height

class Obstacle:
    def __init__(self, x: float, y: float, obs_type: ObstacleType) -> None:
        self.x = x
        self.y = y
        self.obs_type = obs_type
        self.radius = 15 if obs_type == ObstacleType.OIL_SLICK else 12

    def get_rect(self) -> tuple[float, float, float, float]:
        return self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2

class FuelCanister:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.radius = 10

    def get_rect(self) -> tuple[float, float, float, float]:
        return self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2

class Particle:
    def __init__(self, x: float, y: float, vx: float, vy: float, color: tuple[int, int, int], size: float, lifetime: int) -> None:
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
