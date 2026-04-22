# Satellite Thermal Telemetry Monitor (STTM)

![Python](https://img.shields.io/badge/python-3.10+-blue.svg) ![NumPy](https://img.shields.io/badge/library-NumPy-blueviolet.svg) ![Matplotlib](https://img.shields.io/badge/library-Matplotlib-orange.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg)

A high-fidelity simulation engine and analytical dashboard designed to monitor satellite thermal health in Low Earth Orbit (LEO). This project bridges the gap between raw aerospace telemetry and actionable engineering insights by modeling complex orbital temperature fluctuations and detecting critical hardware anomalies.

##  Overview:

In the harsh environment of space, satellites cycle between extreme solar radiation and the deep cold of Earth's shadow. The **Satellite Thermal Telemetry Monitor (STTM)** simulates these cycles using sinusoidal modeling combined with stochastic Gaussian noise to replicate real-world sensor behavior. 

Beyond simple simulation, STTM implements a rigorous data pipeline—validating sensor integrity, classifying thermal states, and identifying extreme peaks and valleys to ensure mission-critical hardware remains within its operational design limits.

---

##  Key Features:

* **Deterministic Simulation**: Uses angular frequency calculations to model orbital periods ($2\pi/P$) with high precision.
* **Stochastic Noise Modeling**: Implements `numpy.random.normal` to simulate Gaussian sensor jitter, providing a more realistic dataset than standard uniform distributions.
* **Data Integrity Layer**: Automated validation logic to detect and filter "impossible" sensor readings.
* **Multi-State Classification**: Categorizes data into five distinct thermal zones (Critical Cold, Cold, Nominal, Hot, and Critical Hot).
* **Signal Processing**: Algorithmically identifies local maxima (peaks) and minima (valleys) to pinpoint moments of maximum thermal stress.
* **Professional Visualization**: A comprehensive dashboard featuring shaded threshold zones and clear trend indicators.

---

##  Architecture & Pipeline:

The project follows a clean, modular pipeline architecture:

1.  **Data Generation**: The `SimulationConfig` dataclass feeds parameters into a generator that creates a timeline based on orbital mechanics.
2.  **Data Processing**: A validation gate checks every data point against physics-based constraints. Valid data is then tagged with an operational status.
3.  **Analysis**: The engine computes descriptive statistics (Mean, Std Dev) and scans the signal for directional changes to identify extremes.
4.  **Visualization**: Data is rendered into a styled Matplotlib dashboard, providing immediate situational awareness.

---

##  Code Structure:

| Function | Responsibility |
| :--- | :--- |
| `generate_telemetry` | Mathematical modeling of the orbital environment using NumPy vectorization. |
| `process_telemetry` | Data cleaning, range validation, and state classification logic. |
| `detect_extremes` | Signal processing to find local peaks and valleys. |
| `compute_statistics` | Statistical reduction (Average, Standard Deviation, Max/Min). |
| `plot_dashboard` | Professional-grade rendering using customized Matplotlib styles. |

---

##  Installation & Usage

### Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/satellite-thermal-monitor.git](https://github.com/yourusername/satellite-thermal-monitor.git)
   cd satellite-thermal-monitor

##  Install dependencies:
Bash
pip install numpy matplotlib
##  Run the system:
Bash
python main.py

## Atuhor 
Lucas Teixeira - Data Science & Machine Learning Student.
