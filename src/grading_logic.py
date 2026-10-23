
def calculate_capacity(current_readings, interval_seconds):
    """
    Menghitung kapasitas discharge dengan integrasi arus.
    current_readings: daftar arus dalam ampere.
    interval_seconds: interval waktu antar-pembacaan dalam detik.
    Hasil: kapasitas dalam mAh.
    """
    if interval_seconds <= 0:
        raise ValueError("Interval waktu harus lebih dari nol.")

    if len(current_readings) < 2:
        raise ValueError("Minimal diperlukan dua pembacaan arus.")

    if any(current < 0 for current in current_readings):
        raise ValueError("Arus discharge tidak boleh negatif.")

    total_ah = 0.0

    for i in range(len(current_readings) - 1):
        average_current = (
            current_readings[i] + current_readings[i + 1]
        ) / 2

        total_ah += average_current * interval_seconds / 3600

    return round(total_ah * 1000, 2)


def calculate_soh(actual_capacity_mah, nominal_capacity_mah):
    """Menghitung State of Health (SoH) dalam persen."""
    if nominal_capacity_mah <= 0:
        raise ValueError("Kapasitas nominal harus lebih dari nol.")

    if actual_capacity_mah < 0:
        raise ValueError("Kapasitas aktual tidak boleh negatif.")

    return round(
        actual_capacity_mah / nominal_capacity_mah * 100, 2
    )


def determine_grade(soh):
    """
    Kriteria rancangan awal BATARA:
    A: 90-100%
    B: 80-<90%
    C: 60-<80%
    X: <60% atau hasil di luar rentang valid.
    """
    if soh < 0 or soh > 100:
        return "X"

    if soh >= 90:
        return "A"
    elif soh >= 80:
        return "B"
    elif soh >= 60:
        return "C"
    else:
        return "X"


def evaluate_battery(current_readings, interval_seconds,
                     nominal_capacity_mah):
    """Menghitung kapasitas, SoH, dan grade baterai."""
    capacity = calculate_capacity(
        current_readings, interval_seconds
    )

    soh = calculate_soh(capacity, nominal_capacity_mah)

    return {
        "actual_capacity_mah": capacity,
        "nominal_capacity_mah": nominal_capacity_mah,
        "soh_percent": soh,
        "grade": determine_grade(soh),
        "data_source": "SIMULATED",
    }


if __name__ == "__main__":
    # Contoh data simulasi: 10 pembacaan arus.
    currents = [0.5] * 10
    interval = 60
    nominal_capacity = 2500

    result = evaluate_battery(
        currents, interval, nominal_capacity
    )

    print("=== BATARA GRADING TEST ===")
    for key, value in result.items():
        print(f"{key}: {value}")
