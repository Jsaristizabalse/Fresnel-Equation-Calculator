import tkinter as tk
from tkinter import messagebox

# Función que se ejecuta cuando se presiona el botón
def mostrar_mensaje():
    messagebox.showinfo("Mensaje", "¡Hola, este es un mensaje!")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Ejemplo Básico de Tkinter")
ventana.geometry("300x200")  # Tamaño de la ventana

# Crear un botón y agregarlo a la ventana
boton = tk.Button(ventana, text="Mostrar Mensaje", command=mostrar_mensaje)
boton.pack(pady=20)  # Añadir el botón con un margen vertical

# Ejecutar el bucle principal de la ventana
ventana.mainloop()
