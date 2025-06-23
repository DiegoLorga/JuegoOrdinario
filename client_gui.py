import time
import tkinter as tk
from tkinter import messagebox
from rpc_client import RPCClient

class CarreraNumericaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Carrera Numérica")
        self.root.geometry("400x300")
        self.rpc = RPCClient()
        self.nombre = ""
        self.pregunta_actual = None
        self.total_preguntas_nivel = 5
        self.preguntas_contestadas = 0
        self.inicio_tiempo = None
        self.tiempo_maximo_nivel3 = 60  # segundos
        self.cronometro_activo = False



        self.pantalla_inicio()

    def pantalla_inicio(self):
        self.clear()
        tk.Label(self.root, text="Bienvenido a Carrera Numérica", font=("Arial", 14)).pack(pady=10)

        tk.Label(self.root, text="Tu nombre:").pack()
        self.nombre_entry = tk.Entry(self.root)
        self.nombre_entry.pack()

        tk.Button(self.root, text="Ingresar", command=self.registrar_jugador).pack(pady=10)
        tk.Button(self.root, text="Instrucciones", command=self.mostrar_instrucciones).pack()
        tk.Button(self.root, text="Acerca de", command=self.mostrar_acerca).pack()

    def registrar_jugador(self):
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            messagebox.showwarning("Nombre vacío", "Por favor ingresa tu nombre.")
            return
        if not self.rpc.register(nombre):
            messagebox.showerror("Nombre en uso", "Ese nombre ya fue tomado.")
            return

        self.nombre = nombre
        self.verificar_turno()

    def verificar_turno(self):
        turno = self.rpc.get_current_turn()
        if turno == self.nombre:
            self.mostrar_pregunta()
        else:
            self.clear()
            tk.Label(self.root, text=f"Esperando tu turno...\nTurno actual: {turno}", font=("Arial", 12)).pack(pady=20)
            self.root.after(3000, self.verificar_turno)
            
    
    
    def mostrar_pregunta(self):
        if self.preguntas_contestadas == 0:
            self.inicio_tiempo = time.time()
            if self.rpc.get_scores()[self.nombre] >= 40:  # estás en nivel 3
                self.iniciar_cronometro_nivel3()

        self.clear()
        self.pregunta_actual = self.rpc.get_question(self.nombre)

        tk.Label(self.root, text=f"Pregunta {self.preguntas_contestadas + 1} de {self.total_preguntas_nivel}", font=("Arial", 12)).pack(pady=5)
        tk.Label(self.root, text=self.pregunta_actual["pregunta"], font=("Arial", 14)).pack(pady=10)

        self.respuesta_entry = tk.Entry(self.root)
        self.respuesta_entry.pack()

        tk.Button(self.root, text="Enviar respuesta", command=self.enviar_respuesta).pack(pady=10)



    def enviar_respuesta(self):
        respuesta_usuario = self.respuesta_entry.get().strip()
        if not respuesta_usuario:
            messagebox.showwarning("Sin respuesta", "Escribe una respuesta antes de enviar.")
            return

        mensaje, puntos, nivel = self.rpc.submit_answer(
            self.nombre,
            respuesta_usuario,
            self.pregunta_actual["respuesta"]
        )

        self.preguntas_contestadas += 1

        if self.preguntas_contestadas < self.total_preguntas_nivel:
            messagebox.showinfo(
                "Respuesta",
                f"{mensaje}\n(Pregunta {self.preguntas_contestadas}/{self.total_preguntas_nivel})"
            )
            self.mostrar_pregunta()
        else:
            # Terminó sus 5 preguntas
            duracion = time.time() - self.inicio_tiempo
            self.preguntas_contestadas = 0

            # Si es nivel 3, evaluar si ganó o perdió (cronómetro aún activo)
            if nivel == 3:
                if self.cronometro_activo:
                    self.cronometro_activo = False  # detener el contador
                    messagebox.showinfo("¡Felicidades!", "🎉 ¡Completaste el nivel 3 a tiempo y ganaste el juego!")
                    self.clear()
                    tk.Label(self.root, text="🏆 Ganaste Carrera Numérica 🏆", font=("Arial", 16)).pack(pady=30)
                    tk.Button(self.root, text="🔄 Reiniciar juego", command=self.reiniciar_juego).pack(pady=10)
                    return
                else:
                    # Ya fue bloqueado por el cronómetro, no se debería llegar aquí.
                    return

            # Para nivel 1 y 2: enviar tiempo, verificar clasificación
            self.rpc.enviar_tiempo(self.nombre, duracion)

            messagebox.showinfo(
                "Nivel terminado",
                f"Terminaste tus 5 preguntas.\nTiempo total: {duracion:.2f} segundos"
            )

            clasificados = self.rpc.verificar_clasificados_y_actualizar_niveles()

            if clasificados and self.nombre not in clasificados:
                messagebox.showinfo("Ronda finalizada", "No clasificaste. Gracias por jugar.")
                self.clear()
                tk.Label(self.root, text="Fin del juego para ti.", font=("Arial", 14)).pack(pady=20)
                return

            elif clasificados and self.nombre in clasificados:
                messagebox.showinfo("¡Felicidades!", "Clasificaste al siguiente nivel.")

            # Continuar turno (si sigue en juego)
            self.rpc.next_turn()
            self.verificar_turno()




    def mostrar_instrucciones(self):
        messagebox.showinfo("Instrucciones", "Responde correctamente para avanzar. ¡Llega a 20 puntos para subir de nivel!")

    def mostrar_acerca(self):
        messagebox.showinfo("Acerca de", "Carrera Numérica v1.0\nCreado por Humano para SPD 2025")

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def iniciar_cronometro_nivel3(self):
        self.cronometro_activo = True
        self.tiempo_restante = self.tiempo_maximo_nivel3
        self.etiqueta_cronometro = tk.Label(self.root, text=f"⏳ Tiempo restante: {self.tiempo_restante}s", font=("Arial", 10))
        self.etiqueta_cronometro.pack()

        self.actualizar_cronometro()

    def actualizar_cronometro(self):
        if not self.cronometro_activo:
            return

        self.tiempo_restante -= 1
        self.etiqueta_cronometro.config(text=f"⏳ Tiempo restante: {self.tiempo_restante}s")

        if self.tiempo_restante <= 0:
            self.cronometro_activo = False
            messagebox.showinfo("Tiempo agotado", "¡Se acabó el tiempo! No lograste completar el nivel.")
            self.clear()
            tk.Label(self.root, text="Fin del juego. ¡Inténtalo de nuevo!", font=("Arial", 14)).pack(pady=20)
            return

        self.root.after(1000, self.actualizar_cronometro)
    
    def reiniciar_juego(self):
        confirmado = messagebox.askyesno("Reiniciar juego", "¿Estás seguro de reiniciar el juego para todos?")
        if confirmado:
            self.rpc.reset_game()
            messagebox.showinfo("Reiniciado", "El juego ha sido reiniciado.")
            self.nombre = ""
            self.preguntas_contestadas = 0
            self.pregunta_actual = None
            self.cronometro_activo = False
            self.pantalla_inicio()



if __name__ == "__main__":
    root = tk.Tk()
    app = CarreraNumericaApp(root)
    root.mainloop()
