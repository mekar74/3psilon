import random
from game.util import get_direction, position_equals
from game.models import GameObject, Board
from game.logic.base import BaseLogic

class Bowtie(BaseLogic):
    def __init__(self):
        super().__init__()
        self.goal_position = None
        self.tackle_cooldown = 0
        self.bot_id = None

    def next_move(self, board_bot: GameObject, board: Board):
        if self.bot_id is None:
            self.bot_id = board_bot.id

        current_position = board_bot.position
        props = board_bot.properties
        inventory = props.diamonds
        base = props.base

        if self._is_on_diamond(current_position, board.diamonds):
            return "collect"

        if self.tackle_cooldown > 0:
            self.tackle_cooldown -= 1

        # Periksa waktu tersisa apakah cukup untuk pulang
        distance_to_base = self._manhattan_distance(current_position, base)
        if props.milliseconds_left and props.milliseconds_left < distance_to_base * 1000:
            self.goal_position = base
        elif inventory >= props.inventory_size:
            self.goal_position = base
        else:
            best_diamond = self._find_best_diamond(board.diamonds, current_position)
            if best_diamond:
                self.goal_position = best_diamond.position

        enemy = self._find_enemy(board.bots, current_position)
        if enemy and enemy.properties.diamonds > 0 and self.tackle_cooldown == 0 and inventory < props.inventory_size // 2:
            self.goal_position = enemy.position
            self.tackle_cooldown = 3
            return "tackle"

        red_button = next((f for f in board.game_objects if f.type == "RedButtonGameObject"), None)
        if red_button and self._can_use_red_button(red_button, current_position, board.diamonds):
            self.goal_position = board.red_button.position

        teleporter = self._find_better_teleporter(board, current_position, self.goal_position)
        if teleporter:
            self.goal_position = teleporter.position

        if not self.goal_position:
            # Fallback: coba gerak menuju tengah board
            mid_x, mid_y = board.width // 2, board.height // 2
            self.goal_position = type(current_position)(x=mid_x, y=mid_y)

        return self._move_towards_goal(current_position, board, self.goal_position)

    def _is_on_diamond(self, current_position, diamonds):
        return any(position_equals(current_position, d.position) for d in diamonds)

    def _find_best_diamond(self, diamonds, current_position):
        best = None
        best_score = -float("inf")
        for d in diamonds:
            dist = self._manhattan_distance(current_position, d.position)
            if d.type == "red" and dist <= 5:
                score = 100 - dist  # Prioritaskan red dalam radius 5
            else:
                score = 10 - dist   # Diamond biasa atau red di luar radius
            if score > best_score:
                best_score = score
                best = d
        return best

    def _find_enemy(self, enemies, current_position):
        for e in enemies:
            if e.id != self.bot_id and self._manhattan_distance(current_position, e.position) == 1:
                return e
        return None

    def _can_use_red_button(self, red_button, current_position, diamonds):
        return self._manhattan_distance(current_position, red_button.position) <= 2 and len(diamonds) < 5

    def _find_better_teleporter(self, board, current_position, goal_position):
        if not goal_position:
            return None
        best_tele = None
        best_dist = self._manhattan_distance(current_position, goal_position)
        for t in getattr(board, "teleporters", []):
            dist = self._manhattan_distance(current_position, t.position) + self._manhattan_distance(t.position, goal_position)
            if dist < best_dist:
                best_dist = dist
                best_tele = t
        return best_tele

    def _move_towards_goal(self, current_position, board, goal_position):
        dx, dy = get_direction(current_position.x, current_position.y, goal_position.x, goal_position.y)
        if board.is_valid_move(current_position, dx, dy):
            return dx, dy
        else:
            return self._random_move()

    def _manhattan_distance(self, p1, p2):
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)

    def _random_move(self):
        return random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
