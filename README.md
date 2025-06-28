# Bird Flocking Simulation: Vicsek and Chaté Models

<p align="center">
  <img src="gifts/vicsek_eta=0.50_N=400.gif" alt="Vicsek model – eta=0.50" width="400">
</p>

This repository contains a 2D visual simulation of self-propelled particle systems using:

- 🟦 **Vicsek Model (1995)** – angular noise applied *after* averaging neighbor directions.
- 🔶 **Chaté Variant (2004)** – vectorial noise applied *before* averaging.

These models are widely used to understand how individual agents (e.g., birds, bacteria or robots) can organize into coherent motion without any centralized control.

## ⚙️ How It Works

- `vicsek.py`: implements the original Vicsek model.
- `chate.py`: implements the Chaté-Gregoire extension.

Both scripts generate animated GIFs in the `gifts/` directory for different values of noise `η`.

## 📌 Model Parameters

| Parameter        | Value           |
|------------------|-----------------|
| Number of particles \(N\) | 400–1000         |
| Domain size \(L\)          | 10               |
| Speed \(v\)                | 0.03             |
| Vision radius \(r\)        | 1.0              |
| Noise η                   | 0.5 – 5.0         |
| Boundary conditions       | Periodic         |

## ▶️ Running the Simulations

Install required libraries:

```bash
pip install numpy matplotlib

