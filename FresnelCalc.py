import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

import Fresnel  # Asegúrate de que las funciones de Fresnel estén correctamente importadas

root = tk.Tk()
root.title("Fresnel Calculator")

# Crear un contenedor para las etiquetas y campos de entrada
frame_params = tk.Frame(root)
frame_params.pack(pady=10)

# Crear la etiqueta y el campo de entrada para nInc
label_nInc = tk.Label(frame_params, text="Índice de refracción incidente (nInc):")
label_nInc.grid(row=0, column=0, padx=5)
entry_nInc = tk.Entry(frame_params)
entry_nInc.grid(row=0, column=1, padx=5)
entry_nInc.insert(0, "1")  # Valor por defecto

# Crear la etiqueta y los campos de entrada para nSub (refracción compleja)
label_nSub = tk.Label(frame_params, text="Índice de refracción sustrato (nSub) [Re, Im]:")
label_nSub.grid(row=1, column=0, padx=5)
entry_nSub_Re = tk.Entry(frame_params)
entry_nSub_Re.grid(row=1, column=1, padx=5)
entry_nSub_Re.insert(0, "1.5")  # Valor por defecto

plus_label = tk.Label(frame_params, text="+")

plus_label.grid(row=1, column=2, padx=5)
entry_nSub_Im = tk.Entry(frame_params)
entry_nSub_Im.grid(row=1, column=3, padx=5)
entry_nSub_Im.insert(0, "0.01")  # Valor por defecto

# Crear una etiqueta para el desplegable de operaciones
label_operation = tk.Label(root, text="Seleccione la operación:")
label_operation.pack(pady=10)

# Operaciones disponibles
operations = [
    "reflected irradiance",
    "reflected diattenuation",
    "reflected retardance",
    "reflected amplitude - Abs",
    "reflected amplitude - Phase",
    "reflected amplitude - Real",
    "reflected amplitude - Imag",
    "transmitted irradiance",
    "transmitted diattenuation",
    "transmitted retardance",
    "transmitted amplitude - Abs",
    "transmitted amplitude - Phase",
    "transmitted amplitude - Real",
    "transmitted amplitude - Imag"
]

# Crear desplegable
combobox_operation = ttk.Combobox(root, values=operations, state="readonly")
combobox_operation.pack(pady=10)
combobox_operation.current(0)  # Seleccionar la primera opción por defecto


# Variable para almacenar el canvas actual
current_canvas = None

