# Bird Flocking Simulation: Vicsek and Chaté Models

This repository contains a 2D visual simulation of self-propelled particle systems using:

- 🟦 **Vicsek Model (1995)** – angular noise applied after averaging neighbor directions.
- 🔶 **Chaté Variant (2004)** – vectorial noise applied before averaging.

These models are used to study how individual agents (like birds, bacteria or robots) can spontaneously organize into collective motion without a leader.

## 🎥 Visualizations

Simulations of 400–1000 particles moving and aligning in 2D with periodic boundaries under varying noise intensity (η). Lower noise → higher alignment.

| Vicsek | Chaté |
|--------|-------|
| ![](gifs/vicsek_eta=1.5_N=400.gif) | ![](gifs/vicsek_chate_eta=4.5_N=1000.gif) |

## ⚙️ How it works

- `vicsek.py`: basic Vicsek model.
- `chate.py`: extended Chaté version (vectorial noise).

Both scripts generate animated GIFs directly into the `gifs/` folder.

## 📌 Key Parameters

| Parameter      | Value         |
|----------------|---------------|
| Particles \(N\)     | 50–1000       |
| Box size \(L\)       | 10            |
| Speed \(v\)          | 0.03          |
| Interaction radius \(r\) | 1.0      |
| Noise η         | 0.5 – 5.0      |
| Boundaries      | Periodic       |

## ▶️ Run locally

Install requirements:
```bash
pip install numpy matplotlib
