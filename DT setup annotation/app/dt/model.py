from math import exp
from typing import List, Dict


def q_runoff_m3s(C: float, i_mmhr: float, A_km2: float) -> float:
    """
    Calculate runoff (Q) in cubic meters per second (m³/s).

    Formula:
        Q = 0.278 * C * i * A

    Parameters:
        C (float): Runoff coefficient (dimensionless, between 0 and 1).
        i_mmhr (float): Rainfall intensity (mm/hr).
        A_km2 (float): Catchment area (km²).

    Returns:
        float: Runoff in m³/s.
    """
    return 0.278 * C * i_mmhr * A_km2


def risk_from_loading(L: float, k: float = 8.0) -> float:
    """
    Calculate flood risk using a logistic function.

    Formula:
        R = 1 / (1 + exp(-k * (L - 1)))

    Parameters:
        L (float): Load factor (Q / Qcap).
        k (float): Steepness of the risk curve (default = 8.0).

    Returns:
        float: Risk value between 0 and 1.
    """
    return 1.0 / (1.0 + exp(-k * (L - 1.0)))


def simulate_catchment(
    rain_mmhr: List[float],
    timestamps_utc: List[str],
    C: float,
    A_km2: float,
    Qcap_m3s: float,
) -> Dict:
    """
    Simulate runoff and flood risk for a time series of rainfall.

    Parameters:
        rain_mmhr (List[float]): List of rainfall intensities (mm/hr).
        timestamps_utc (List[str]): List of timestamps (ISO 8601 format).
        C (float): Runoff coefficient.
        A_km2 (float): Catchment area (km²).
        Qcap_m3s (float): Drainage system capacity (m³/s).

    Returns:
        Dict: {
            "series": list of results per timestamp,
            "max_risk": highest risk across the series
        }
    """
    series = []
    max_r = 0.0

    # Loop through rainfall data with timestamps
    for i, t in zip(rain_mmhr, timestamps_utc):
        # Step 1: Calculate runoff
        Q = q_runoff_m3s(C, i, A_km2)

        # Step 2: Calculate load factor (relative to capacity)
        L = Q / Qcap_m3s if Qcap_m3s > 0 else 1e6  # avoid division by zero

        # Step 3: Calculate risk from load factor
        R = risk_from_loading(L)

        # Step 4: Track maximum risk across simulation
        max_r = max(max_r, R)

        # Step 5: Append results to series
        series.append({
            "t": t,
            "i": i,
            "Qrunoff": round(Q, 3),
            "L": round(L, 3),
            "R": round(R, 3)
        })

    return {"series": series, "max_risk": round(max_r, 3)}


if __name__ == "__main__":
    # ========== Example 1: Single calculation ==========
    C = 0.6          # Runoff coefficient
    i_mmhr = 8       # Rainfall intensity (mm/hr)
    A_km2 = 10       # Catchment area (km²)
    Qcap_m3s = 100   # Capacity (m³/s)

    # Runoff calculation
    Q = q_runoff_m3s(C, i_mmhr, A_km2)

    # Load factor (Q relative to capacity)
    L = Q / Qcap_m3s

    # Risk value
    R = risk_from_loading(L)

    print("Runoff Q:", Q, "m³/s")
    print("Load L:", L)
    print("Risk R:", R)

    # ========== Example 2: Simulation over multiple hours ==========
    results = simulate_catchment(
        rain_mmhr=[5, 10, 20],   # Rainfall intensities
        timestamps_utc=["2025-09-22T00:00Z", "2025-09-22T01:00Z", "2025-09-22T02:00Z"],
        C=0.6,
        A_km2=10,
        Qcap_m3s=15
    )

    print("Simulation Results:")
    print(results)

