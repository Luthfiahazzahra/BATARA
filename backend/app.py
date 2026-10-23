
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sensor_simulator import simulate_sensor
from grading_logic import evaluate_battery
from protection_logic import check_protection

st.set_page_config(
    page_title="BATARA Sensor Simulator",
    page_icon="🔋",
    layout="wide",
)

st.title("🔋 BATARA Sensor Simulator")
st.caption(
    "Simulasi software baterai 18650 — "
    "bukan pembacaan sensor fisik."
)

scenario = st.selectbox(
    "Pilih skenario",
    ["normal", "low_capacity", "high_temperature", "high_current"],
)

nominal_capacity = st.number_input(
    "Kapasitas nominal baterai (mAh)",
    min_value=1,
    value=2500,
)

duration_minutes = st.slider(
    "Durasi simulasi discharge (menit)",
    min_value=1,
    max_value=120,
    value=30,
)

current_a = st.slider(
    "Arus discharge simulasi (A)",
    min_value=0.1,
    max_value=2.5,
    value=0.5,
    step=0.1,
)

if st.button("Jalankan Simulasi"):
    interval_seconds = 60
    number_of_readings = duration_minutes + 1

    readings = [
        simulate_sensor(scenario)
        for _ in range(number_of_readings)
    ]

    # Gunakan arus yang sama dengan parameter discharge
    # agar perhitungan kapasitas konsisten.
    currents = [current_a] * number_of_readings

    result = evaluate_battery(
        currents,
        interval_seconds,
        nominal_capacity,
    )

    latest = readings[-1]

    protection = check_protection(
        latest["temperature_c"],
        current_a,
    )

    st.subheader("Hasil pengujian")
    st.caption("Data source: SIMULATED")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tegangan", f'{latest["voltage_v"]} V')
    col2.metric("Arus discharge", f"{current_a:.2f} A")
    col3.metric("Suhu", f'{latest["temperature_c"]} °C')
    col4.metric("Kapasitas", f'{result["actual_capacity_mah"]} mAh')

    st.metric("SoH", f'{result["soh_percent"]}%')
    st.metric("Grade", result["grade"])
    st.metric("Status proteksi", protection["protection_status"])

    if protection["warnings"]:
        for warning in protection["warnings"]:
            st.warning(warning)
    else:
        st.success("Tidak ada batas simulasi yang terlampaui.")

    df = pd.DataFrame(readings)
    df["elapsed_minutes"] = range(len(df))

    st.subheader("Grafik tegangan")
    st.plotly_chart(
        px.line(df, x="elapsed_minutes", y="voltage_v"),
        use_container_width=True,
    )

    st.subheader("Grafik suhu")
    st.plotly_chart(
        px.line(df, x="elapsed_minutes", y="temperature_c"),
        use_container_width=True,
    )

    st.subheader("Data simulasi")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "Unduh data CSV",
        df.to_csv(index=False).encode("utf-8"),
        file_name="batara_simulation.csv",
        mime="text/csv",
    )
