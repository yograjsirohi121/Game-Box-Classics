"""Unit tests for Road Hunter gameplay logic."""

import pytest
from road_hunter.config import Difficulty, ROAD_CENTER, ROAD_L, ROAD_R, CAR_WIDTH
from road_hunter.game import RoadHunterGame
from road_hunter.models import GameStatus, Car, CarType, Obstacle, ObstacleType, FuelCanister

def test_game_start_and_reset():
    game = RoadHunterGame()
    game.start_game(Difficulty.MEDIUM)
    assert game.status == GameStatus.PLAYING
    assert game.fuel == 100.0
    assert game.score == 0
    assert game.player.x == ROAD_CENTER
    assert len(game.opponents) == 0
    assert len(game.obstacles) == 0

def test_player_lateral_movement():
    game = RoadHunterGame()
    game.start_game(Difficulty.EASY)
    
    # Steer right
    game.input_right = True
    game.step()
    assert game.player.vx > 0.0
    assert game.player.x > ROAD_CENTER

    # Release steer, verify drag friction reduces vx over time
    game.input_right = False
    game.step()
    vx_after_release = game.player.vx
    game.step()
    assert abs(game.player.vx) < abs(vx_after_release)

def test_player_road_boundaries():
    game = RoadHunterGame()
    game.start_game(Difficulty.EASY)
    
    # Force steer left until boundary is hit
    game.input_left = True
    for _ in range(100):
        game.step()
        
    half_w = CAR_WIDTH / 2
    min_x = ROAD_L + half_w
    assert game.player.x == min_x
    assert game.player.vx == 0.0

    # Force steer right until boundary is hit
    game.input_left = False
    game.input_right = True
    for _ in range(100):
        game.step()
        
    max_x = ROAD_R - half_w
    assert game.player.x == max_x
    assert game.player.vx == 0.0

def test_fuel_depletion():
    game = RoadHunterGame()
    game.start_game(Difficulty.MEDIUM)
    
    # Take a few steps and check fuel depletion
    start_fuel = game.fuel
    game.step()
    assert game.fuel < start_fuel
    
    # Acceleration should burn fuel faster
    game.start_game(Difficulty.MEDIUM)
    game.input_accel = True
    game.step()
    fuel_depleted_accel = 100.0 - game.fuel
    
    game.start_game(Difficulty.MEDIUM)
    game.input_accel = False
    game.step()
    fuel_depleted_normal = 100.0 - game.fuel
    
    assert fuel_depleted_accel > fuel_depleted_normal

def test_car_collision():
    game = RoadHunterGame()
    game.start_game(Difficulty.MEDIUM)
    game.invulnerable_timer = 0  # Disable startup invulnerability
    
    # Place opponent directly in front of the player
    op_car = Car(game.player.x, game.player.y - 10, CarType.CRUISER)
    game.opponents.append(op_car)
    
    # Step simulation -> collision check
    game.step()
    
    # Check that crash was triggered
    assert game.crash_timer > 0
    assert game.fuel == 75.0  # 100 - 25 penalty
    assert len(game.particles) > 0
    assert op_car not in game.opponents

def test_fuel_canister_collection():
    game = RoadHunterGame()
    game.start_game(Difficulty.MEDIUM)
    game.fuel = 50.0  # Decrease fuel first
    game.invulnerable_timer = 0
    
    # Place fuel canister at player's location
    fc = FuelCanister(game.player.x, game.player.y)
    game.fuel_canisters.append(fc)
    
    game.step()
    
    assert abs(game.fuel - 79.88) < 0.01  # 50 + 30 - 0.12 decay
    assert len(game.fuel_canisters) == 0
    assert len(game.particles) > 0

def test_oil_slick_spinout():
    game = RoadHunterGame()
    game.start_game(Difficulty.MEDIUM)
    game.invulnerable_timer = 0
    
    # Place oil slick at player's location
    oil = Obstacle(game.player.x, game.player.y, ObstacleType.OIL_SLICK)
    game.obstacles.append(oil)
    
    game.step()
    
    assert game.spinout_timer > 0
    assert len(game.obstacles) == 0

def test_barrier_collision():
    game = RoadHunterGame()
    game.start_game(Difficulty.MEDIUM)
    game.invulnerable_timer = 0
    
    # Place barrier at player's location
    barrier = Obstacle(game.player.x, game.player.y, ObstacleType.BARRIER)
    game.obstacles.append(barrier)
    
    game.step()
    
    assert game.crash_timer > 0
    assert game.fuel == 75.0
    assert len(game.obstacles) == 0
