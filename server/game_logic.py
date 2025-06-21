import random
import json

class GameLogic:
    def __init__(self):
        self.players = {}  # {nombre: {'puntos': 0, 'nivel': 1}}
        self.turn_order = []
        self.current_turn_index = 0
        self.load_questions()

    def load_questions(self):
        with open("questions.json", "r", encoding="utf-8") as f:
            self.questions = json.load(f)

    def register_player(self, name):
        if name in self.players:
            return False  # nombre repetido
        self.players[name] = {"puntos": 0, "nivel": 1}
        self.turn_order.append(name)
        return True

    def get_question(self, name):
        nivel = self.players[name]["nivel"]
        return random.choice(self.questions[f"nivel{nivel}"])

    def submit_answer(self, name, respuesta_usuario, respuesta_correcta):
        if respuesta_usuario == respuesta_correcta:
            self.players[name]["puntos"] += 10
            mensaje = "¡Correcto!"
        else:
            mensaje = "Incorrecto."

        # avanzar de nivel si puntaje supera 20
        if self.players[name]["puntos"] >= 20:
            self.players[name]["nivel"] = 2
        return mensaje, self.players[name]["puntos"], self.players[name]["nivel"]

    def get_scores(self):
        return {k: v["puntos"] for k, v in self.players.items()}

    def next_turn(self):
        self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)
        return self.turn_order[self.current_turn_index]

    def get_current_player(self):
        return self.turn_order[self.current_turn_index]

    def reset_game(self):
        for player in self.players:
            self.players[player] = {"puntos": 0, "nivel": 1}
        self.current_turn_index = 0
        return True
