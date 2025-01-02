
# N-Body Simulation in Python

This project is a Python-based N-body simulation that models the interactions of particles under gravitational forces. The simulation implements two numerical integration methods for comparison: the **Euler Method** and the **Runge-Kutta Order 4 (RK4)**. These methods allow for an exploration of the accuracy and performance differences in solving such dynamic systems.

## Features

- Simulates gravitational interactions between multiple bodies.
- Supports two numerical integration methods:
  - Euler Method (simple but less accurate).
  - Runge-Kutta Order 4 (more accurate and widely used).
- Visualizes the trajectories of the bodies.
- Plots energy conservation and system dynamics.

## Prerequisites

To run this project, you need:
- Python 3.7 or higher.
- The following Python libraries:
  - `matplotlib`
  - `numpy`

You can install the required libraries using pip:
```bash
pip install matplotlib numpy
```

## Getting Started

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd nbody-simulation
   ```

2. **Run the Main Program:**
   The main program generates simulation data for the N-body system using the chosen integration method.
   ```bash
   python main.py
   ```

3. **Visualize the Simulation:**
   Choose one of the following visualization tools:
   - **Pos Plotter:** Allows you to control the simulation time with an interactive slider.
     ```bash
     python pos_plotter.py
     ```
   - **Plotter:** Plots trajectories, energies, and other system metrics without interactivity.
     ```bash
     python plotter.py
     ```

## Usage

- **Choosing the Integration Method:** The default method can be set in `main.py`. Edit the relevant section to select either the Euler method or the RK4 method.
- **Customizing the Simulation:** Modify the initial conditions, number of bodies, and simulation parameters in `main.py` to suit your needs.

## Output

- **Pos Plotter:** Displays a dynamic plot where users can adjust the time slider to observe the bodies' positions over time.
- **Plotter:** Provides detailed graphs of:
  - Trajectories of all bodies.
  - Conservation of energy and momentum.

## Project Overview

This project demonstrates the differences between the Euler and RK4 methods in an N-body simulation. While the Euler method offers simplicity, the RK4 method provides superior accuracy, particularly in conserving physical quantities such as energy. The visualizations highlight these differences and offer insight into the behavior of dynamic systems.

## License

This project is released under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

This simulation was developed to explore numerical integration techniques and their application in physics-based simulations.
