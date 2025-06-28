#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
simulacionvicsek_chaté_gifs.py

Simulación del modelo de Vicsek con variante de Chaté: mide la velocidad
media y genera animaciones en GIF para distintos valores de ruido η,
guardándolas en la carpeta ./gifts con identificación de "chate".
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# ------------------ CONFIGURACIÓN DEL DIRECTORIO ------------------
output_dir = 'gifts'
os.makedirs(output_dir, exist_ok=True)

# ------------------------- PARÁMETROS -------------------------
N = 1000           # número de partículas
L = 10.0          # tamaño del dominio
r = 1.0           # radio de visión
v = 0.03          # velocidad de cada partícula
dt = 1.0          # paso de tiempo
gu_steps_eq = 300    # pasos de equilibrio
gu_steps_meas = 500  # pasos de animación/medida
valores_eta = np.linspace(0.5, 5.0, 5)

# ------------------------- VARIANTE DE CHATÉ -------------------------
def update_step_chate(pos, ang, eta):
    """
    Versión Chaté: aplica ruido a cada vecino antes de promediar.
    """
    new_ang = np.empty_like(ang)
    for i in range(N):
        # distancias periódicas
        d = pos - pos[i]
        d -= L * np.round(d / L)
        dist2 = np.sum(d**2, axis=1)
        neighbors = np.where(dist2 < r**2)[0]
        # ruido antes del promedio
        noisy = ang[neighbors] + (np.random.rand(len(neighbors)) - 0.5) * eta
        sin_sum = np.sum(np.sin(noisy))
        cos_sum = np.sum(np.cos(noisy))
        new_ang[i] = np.arctan2(sin_sum, cos_sum)
    # actualiza ángulos y posiciones
    ang[:] = new_ang
    pos[:, 0] = (pos[:, 0] + v * np.cos(ang) * dt) % L
    pos[:, 1] = (pos[:, 1] + v * np.sin(ang) * dt) % L

# ---------------------- BUCLE PRINCIPAL ----------------------
for eta in valores_eta:
    # inicialización
    pos = np.random.rand(N, 2) * L
    ang = np.random.rand(N) * 2*np.pi - np.pi

    # equilibrio
    for _ in range(gu_steps_eq):
        update_step_chate(pos, ang, eta)

    # prepara figura
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    quiv = ax.quiver(pos[:,0], pos[:,1],
                     np.cos(ang), np.sin(ang),
                     scale=20, width=0.007)
    prev = [ang.copy()]

    def init():
        quiv.set_offsets(pos)
        quiv.set_UVC(np.cos(prev[0]), np.sin(prev[0]))
        return quiv,

    def animate(frame):
        update_step_chate(pos, ang, eta)
        # suavizado visual
        alpha = 0.065
        sm = (1-alpha)*prev[0] + alpha*ang
        prev[0] = sm.copy()
        quiv.set_offsets(pos)
        quiv.set_UVC(np.cos(sm), np.sin(sm))
        return quiv,

    anim = FuncAnimation(fig, animate, init_func=init,
                         frames=gu_steps_meas, interval=50, blit=True)

    # guarda GIF
    fname = f"vicsek_chate_eta={eta:.2f}_N={N}.gif"
    path = os.path.join(output_dir, fname)
    anim.save(path, writer=PillowWriter(fps=20))
    plt.close(fig)
    print(f"GIF guardado: {path}")


