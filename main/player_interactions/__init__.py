# main/player_interactions/__init__.py

from main.player_interactions.ai_player import Bot
from main.player_interactions.human_player import Human

# Определяем список всех классов игроков
all_player_types = [Bot, Human]
