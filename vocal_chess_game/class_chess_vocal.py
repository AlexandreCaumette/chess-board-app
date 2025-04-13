import re
import speech_recognition as sr
import logging


class ChessVocal:
    def __init__(self, actions: list = []):
        """This function initialize the instance of the class ChessVocal, which is the module that handles
        the vocal recognition and interpretation.

        Args:
            actions (list, optional): The list of the available actions to be recognized. Defaults to [].
        """
        self.logger = logging.getLogger(__name__)

        self.AVAILABLE_COMMANDS = actions
        self.AVAILABLE_PROMOTIONS = {
            "reine": "q",
            "pion": "p",
            "tour": "r",
            "cavalier": "n",
            "fou": "b",
        }

        self.logger.info("Vocal initialized")

    def clean_vocal_input(self, vocal_input: str) -> str:
        # Define the replacement function
        def replacement(match):
            number = match.group(1)
            unit_digit = number[1]
            return f"d{unit_digit}"

        # Correction de la reconnaissance vocale
        command = vocal_input.replace("dessin", "d7")
        command = command.replace("géant", "g1")
        command = command.replace("j'ai ", "g")
        command = command.replace("à ", "a")
        command = command.replace("à", "")
        command = command.replace("recette", "e7")
        command = command.replace("bessette", "b7")
        command = command.replace("baisser", "b7")
        command = command.replace(" ans ", " en ")
        command = command.replace("-", "")
        command = command.replace("un", "1")
        command = command.replace("détroit", "d3")
        command = command.replace("angers ", "en g")
        command = command.replace("aussi", "e6")
        command = command.replace("c'est ", "c")
        command = command.replace("des ", "d")
        command = command.replace("deux", "2")
        command = command.replace("annuler", "annule")
        command = command.replace("rennes", "reine")
        command = re.sub(pattern=r"\b(1[0-9])\b", repl=replacement, string=command)
        command = re.sub(pattern=r"\bans\b", repl="en", string=command)

        return command

    def recognize_speech(self) -> str:
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            try:
                self.logger.info("Speech recognizer listenning")

                audio = recognizer.listen(source)
                vocal_input = recognizer.recognize_google(
                    audio, language="fr-FR"
                ).lower()

                self.logger.debug(f"vocal input : <{vocal_input}>")

                cleaned_vocal_input = self.clean_vocal_input(vocal_input)

                self.logger.debug(f"cleaned vocal input : <{cleaned_vocal_input}>")

                command = self.interpret_vocal_input(cleaned_vocal_input)

                self.logger.debug(f"interpreted input : <{command}>")

                return command
            except sr.UnknownValueError:
                return None
            except sr.RequestError:
                self.logger.error("Speech recognition service unavailable")
        return None

    def interpret_promotion(self, words: list) -> str:
        if "promotion" not in words:
            return ""

        index_promotion = words.index("promotion")
        promotion = words[index_promotion + 1]

        return self.AVAILABLE_PROMOTIONS.get(promotion, "")

    def interpret_vocal_input(self, vocal_input: str) -> str:
        words = vocal_input.split()

        for command in self.AVAILABLE_COMMANDS:
            if command in words:
                return command

        if "en" not in words:
            raise Exception("Le mot clé 'en' n'est pas présent dans la commande")

        if len(words) < 3:
            raise Exception("La commande contient moins de 3 éléments")

        if any([len(word) < 2 for word in words]):
            raise Exception("Une des positions n'est pas complète")

        index_en = words.index("en")
        from_square = words[index_en - 1]
        to_square = words[index_en + 1]

        move = from_square + to_square

        promotion = self.interpret_promotion(words)

        return move + promotion
