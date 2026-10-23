
def check_protection(
    temperature_c,
    current_a,
    max_temperature_c=45.0,
    max_current_a=1.0,
):
    """Memeriksa parameter simulasi terhadap batas rancangan."""
    warnings = []

    if temperature_c >= max_temperature_c:
        warnings.append("TEMPERATURE_LIMIT_EXCEEDED")

    if current_a > max_current_a:
        warnings.append("CURRENT_LIMIT_EXCEEDED")

    return {
        "protection_status": "WARNING" if warnings else "NORMAL",
        "warnings": warnings,
        "data_source": "SIMULATED",
    }


if __name__ == "__main__":
    result = check_protection(
        temperature_c=48.0,
        current_a=1.2,
    )

    print("=== BATARA PROTECTION TEST ===")
    print(result)
