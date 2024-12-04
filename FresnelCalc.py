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
    global current_canvas  # Declarar la variable global para usarla

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
        # Calcular Rs (onda s) y Rp (onda p)
        reflected_s = [Fresnel.Rs(nInc, nSub, angle) for angle in angles]
        reflected_p = [Fresnel.Rp(nInc, nSub, angle) for angle in angles]

        # Graficar las ondas s y p
        ax.plot(angles, reflected_s, label="Reflected Irradiance (s)", color='blue')
        ax.plot(angles, reflected_p, label="Reflected Irradiance (p)", color='red')

    elif operation == "transmitted irradiance":
        transmitted_s = [Fresnel.Ts(nInc, nSub, angle) for angle in angles]
        transmitted_p = [Fresnel.Tp(nInc, nSub, angle) for angle in angles]
        ax.plot(angles, transmitted_s, label="Transmitted Irradiance (s)", color='blue')
        ax.plot(angles, transmitted_p, label="Transmitted Irradiance (p)", color='red')

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
        transmitted_Retardance_s = [Fresnel.Retardance(Fresnel.ts(nInc, nSub, angle), Fresnel.tp(nInc, nSub, angle)) for angle in angles]
        transmitted_Retardance_p = [Fresnel.Retardance(Fresnel.tp(nInc, nSub, angle), Fresnel.tp(nInc, nSub, angle)) for angle in angles]
        ax.plot(angles, transmitted_Retardance_s, label="Transmitted Retardance (s)", color='blue')
        ax.plot(angles, transmitted_Retardance_p, label="Transmitted Retardance (p)", color='red')

    elif operation == "reflected amplitude - Abs":
        reflected_Amplitude_Abs_s = [abs(Fresnel.rs(nInc, nSub, angle)) for angle in angles]  # Onda s
        reflected_Amplitude_Abs_p = [abs(Fresnel.rp(nInc, nSub, angle)) for angle in angles]  # Onda p
        ax.plot(angles, reflected_Amplitude_Abs_s, label="Reflected Amplitude - Abs (s)", color='blue')
        ax.plot(angles, reflected_Amplitude_Abs_p, label="Reflected Amplitude - Abs (p)", color='red')


    elif operation == "transmitted amplitude - Abs":
        transmitted_Amplitude_Abs_s = [abs(Fresnel.ts(nInc, nSub, angle)) for angle in angles]
        transmitted_Amplitude_Abs_p = [abs(Fresnel.tp(nInc, nSub, angle)) for angle in angles]
        ax.plot(angles, transmitted_Amplitude_Abs_s, label="Transmitted Amplitude (s) - Abs", color='blue')
        ax.plot(angles, transmitted_Amplitude_Abs_p, label="Transmitted Amplitude (p) - Abs", color='red')

    elif operation == "reflected amplitude - Phase":
        reflected_Amplitude_Phase_s = [np.angle(Fresnel.rs(nInc, nSub, angle)) for angle in angles]
        reflected_Amplitude_Phase_p = [np.angle(Fresnel.rp(nInc, nSub, angle)) for angle in angles]
        ax.plot(angles, reflected_Amplitude_Phase_s, label="Reflected Amplitude (s) - Phase", color='blue')
        ax.plot(angles, reflected_Amplitude_Phase_p, label="Reflected Amplitude (p) - Phase", color='red')

    elif operation == "transmitted amplitude - Phase":
        transmitted_Amplitude_Phase_s = [np.angle(Fresnel.ts(nInc, nSub, angle)) for angle in angles]
        transmitted_Amplitude_Phase_p = [np.angle(Fresnel.tp(nInc, nSub, angle)) for angle in angles]
        ax.plot(angles, transmitted_Amplitude_Phase_s, label="Transmitted Amplitude (s) - Phase", color='blue')
        ax.plot(angles, transmitted_Amplitude_Phase_p, label="Transmitted Amplitude (p) - Phase", color='red')

    elif operation == "reflected amplitude - Real":
        reflected_Amplitude_Real_s = [Fresnel.rs(nInc, nSub, angle).real for angle in angles]
        reflected_Amplitude_Real_p = [Fresnel.rp(nInc, nSub, angle).real for angle in angles]
        ax.plot(angles, reflected_Amplitude_Real_s, label="Reflected Amplitude (s) - Real", color='blue')
        ax.plot(angles, reflected_Amplitude_Real_p, label="Reflected Amplitude (p) - Real", color='red')

    elif operation == "transmitted amplitude - Real":
        transmitted_Amplitude_Real_s = [Fresnel.ts(nInc, nSub, angle).real for angle in angles]
        transmitted_Amplitude_Real_p = [Fresnel.tp(nInc, nSub, angle).real for angle in angles]
        ax.plot(angles, transmitted_Amplitude_Real_s, label="Transmitted Amplitude (s) - Real", color='blue')
        ax.plot(angles, transmitted_Amplitude_Real_p, label="Transmitted Amplitude (p) - Real", color='red')

    elif operation == "reflected amplitude - Imag":
        reflected_Amplitude_Imag_s = [Fresnel.rs(nInc, nSub, angle).imag for angle in angles]
        reflected_Amplitude_Imag_p = [Fresnel.rp(nInc, nSub, angle).imag for angle in angles]
        ax.plot(angles, reflected_Amplitude_Imag_s, label="Reflected Amplitude (s) - Imag", color='blue')
        ax.plot(angles, reflected_Amplitude_Imag_p, label="Reflected Amplitude (p) - Imag", color='red')

    elif operation == "transmitted amplitude - Imag":
        transmitted_Amplitude_Imag_s = [Fresnel.ts(nInc, nSub, angle).imag for angle in angles]
        transmitted_Amplitude_Imag_p = [Fresnel.tp(nInc, nSub, angle).imag for angle in angles]
        ax.plot(angles, transmitted_Amplitude_Imag_s, label="Transmitted Amplitude (s) - Imag", color='blue')
        ax.plot(angles, transmitted_Amplitude_Imag_p, label="Transmitted Amplitude (p) - Imag", color='red')

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
    current_canvas.mpl_connect("figure_leave_event", on_mouse_leave)

# Función que se ejecuta al mover el mouse sobre el gráfico
def on_mouse_move(event):
    if event.inaxes:  # Verifica si el mouse está dentro del área del gráfico
        x, y = event.xdata, event.ydata
        # Actualiza las coordenadas en la etiqueta
        label_coords.config(text=f"Coordenadas: ({x:.2f}, {y:.2f})")
        # Mueve la etiqueta cerca del puntero
        label_coords.place(x=event.x + 10, y=root.winfo_height() - event.y + 10)  # Invertir solo el valor de y
        label_coords.lift()  # Mover la etiqueta al frente

# Función que oculta el label cuando el mouse sale del gráfico
def on_mouse_leave(event):
    label_coords.place_forget()  # Oculta el label cuando el mouse sale

# Crear una etiqueta para mostrar las coordenadas del mouse
label_coords = tk.Label(root, text="(0.00, 0.00)", font=("Helvetica", 8), bg="white", relief="solid", padx=5, pady=5)
label_coords.place_forget()  # Inicialmente, no mostrar

# Botón para actualizar el gráfico
button_update = tk.Button(root, text="Actualizar Gráfico", command=update_graph)
button_update.pack(pady=10)

# Función para cerrar correctamente el script al cerrar la ventana
def on_close():
    root.quit()  # Detiene el bucle de eventos

# Asocia la función de cierre a la ventana
root.protocol("WM_DELETE_WINDOW", on_close)

# Ejecutar la interfaz gráfica
root.mainloop()
