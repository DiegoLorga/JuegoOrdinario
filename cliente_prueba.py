import xmlrpc.client

# Conectarse al servidor RPC
proxy = xmlrpc.client.ServerProxy("http://localhost:9000/", allow_none=True)

# Registro del jugador
nombre = input("Ingresa tu nombre de jugador: ")
registrado = proxy.register_player(nombre)

if not registrado:
    print("Ese nombre ya está en uso. Intenta con otro.")
    exit()

# Verificar si es su turno
turno_actual = proxy.get_current_player()
if turno_actual != nombre:
    print(f"No es tu turno. Es el turno de: {turno_actual}")
    exit()

# Obtener pregunta del servidor
pregunta = proxy.get_question(nombre)
print("\n🧠 Pregunta:", pregunta["pregunta"])

# Enviar respuesta
respuesta = input("Tu respuesta: ")
mensaje, puntos, nivel = proxy.submit_answer(nombre, respuesta, pregunta["respuesta"])

# Mostrar resultados
print(f"{mensaje} | Puntos: {puntos} | Nivel: {nivel}")
print("🏁 Puntajes actuales:", proxy.get_scores())

# Avanzar turno
proxy.next_turn()
