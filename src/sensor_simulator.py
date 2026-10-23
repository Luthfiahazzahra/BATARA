
import json
import random
import time
from datetime import datetime, timezone, timedelta

WIB = timezone(timedelta(hours=7))


def simulate_sensor(condition="normal"):
    """Menghasilkan data sensor simulasi baterai 18650."""

    scenarios = {
        "normal": {
            "voltage": (3.4, 4.1),
            "current": (0.3, 0.8),
            "temperature": (25.0, 35.0),
        },
        "low_capacity": {
            "voltage": (3.0, 3.7),
            "current": (0.3, 0.8),
            "temperature": (25.0, 38.0),
        },
        "high_temperature": {
            "voltage": (3.2, 3.9),
            "current": (0.3, 0.8),
            "temperature": (46.0, 55.0),
        },
        "high_current": {
            "voltage": (3.0, 4.0),
            "current": (1.5, 2.5),
            "temperature": (30.0, 45.0),
        },
    }

    if condition not in scenarios:
        raise ValueError("Skenario tidak dikenal.")

    scenario = scenarios[condition]

    voltage = round(random.uniform(*scenario["voltage"]), 3)
    current = round(random.uniform(*scenario["current"]), 3)
    temperature = round(
        random.uniform(*scenario["temperature"]), 2
    )

    return {
        "device_id": "BATARA-18650-001",
        "timestamp": datetime.now(WIB).isoformat(
            timespec="seconds"
        ),
        "condition": condition,
        "voltage_v": voltage,
        "current_a": current,
        "power_w": round(voltage * current, 3),
        "temperature_c": temperature,
        "data_source": "SIMULATED",
    }


def main():
    print("=== BATARA SENSOR SIMULATOR ===")
    print("Data ini merupakan SIMULASI, bukan hasil sensor asli.")

    scenarios = {
        "1": "normal",
        "2": "low_capacity",
        "3": "high_temperature",
        "4": "high_current",
    }

    while True:
        print("\nPilih skenario:")
        print("1. Kondisi normal")
        print("2. Simulasi kapasitas rendah")
        print("3. Simulasi suhu tinggi")
        print("4. Simulasi arus tinggi")
        print("0. Keluar")

        choice = input("Pilihan: ").strip()

        if choice == "0":
            print("Simulator dihentikan.")
            break

        if choice not in scenarios:
            print("Pilihan tidak valid.")
            continue

        data = simulate_sensor(scenarios[choice])
        print(json.dumps(data, indent=2, ensure_ascii=False))
        time.sleep(0.2)


if __name__ == "__main__":
    main()
