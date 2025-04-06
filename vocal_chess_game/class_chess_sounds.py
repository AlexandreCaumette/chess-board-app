import pygame


class ChessSounds:
    def __init__(self):
        pygame.init()

        self.SOUNDS = {
            "knight": pygame.mixer.Sound("vocal_chess_game/assets/sounds/horse.mp3"),
            "valid_move": pygame.mixer.Sound(
                "vocal_chess_game/assets/sounds/piece_move.mp3"
            ),
            "invalid_move": pygame.mixer.Sound(
                "vocal_chess_game/assets/sounds/wrong_move.mp3"
            ),
            "capture": pygame.mixer.Sound(
                "vocal_chess_game/assets/sounds/gun_shot.mp3"
            ),
            "suggestion": pygame.mixer.Sound(
                "vocal_chess_game/assets/sounds/suggestion.mp3"
            ),
            "check": pygame.mixer.Sound("vocal_chess_game/assets/sounds/check.mp3"),
            "bishop": pygame.mixer.Sound("vocal_chess_game/assets/sounds/bishop.mp3"),
            "king": pygame.mixer.Sound("vocal_chess_game/assets/sounds/king.mp3"),
            "castling": pygame.mixer.Sound(
                "vocal_chess_game/assets/sounds/castling_move.mp3"
            ),
            "checkmate": pygame.mixer.Sound(
                "vocal_chess_game/assets/sounds/checkmate.mp3"
            ),
            "annule": pygame.mixer.Sound("vocal_chess_game/assets/sounds/annule.mp3"),
            "magie": pygame.mixer.Sound("vocal_chess_game/assets/sounds/magie.mp3"),
            "pawn_captured": pygame.mixer.Sound(
                "vocal_chess_game/assets/sounds/pawn_captured.mp3"
            ),
            "rook": pygame.mixer.Sound("vocal_chess_game/assets/sounds/rook.mp3"),
            "roulette": pygame.mixer.Sound(
                "vocal_chess_game/assets/sounds/roulette.mp3"
            ),
            "zombie": pygame.mixer.Sound("vocal_chess_game/assets/sounds/zombie.mp3"),
        }

    def play(self, sound: str):
        if sound in self.SOUNDS:
            self.SOUNDS[sound].play()
