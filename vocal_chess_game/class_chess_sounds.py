import pygame
import os


class ChessSounds:
    def __init__(self):
        pygame.init()

        sound_directory = os.path.join("vocal_chess_game", "assets", "sounds")

        self.SOUNDS = {
            "knight": pygame.mixer.Sound(os.path.join(sound_directory, "horse.mp3")),
            "valid_move": pygame.mixer.Sound(
                os.path.join(sound_directory, "piece_move.mp3")
            ),
            "invalid_move": pygame.mixer.Sound(
                os.path.join(sound_directory, "wrong_move.mp3")
            ),
            "capture": pygame.mixer.Sound(
                os.path.join(sound_directory, "gun_shot.mp3")
            ),
            "suggestion": pygame.mixer.Sound(
                os.path.join(sound_directory, "suggestion.mp3")
            ),
            "check": pygame.mixer.Sound(os.path.join(sound_directory, "check.mp3")),
            "bishop": pygame.mixer.Sound(os.path.join(sound_directory, "bishop.mp3")),
            "king": pygame.mixer.Sound(os.path.join(sound_directory, "king.mp3")),
            "castling": pygame.mixer.Sound(
                os.path.join(sound_directory, "castling_move.mp3")
            ),
            "checkmate": pygame.mixer.Sound(
                os.path.join(sound_directory, "checkmate.mp3")
            ),
            "annule": pygame.mixer.Sound(os.path.join(sound_directory, "annule.mp3")),
            "magie": pygame.mixer.Sound(os.path.join(sound_directory, "magie.mp3")),
            "pawn_captured": pygame.mixer.Sound(
                os.path.join(sound_directory, "pawn_captured.mp3")
            ),
            "rook": pygame.mixer.Sound(os.path.join(sound_directory, "rook.mp3")),
            "roulette": pygame.mixer.Sound(
                os.path.join(sound_directory, "roulette.mp3")
            ),
            "zombie": pygame.mixer.Sound(os.path.join(sound_directory, "zombie.mp3")),
            "promotion": pygame.mixer.Sound(
                os.path.join(sound_directory, "promotion.mp3")
            ),
            "tremblement": pygame.mixer.Sound(
                os.path.join(sound_directory, "tremblement.mp3")
            ),
        }

    def play(self, sound: str):
        if sound in self.SOUNDS:
            self.SOUNDS[sound].play()
