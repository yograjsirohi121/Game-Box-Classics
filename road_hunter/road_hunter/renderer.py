"""Neon synthwave renderer for Road Hunter using pygame."""

import pygame
import random
from typing import Dict, Tuple
from road_hunter.config import (
    WIDTH,
    HEIGHT,
    HEADER_H,
    ROAD_L,
    ROAD_R,
    ROAD_WIDTH,
    LANE_LINE,
    ROAD_BORDER,
    BG,
    ROAD_BG,
    TEXT,
    TEXT_DIM,
    ACCENT,
    ACCENT_GREEN,
    ACCENT_YELLOW,
    ACCENT_PURPLE,
    OVERLAY,
    MENU_HOVER,
    DIFFICULTY_LABELS,
    DIFFICULTY_ORDER,
    CAR_WIDTH,
    CAR_HEIGHT,
    PADDING,
)
from road_hunter.game import RoadHunterGame
from road_hunter.models import GameStatus, Car, CarType, Obstacle, ObstacleType, FuelCanister

class Renderer:
    def __init__(self, fonts: Dict[str, pygame.font.Font]) -> None:
        self.fonts = fonts

    def draw_frame(self, surface: pygame.Surface, game: RoadHunterGame, tick: int) -> None:
        # 1. Fill base screen background
        surface.fill(BG)

        # 2. Draw playfield (road and borders)
        self._draw_road(surface, game)

        # 3. Draw game entities
        if game.status != GameStatus.MENU:
            self._draw_obstacles(surface, game)
            self._draw_fuel_canisters(surface, game, tick)
            self._draw_opponents(surface, game, tick)
            self._draw_player(surface, game, tick)
            self._draw_particles(surface, game)

        # 4. Draw header UI
        self._draw_header(surface, game)

        # 5. Overlays for menu, pause, game over
        if game.status == GameStatus.MENU:
            self._draw_menu(surface, game)
        elif game.status == GameStatus.PAUSED:
            self._draw_banner(surface, "PAUSED", "Press P to resume")
        elif game.status == GameStatus.GAME_OVER:
            self._draw_banner(
                surface,
                "GAME OVER",
                f"Score {game.score:05d}  ·  Press R to retry",
            )

    def _draw_road(self, surface: pygame.Surface, game: RoadHunterGame) -> None:
        # Road asphalt background
        road_rect = pygame.Rect(ROAD_L, HEADER_H, ROAD_WIDTH, HEIGHT - HEADER_H)
        pygame.draw.rect(surface, ROAD_BG, road_rect)

        # Scrolling side decor (horizontal lines to simulate vertical speed)
        sy = HEADER_H + (game.road_offset % 40) - 40
        while sy < HEIGHT:
            if sy >= HEADER_H:
                # Left shoulder line
                pygame.draw.line(surface, (38, 18, 70), (0, sy), (ROAD_L - 4, sy), 1)
                # Right shoulder line
                pygame.draw.line(surface, (38, 18, 70), (ROAD_R + 4, sy), (WIDTH, sy), 1)
            sy += 40

        # Glowing Neon Cyan Road Borders
        # Draw double lines to give it a laser effect
        pygame.draw.line(surface, (0, 100, 200), (ROAD_L - 3, HEADER_H), (ROAD_L - 3, HEIGHT), 2)
        pygame.draw.line(surface, ROAD_BORDER, (ROAD_L, HEADER_H), (ROAD_L, HEIGHT), 2)
        
        pygame.draw.line(surface, (0, 100, 200), (ROAD_R + 3, HEADER_H), (ROAD_R + 3, HEIGHT), 2)
        pygame.draw.line(surface, ROAD_BORDER, (ROAD_R, HEADER_H), (ROAD_R, HEIGHT), 2)

        # Scrolling Lane Dividers
        # Lanes separated at ROAD_L + 106 and ROAD_L + 212
        sep1 = ROAD_L + ROAD_WIDTH // 3
        sep2 = ROAD_L + (ROAD_WIDTH // 3) * 2
        
        y = HEADER_H + (game.road_offset % 60) - 60
        while y < HEIGHT:
            if y >= HEADER_H:
                pygame.draw.line(surface, LANE_LINE, (sep1, y), (sep1, min(y + 30, HEIGHT)), 1)
                pygame.draw.line(surface, LANE_LINE, (sep2, y), (sep2, min(y + 30, HEIGHT)), 1)
            y += 60

    def _draw_player(self, surface: pygame.Surface, game: RoadHunterGame, tick: int) -> None:
        # Crash flash animation
        if game.crash_timer > 0:
            # Render explosion frames
            radius = (60 - game.crash_timer) * 1.2
            if radius > 2:
                pygame.draw.circle(surface, (255, 150, 0), (int(game.player.x), int(game.player.y)), int(radius), 3)
                pygame.draw.circle(surface, (255, 230, 100), (int(game.player.x), int(game.player.y)), int(radius * 0.6))
            return

        # Flashing when invulnerable
        if game.invulnerable_timer > 0:
            if (tick // 6) % 2 == 0:
                return  # Skip draw

        # Underglow (neon pink glow)
        glow_surf = pygame.Surface((CAR_WIDTH + 16, CAR_HEIGHT + 16), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surf, (255, 0, 127, 45), (0, 0, CAR_WIDTH + 16, CAR_HEIGHT + 16))
        surface.blit(glow_surf, (game.player.x - (CAR_WIDTH + 16)/2, game.player.y - (CAR_HEIGHT + 16)/2))

        self._draw_vector_car(surface, game.player.x, game.player.y, ACCENT, is_player=True)

    def _draw_opponents(self, surface: pygame.Surface, game: RoadHunterGame, tick: int) -> None:
        for op in game.opponents:
            color = ACCENT_YELLOW
            if op.car_type == CarType.SWERVER:
                color = (255, 110, 0)
            elif op.car_type == CarType.RACER:
                color = (255, 40, 40)
            self._draw_vector_car(surface, op.x, op.y, color, is_player=False)

    def _draw_vector_car(self, surface: pygame.Surface, cx: float, cy: float, color: Tuple[int, int, int], is_player: bool) -> None:
        # Sleek vector polygon points relative to center (0, 0)
        # CAR_WIDTH = 26, CAR_HEIGHT = 48
        # We can construct the car shape points:
        w_half = CAR_WIDTH / 2
        h_half = CAR_HEIGHT / 2

        # Draw tires
        tire_color = (20, 20, 30)
        tire_w = 4
        tire_h = 10
        tires = [
            (-w_half - 1, -h_half + 6),  # Front Left
            (w_half - 3, -h_half + 6),   # Front Right
            (-w_half - 1, h_half - 16),  # Rear Left
            (w_half - 3, h_half - 16),   # Rear Right
        ]
        for tx, ty in tires:
            pygame.draw.rect(surface, tire_color, (cx + tx, cy + ty, tire_w, tire_h), border_radius=2)
            pygame.draw.rect(surface, color, (cx + tx, cy + ty, tire_w, tire_h), 1)

        # Body outline polygon
        if is_player:
            points = [
                (0, -h_half),             # Front nose tip
                (5, -h_half + 8),         # Front nose right
                (w_half, -h_half + 16),    # Front bumper right
                (w_half - 2, h_half - 8),  # Side body right
                (w_half, h_half),         # Rear spoiler right
                (-w_half, h_half),        # Rear spoiler left
                (-w_half + 2, h_half - 8), # Side body left
                (-w_half, -h_half + 16),   # Front bumper left
                (-5, -h_half + 8),        # Front nose left
            ]
        else:
            # AI cars look slightly different (sleek cruiser/truck look)
            points = [
                (-w_half + 3, -h_half),
                (w_half - 3, -h_half),
                (w_half, -h_half + 6),
                (w_half, h_half - 4),
                (w_half - 3, h_half),
                (-w_half + 3, h_half),
                (-w_half, h_half - 4),
                (-w_half, -h_half + 6),
            ]

        translated_points = [(cx + px, cy + py) for px, py in points]
        
        # Fill base car body with a slightly dark shade of the color
        dark_color = (max(0, color[0] // 3), max(0, color[1] // 3), max(0, color[2] // 3))
        pygame.draw.polygon(surface, dark_color, translated_points)
        # Glowing vector edge
        pygame.draw.polygon(surface, color, translated_points, 2)

        # Draw cockpit glass (cyan outline or black filled)
        glass_color = (0, 240, 255) if is_player else (255, 255, 255)
        glass_pts = [
            (cx - 4, cy - 6),
            (cx + 4, cy - 6),
            (cx + 6, cy + 6),
            (cx - 6, cy + 6),
        ]
        pygame.draw.polygon(surface, (10, 20, 30), glass_pts)
        pygame.draw.polygon(surface, glass_color, glass_pts, 1)

        # Headlights / Taillights
        if is_player:
            # Pink/magenta taillights
            pygame.draw.line(surface, ACCENT, (cx - w_half + 2, cy + h_half - 1), (cx - w_half + 6, cy + h_half - 1), 2)
            pygame.draw.line(surface, ACCENT, (cx + w_half - 6, cy + h_half - 1), (cx + w_half - 2, cy + h_half - 1), 2)
        else:
            # Yellow front headlights
            pygame.draw.circle(surface, (255, 255, 180), (int(cx - w_half + 3), int(cy - h_half + 2)), 2)
            pygame.draw.circle(surface, (255, 255, 180), (int(cx + w_half - 3), int(cy - h_half + 2)), 2)

    def _draw_obstacles(self, surface: pygame.Surface, game: RoadHunterGame) -> None:
        for ob in game.obstacles:
            if ob.obs_type == ObstacleType.OIL_SLICK:
                # Purple glowing puddle
                # Underglow
                pygame.draw.ellipse(surface, (157, 0, 255, 40), (ob.x - ob.radius, ob.y - ob.radius * 0.6, ob.radius * 2, ob.radius * 1.2))
                # Core
                pygame.draw.ellipse(surface, (30, 5, 50), (ob.x - ob.radius, ob.y - ob.radius * 0.6, ob.radius * 2, ob.radius * 1.2))
                pygame.draw.ellipse(surface, ACCENT_PURPLE, (ob.x - ob.radius, ob.y - ob.radius * 0.6, ob.radius * 2, ob.radius * 1.2), 2)
            else:
                # Barrier (barricade with neon yellow/black stripes)
                rect = pygame.Rect(ob.x - 14, ob.y - 8, 28, 16)
                pygame.draw.rect(surface, (20, 10, 0), rect)
                pygame.draw.rect(surface, ACCENT_YELLOW, rect, 2)
                # Draw hazard stripes
                pygame.draw.line(surface, ACCENT_YELLOW, (ob.x - 10, ob.y + 4), (ob.x - 2, ob.y - 4), 2)
                pygame.draw.line(surface, ACCENT_YELLOW, (ob.x, ob.y + 4), (ob.x + 8, ob.y - 4), 2)

    def _draw_fuel_canisters(self, surface: pygame.Surface, game: RoadHunterGame, tick: int) -> None:
        for fc in game.fuel_canisters:
            # Pulsing green glow
            pulse = 2 + int(random.uniform(0.0, 3.0)) if (tick // 4) % 2 == 0 else 3
            pygame.draw.circle(surface, (57, 255, 20, 60), (int(fc.x), int(fc.y)), fc.radius + pulse)
            
            # Draw diamond fuel cell icon
            pts = [
                (fc.x, fc.y - fc.radius),
                (fc.x + fc.radius, fc.y),
                (fc.x, fc.y + fc.radius),
                (fc.x - fc.radius, fc.y),
            ]
            pygame.draw.polygon(surface, (5, 40, 5), pts)
            pygame.draw.polygon(surface, ACCENT_GREEN, pts, 2)
            
            # "F" character inside the canister
            f_text = self.fonts["small"].render("F", True, ACCENT_GREEN)
            surface.blit(f_text, f_text.get_rect(center=(fc.x + 1, fc.y - 1)))

    def _draw_particles(self, surface: pygame.Surface, game: RoadHunterGame) -> None:
        for p in game.particles:
            # Fade out based on remaining lifetime
            alpha = int(255 * (p.lifetime / p.max_lifetime))
            p_color = p.color
            if len(p_color) == 3:
                # Add alpha if needed, but pygame draw.circle with custom alpha surface is cleaner.
                # Since we want it fast, we can just draw circle directly.
                pygame.draw.circle(surface, p_color, (int(p.x), int(p.y)), int(p.size))

    def _draw_header(self, surface: pygame.Surface, game: RoadHunterGame) -> None:
        # Header Box background
        header_rect = pygame.Rect(0, 0, WIDTH, HEADER_H)
        pygame.draw.rect(surface, BG, header_rect)
        pygame.draw.line(surface, ROAD_BORDER, (0, HEADER_H - 1), (WIDTH, HEADER_H - 1), 2)

        # Title (Road Hunter)
        title = self.fonts["title"].render("ROAD HUNTER", True, ACCENT)
        surface.blit(title, (PADDING, (HEADER_H - title.get_height()) // 2))

        if game.status != GameStatus.MENU:
            # Score
            score_str = f"SCORE: {game.score:05d}"
            score_text = self.fonts["score"].render(score_str, True, TEXT)
            surface.blit(score_text, (WIDTH - PADDING - score_text.get_width(), 10))

            # Fuel Indicator (Label + progress bar)
            fuel_lbl = self.fonts["small"].render("FUEL", True, TEXT_DIM)
            surface.blit(fuel_lbl, (220, 10))
            
            # Fuel bar background
            bar_w = 100
            bar_h = 10
            bar_x = 220
            bar_y = 28
            pygame.draw.rect(surface, (30, 20, 50), (bar_x, bar_y, bar_w, bar_h), border_radius=3)
            
            # Fuel bar fill
            fill_w = int(bar_w * (game.fuel / game.max_fuel))
            fill_color = ACCENT_GREEN
            if game.fuel < 30:
                # Flashes red if critically low
                fill_color = (255, 40, 40) if pygame.time.get_ticks() % 400 < 200 else (100, 0, 0)
            elif game.fuel < 60:
                fill_color = ACCENT_YELLOW
                
            if fill_w > 0:
                pygame.draw.rect(surface, fill_color, (bar_x, bar_y, fill_w, bar_h), border_radius=3)
            pygame.draw.rect(surface, TEXT_DIM, (bar_x, bar_y, bar_w, bar_h), 1, border_radius=3)

            # Speedometer (converts internal speed float to realistic mph value)
            speed_mph = int(game.player.speed * 8.5)
            speed_str = f"{speed_mph} MPH"
            speed_text = self.fonts["small"].render(speed_str, True, ACCENT_GREEN)
            surface.blit(speed_text, (WIDTH - PADDING - speed_text.get_width(), 32))

            # Difficulty tag
            diff_lbl = DIFFICULTY_LABELS[game.difficulty].upper()
            diff_text = self.fonts["small"].render(diff_lbl, True, TEXT_DIM)
            surface.blit(diff_text, (PADDING + 5, HEADER_H + 8))

    def _draw_menu(self, surface: pygame.Surface, game: RoadHunterGame) -> None:
        # Darkening overlay
        overlay = pygame.Surface((WIDTH, HEIGHT - HEADER_H), pygame.SRCALPHA)
        overlay.fill((10, 5, 25, 210))
        surface.blit(overlay, (0, HEADER_H))

        cx = WIDTH // 2
        y = HEADER_H + 60

        # Subtitle
        subtitle = self.fonts["small"].render("SELECT DIFFICULTY", True, TEXT_DIM)
        surface.blit(subtitle, subtitle.get_rect(centerx=cx, top=y))
        y += 50

        # Difficulty Selection Options
        for i, difficulty in enumerate(DIFFICULTY_ORDER):
            selected = (i == game.menu_index)
            label = DIFFICULTY_LABELS[difficulty]
            prefix = "▸ " if selected else "  "
            color = ACCENT if selected else TEXT
            
            # Add subtle neon hover box background
            if selected:
                h_rect = pygame.Rect(0, 0, 200, 36)
                h_rect.center = (cx, y + 14)
                pygame.draw.rect(surface, MENU_HOVER, h_rect, border_radius=6)
                pygame.draw.rect(surface, ACCENT, h_rect, 1, border_radius=6)

            text = self.fonts["menu"].render(f"{prefix}{label}", True, color)
            surface.blit(text, text.get_rect(centerx=cx, top=y))
            y += 50

        # Instructions / Help box
        y = HEIGHT - 180
        instructions = [
            "A D  or  ← →  to steer car",
            "W  or  ↑  to speed boost (burns fuel)",
            "S  or  ↓  to decelerate/brake",
            "Space/Enter to Start",
            "Esc  to Quit",
        ]
        
        # Border box around instructions
        box_w = 320
        box_h = 130
        box_rect = pygame.Rect(cx - box_w // 2, y - 10, box_w, box_h)
        pygame.draw.rect(surface, (22, 11, 46), box_rect, border_radius=8)
        pygame.draw.rect(surface, ROAD_BORDER, box_rect, 1, border_radius=8)

        for line in instructions:
            text_line = self.fonts["small"].render(line, True, TEXT_DIM)
            surface.blit(text_line, text_line.get_rect(centerx=cx, top=y))
            y += 22

    def _draw_banner(self, surface: pygame.Surface, title: str, subtitle: str) -> None:
        overlay = pygame.Surface((WIDTH, HEIGHT - HEADER_H), pygame.SRCALPHA)
        overlay.fill(OVERLAY)
        surface.blit(overlay, (0, HEADER_H))

        cx = WIDTH // 2
        cy = HEADER_H + (HEIGHT - HEADER_H) // 2

        # Draw a beautiful banner background box
        box_w = 340
        box_h = 120
        box_rect = pygame.Rect(cx - box_w // 2, cy - 60, box_w, box_h)
        pygame.draw.rect(surface, (22, 11, 46), box_rect, border_radius=10)
        pygame.draw.rect(surface, ACCENT, box_rect, 2, border_radius=10)

        main_text = self.fonts["banner"].render(title, True, TEXT)
        sub_text = self.fonts["small"].render(subtitle, True, TEXT_DIM)
        
        surface.blit(main_text, main_text.get_rect(center=(cx, cy - 15)))
        surface.blit(sub_text, sub_text.get_rect(center=(cx, cy + 20)))
