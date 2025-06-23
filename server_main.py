from xmlrpc.server import SimpleXMLRPCServer
from server.game_logic import GameLogic


game = GameLogic()

server = SimpleXMLRPCServer(("localhost", 9000), allow_none=True)
print("Servidor RPC corriendo en puerto 9000...")

# Registrar métodos disponibles
server.register_function(game.register_player, "register_player")
server.register_function(game.get_question, "get_question")
server.register_function(game.submit_answer, "submit_answer")
server.register_function(game.get_scores, "get_scores")
server.register_function(game.next_turn, "next_turn")
server.register_function(game.get_current_player, "get_current_player")
server.register_function(game.reset_game, "reset_game")
server.register_function(game.enviar_tiempo, "enviar_tiempo")
server.register_function(game.obtener_clasificados_nivel, "obtener_clasificados_nivel")
server.register_function(game.verificar_clasificados_y_actualizar_niveles, "verificar_clasificados_y_actualizar_niveles")


server.serve_forever()