# Función para actualizar el gráfico basado en la operación seleccionada
def update_graph():

    global current_canvas  # Usar la variable global para el canvas actual

        # Si ya existe un canvas, eliminarlo
    if current_canvas:
        current_canvas.get_tk_widget().destroy()


    operation = combobox_operation.get()
    nInc = float(entry_nInc.get())  # Índice de refracción incidente
    nSub_Re = float(entry_nSub_Re.get())  # Parte real índice de refracción sustrato
    nSub_Im = float(entry_nSub_Im.get())  # Parte imaginaria índice de refracción sustrato
    nSub = complex(nSub_Re, nSub_Im)  # Índice de refracción sustrato

    # Crear una figura de Matplotlib
    fig, ax = plt.subplots(figsize=(6, 4))

    # Rango de ángulos para graficar
    angles = np.linspace(0, np.pi/2, 100)  # Ángulos de 0 a 90 grados

    # Dependiendo de la operación seleccionada, calculamos y graficamos
    if operation == "reflected irradiance":
        reflected = [Fresnel.Rs(nInc, nSub, angle) for angle in angles]
        ax.plot(angles, reflected, label="Reflected Irradiance", color='blue')

    elif operation == "transmitted irradiance":
        transmitted = [Fresnel.Ts(nInc, nSub, angle) for angle in angles]
        ax.plot(angles, transmitted, label="Transmitted Irradiance", color='red')

    elif operation == "reflected diattenuation":
        reflected_Diattenuation = [Fresnel.Diattenuation(Fresnel.Rs(nInc, nSub, angle), Fresnel.Rp(nInc, nSub, angle)) for angle in angles]
        ax.plot(angles, reflected_Diattenuation, label="Reflected Diattenuation", color='green')

    elif operation == "transmitted diattenuation":
        transmitted_Diattenuation = [Fresnel.Diattenuation(Fresnel.Ts(nInc, nSub, angle), Fresnel.Tp(nInc, nSub, angle)) for angle in angles]
        ax.plot(angles, transmitted_Diattenuation, label="Transmitted Diattenuation", color='purple')

    elif operation == "reflected retardance":
        reflected_Retardance = [Fresnel.Retardance(Fresnel.rs(nInc, nSub, angle), Fresnel.rp(nInc, nSub, angle)) for angle in angles]
        ax.plot(angles, reflected_Retardance, label="Reflected Retardance", color='orange')

    elif operation == "transmitted retardance":
        transmitted_Retardance = [Fresnel.Retardance(Fresnel.ts(nInc, nSub, angle), Fresnel.tp(nInc, nSub, angle)) for angle in angles]
        ax.plot(angles, transmitted_Retardance, label="Transmitted Retardance", color='brown')

    elif operation == "reflected amplitude - Abs":
        reflected_Amplitude_Abs = [abs(Fresnel.rs(nInc, nSub, angle)) for angle in angles]
        ax.plot(angles, reflected_Amplitude_Abs, label="Reflected Amplitude - Abs", color='cyan')

    elif operation == "transmitted amplitude - Abs":
        transmitted_Amplitude_Abs = [abs(Fresnel.ts(nInc, nSub, angle)) for angle in angles]
        ax.plot(angles, transmitted_Amplitude_Abs, label="Transmitted Amplitude - Abs", color='magenta')

    elif operation == "reflected amplitude - Phase":
        reflected_Amplitude_Phase = [np.angle(Fresnel.rs(nInc, nSub, angle)) for angle in angles]
        ax.plot(angles, reflected_Amplitude_Phase, label="Reflected Amplitude - Phase", color='yellow')

    elif operation == "transmitted amplitude - Phase":
        transmitted_Amplitude_Phase = [np.angle(Fresnel.ts(nInc, nSub, angle)) for angle in angles]
        ax.plot(angles, transmitted_Amplitude_Phase, label="Transmitted Amplitude - Phase", color='gray')

    elif operation == "reflected amplitude - Real":
        reflected_Amplitude_Real = [Fresnel.rs(nInc, nSub, angle).real for angle in angles]
        ax.plot(angles, reflected_Amplitude_Real, label="Reflected Amplitude - Real", color='pink')

    elif operation == "transmitted amplitude - Real":
        transmitted_Amplitude_Real = [Fresnel.ts(nInc, nSub, angle).real for angle in angles]
        ax.plot(angles, transmitted_Amplitude_Real, label="Transmitted Amplitude - Real", color='lime')

    elif operation == "reflected amplitude - Imag":
        reflected_Amplitude_Imag = [Fresnel.rs(nInc, nSub, angle).imag for angle in angles]
        ax.plot(angles, reflected_Amplitude_Imag, label="Reflected Amplitude - Imag", color='violet')

    elif operation == "transmitted amplitude - Imag":
        transmitted_Amplitude_Imag = [Fresnel.ts(nInc, nSub, angle).imag for angle in angles]
        ax.plot(angles, transmitted_Amplitude_Imag, label="Transmitted Amplitude - Imag", color='teal')

    # Configurar etiquetas y leyenda
    ax.set_xlabel('Ángulo de incidencia (radianes)')
    ax.set_ylabel('Valor')
    ax.set_title(f'{operation.capitalize()} vs Incident Angle')
    ax.legend()

    # Mostrar la gráfica en el GUI
    current_canvas = FigureCanvasTkAgg(fig, master=root)
    current_canvas.get_tk_widget().pack(pady=20)
    current_canvas.draw()

        # Conectar el evento de movimiento del mouse
    current_canvas.mpl_connect("motion_notify_event", on_mouse_move)

# Función que se ejecuta al mover el mouse sobre el gráfico
def on_mouse_move(event):
    if event.inaxes:  # Verifica si el mouse está dentro del área del gráfico
        x, y = event.xdata, event.ydata
        # Actualiza las coordenadas en la etiqueta
        label_coords.config(text=f"Coordenadas: ({x:.2f}, {y:.2f})")
        # Mueve la etiqueta de coordenadas junto al puntero
        label_coords.place(x=event.x + 10, y=event.y + 10)  # Mueve la etiqueta cerca del puntero

# Crear una etiqueta para mostrar las coordenadas del mouse
label_coords = tk.Label(root, text="(0.00, 0.00)", font=("Helvetica", 8), bg="white")
label_coords.pack_forget()  # Inicialmente, no mostrar

# Crear un botón para confirmar la selección y actualizar el gráfico
boton_confirmar = tk.Button(root, text="Confirmar", command=update_graph)
boton_confirmar.pack(pady=10)



# Función para cerrar correctamente el script al cerrar la ventana
def on_close():
    root.quit()  # Detiene el bucle de eventos
# Asocia la función de cierre a la ventana
root.protocol("WM_DELETE_WINDOW", on_close)

# Ejecutar la ventana principal
root.mainloop()
