import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Tuple

# =========================
# CONFIGURATION
# =========================

@dataclass
class SimulationConfig:
    duration: int = 160          # minutes
    interval: int = 3            # minutes
    orbit_period: int = 90       # minutes
    offset: float = 15.0
    amplitude: float = 60.0
    noise_std: float = 1.5       # Gaussian noise (realistic)

MIN_VALID_TEMP = -100
MAX_VALID_TEMP = 120


# =========================
# DATA GENERATION
# =========================

def generate_telemetry(config: SimulationConfig) -> List[Dict]:
    """Generate synthetic satellite thermal telemetry."""
    angular_freq = (2 * np.pi) / config.orbit_period
    
    timeline = np.arange(0, config.duration + 1, config.interval)
    
    base_signal = config.offset + config.amplitude * np.sin(angular_freq * timeline)
    noise = np.random.normal(0, config.noise_std, size=len(timeline))
    
    temperatures = np.round(base_signal + noise, 2)

    return [
        {"minute": int(t), "temperature": float(temp)}
        for t, temp in zip(timeline, temperatures)
    ]


# =========================
# PROCESSING
# =========================

def process_telemetry(data: List[Dict]) -> List[Dict]:
    """Validate and classify telemetry data."""
    processed = []

    for point in data:
        temp = point["temperature"]

        if not (MIN_VALID_TEMP <= temp <= MAX_VALID_TEMP):
            print(f"[WARNING] Invalid sensor reading at minute {point['minute']}: {temp}°C")
            continue

        if temp < -40:
            status = "Critical Cold"
        elif temp <= -20:
            status = "Cold"
        elif temp <= 50:
            status = "Nominal"
        elif temp <= 70:
            status = "Hot"
        else:
            status = "Critical Hot"

        point["status"] = status
        processed.append(point)

    return processed


# =========================
# ANALYSIS
# =========================

def detect_extremes(data: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    """Detect local peaks and valleys."""
    peaks, valleys = [], []

    for i in range(1, len(data) - 1):
        prev_t = data[i - 1]["temperature"]
        curr_t = data[i]["temperature"]
        next_t = data[i + 1]["temperature"]

        if curr_t > prev_t and curr_t > next_t:
            peaks.append(data[i])
        elif curr_t < prev_t and curr_t < next_t:
            valleys.append(data[i])

    return peaks, valleys


def compute_statistics(data: List[Dict]) -> Dict:
    temps = [d["temperature"] for d in data]
    return {
        "max": max(temps),
        "min": min(temps),
        "mean": np.mean(temps),
        "std": np.std(temps)
    }


# =========================
# VISUALIZATION (UPGRADED)
# =========================

def plot_dashboard(data: List[Dict], peaks: List[Dict], valleys: List[Dict]):
    """Professional-grade visualization."""
    minutes = [d["minute"] for d in data]
    temps = [d["temperature"] for d in data]

    plt.style.use("seaborn-v0_8-darkgrid")

    fig, ax = plt.subplots(figsize=(14, 7))

    # Main line
    ax.plot(
        minutes,
        temps,
        linewidth=2.2,
        label="Thermal Telemetry",
        alpha=0.9
    )

    # Fill area (adds visual impact)
    ax.fill_between(minutes, temps, alpha=0.15)

    # Peaks and valleys
    ax.scatter(
        [p["minute"] for p in peaks],
        [p["temperature"] for p in peaks],
        marker="^",
        s=90,
        label="Heat Peaks"
    )

    ax.scatter(
        [v["minute"] for v in valleys],
        [v["temperature"] for v in valleys],
        marker="v",
        s=90,
        label="Cooling Valleys"
    )

    # Threshold zones (VERY recruiter-impressive)
    ax.axhspan(50, 70, alpha=0.1, label="Hot Zone")
    ax.axhspan(-20, 50, alpha=0.05, label="Nominal Zone")
    ax.axhspan(-100, -40, alpha=0.1, label="Critical Cold")

    # Labels
    ax.set_title("Satellite Thermal Telemetry Monitoring", fontsize=16, weight="bold")
    ax.set_xlabel("Time (minutes)")
    ax.set_ylabel("Temperature (°C)")

    # Legend
    ax.legend(loc="upper right", frameon=True)

    # Grid tuning
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()


# =========================
# REPORT
# =========================

def print_report(stats: Dict, peaks: List[Dict], valleys: List[Dict]):
    print("\n" + "=" * 40)
    print("        THERMAL ANALYSIS REPORT")
    print("=" * 40)

    print(f"Max Temperature : {stats['max']:.2f}°C")
    print(f"Min Temperature : {stats['min']:.2f}°C")
    print(f"Mean Temperature: {stats['mean']:.2f}°C")
    print(f"Std Deviation   : {stats['std']:.2f}")

    print(f"\nDetected Peaks  : {len(peaks)}")
    print(f"Detected Valleys: {len(valleys)}")

    print("=" * 40)


# =========================
# MAIN PIPELINE
# =========================

def main():
    config = SimulationConfig()

    raw = generate_telemetry(config)
    processed = process_telemetry(raw)
    peaks, valleys = detect_extremes(processed)
    stats = compute_statistics(processed)

    print_report(stats, peaks, valleys)
    plot_dashboard(processed, peaks, valleys)


if __name__ == "__main__":
    main()