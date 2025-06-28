#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vicsek_measure_and_save_gif.py

Simulación del modelo de Vicsek: mide la velocidad media normalizada v_a
para distintos valores de ruido eta y guarda las animaciones en GIFs
en la carpeta ./gifts dentro del directorio de ejecución.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# ------------------ CONFIGURACIÓN DEL DIRECTORIO ------------------
output_dir = 'gifts'               # carpeta relativa, no '/gifts'
os.makedirs(output_dir, exist_ok=True)

# ------------------------- FUNCIÓN DE ACTUALIZACIÓN -------------------------
def update_step(pos, ang, eta):
    """
    Actualiza posiciones y ángulos según el modelo de Vicsek.
    """
    N = len(ang)
    v = 0.03
    dt = 1.0
    new_ang = np.zeros_like(ang)

    for i in range(N):
        dx = pos[:, 0] - pos[i, 0]
        dy = pos[:, 1] - pos[i, 1]
        dx = (dx + L/2) % L - L/2
        dy = (dy + L/2) % L - L/2
        dist2 = dx**2 + dy**2

        neighbors = dist2 < 1.0**2
        angles = ang[neighbors]
        sin_sum = np.sum(np.sin(angles))
        cos_sum = np.sum(np.cos(angles))
        theta_mean = np.arctan2(sin_sum, cos_sum)

        noise = (np.random.rand() - 0.5) * eta
        new_ang[i] = theta_mean + noise

    ang[:] = new_ang
    pos[:, 0] = (pos[:, 0] + v * np.cos(ang) * dt) % L
    pos[:, 1] = (pos[:, 1] + v * np.sin(ang) * dt) % L

# ---------------------- PARÁMETROS DE LA SIMULACIÓN ----------------------
N = 400
L = 10.0
gu_steps_eq = 300
gu_steps_meas = 500
valores_eta = np.linspace(0.5, 5.0, 5)

# ---------------------- MÉTODO PRINCIPAL ----------------------
for eta in valores_eta:
    pos = np.random.rand(N, 2) * L
    ang = np.random.rand(N) * 2*np.pi - np.pi

    # Calentamiento
    for _ in range(gu_steps_eq):
        update_step(pos, ang, eta)

    # Prepara la figura y la animación
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    quiver = ax.quiver(
        pos[:, 0], pos[:, 1],
        np.cos(ang), np.sin(ang),
        scale=20, width=0.007
    )

    previous_angles = [ang.copy()]

    def init():
        quiver.set_offsets(pos)
        quiver.set_UVC(
            np.cos(previous_angles[0]),
            np.sin(previous_angles[0])
        )
        return quiver,

    def animate(frame):
        update_step(pos, ang, eta)
        alpha = 0.065
        smooth = (1 - alpha) * previous_angles[0] + alpha * ang
        previous_angles[0] = smooth.copy()

        quiver.set_offsets(pos)
        quiver.set_UVC(np.cos(smooth), np.sin(smooth))
        ax.set_title(f"η={eta:.2f}, paso {frame}")
        return quiver,

    anim = FuncAnimation(
        fig, animate,
        init_func=init,
        frames=gu_steps_meas,
        interval=50,
        blit=True
    )

    # Guarda como GIF en ./gifts
    gif_writer = PillowWriter(fps=20)
    filename = f'vicsek_eta={eta:.2f}_N={N}.gif'
    filepath = os.path.join(output_dir, filename)
    anim.save(filepath, writer=gif_writer)
    plt.close(fig)

    print(f"GIF guardado: {filepath}")

