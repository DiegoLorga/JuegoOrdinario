import xmlrpc.client

class RPCClient:
    def __init__(self, server_url="http://localhost:9000/"):
        self.proxy = xmlrpc.client.ServerProxy(server_url, allow_none=True)

    def register(self, name):
        return self.proxy.register_player(name)

    def get_question(self, name):
        return self.proxy.get_question(name)

    def submit_answer(self, name, user_answer, correct_answer):
        return self.proxy.submit_answer(name, user_answer, correct_answer)

    def get_scores(self):
        return self.proxy.get_scores()

    def get_current_turn(self):
        return self.proxy.get_current_player()

    def next_turn(self):
        return self.proxy.next_turn()

    def reset_game(self):
        return self.proxy.reset_game()
    
    def enviar_tiempo(self, nombre, tiempo):
        return self.proxy.enviar_tiempo(nombre, tiempo)

    def obtener_clasificados_nivel(self, nivel, cuantos=2):
        return self.proxy.obtener_clasificados_nivel(nivel, cuantos)
    
    def verificar_clasificados_y_actualizar_niveles(self):
       return self.proxy.verificar_clasificados_y_actualizar_niveles()

