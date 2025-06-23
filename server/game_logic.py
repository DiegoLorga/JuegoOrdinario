import random
import json

class GameLogic:
    def __init__(self):
        self.players = {}  # {nombre: {'puntos': 0, 'nivel': 1}}
        self.turn_order = []
        self.current_turn_index = 0
        self.load_questions()
        self.tiempos_por_nivel = {1: {}, 2: {}, 3: {}}  # {nivel: {nombre: tiempo_total}}
        self.nivel_actual = 1


    def load_questions(self):
        with open("server/questions.json", "r", encoding="utf-8") as f:
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
    
    def enviar_tiempo(self, nombre, tiempo):
        nivel = self.players[nombre]["nivel"]
        self.tiempos_por_nivel[nivel][nombre] = tiempo
        return True
    
    def obtener_clasificados_nivel(self, nivel, cuantos=2):
        if nivel not in self.tiempos_por_nivel:
            return []

        tiempos = self.tiempos_por_nivel[nivel]
        clasificados = sorted(tiempos.items(), key=lambda x: x[1])[:cuantos]
        return [nombre for nombre, _ in clasificados]

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
    
    def verificar_clasificados_y_actualizar_niveles(self):
        nivel = self.nivel_actual
        jugadores_terminados = set(self.tiempos_por_nivel[nivel].keys())
        jugadores_en_nivel = [nombre for nombre, datos in self.players.items() if datos["nivel"] == nivel]

        if len(jugadores_terminados) < len(jugadores_en_nivel):
            return False

        clasificados = self.obtener_clasificados_nivel(nivel, 2 if nivel == 1 else 1)

        for nombre in self.players:
            if nombre in clasificados:
                self.players[nombre]["nivel"] += 1
            else:
                if nombre in self.turn_order:
                    self.turn_order.remove(nombre)

        self.current_turn_index = 0
        self.nivel_actual += 1
        return clasificados


