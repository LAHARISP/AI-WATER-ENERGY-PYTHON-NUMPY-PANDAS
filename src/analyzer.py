import numpy as np
import pandas as pd

def analyse_resource(df, resource):
    # Select the requested resource.
    resource_df = df[
        df["resource"] == resource
    ].sort_values("date").copy()

    if len(resource_df) < 7:
        raise ValueError(
            "At least 7 readings are required."
        )

    # Use all observations except the latest one
    # as the historical baseline.
    history = resource_df.iloc[:-1]
    latest = resource_df.iloc[-1]
    historical_usage = history["consumption"].to_numpy(
        dtype=float
    )

    actual_usage = float(latest["consumption"])
    # Calculate historical statistics.
    expected_usage = float(
        np.mean(historical_usage)
    )

    standard_deviation = float(
        np.std(
            historical_usage,
            ddof=1
        )
    )

    minimum_usage = float(
        np.min(historical_usage)
    )
    maximum_usage = float(
        np.max(historical_usage)
    )

    # Calculate percentage deviation.
    if expected_usage > 0:
        percentage_change = (
            (actual_usage - expected_usage)
            / expected_usage
        ) * 100

    else:
        percentage_change = 0.0

    # Statistical threshold:
    # More than 20% above expected usage AND
    # more than 2 historical standard deviations above it.
    threshold = max(
        expected_usage * 1.20,
        expected_usage + 2 * standard_deviation
    )

    anomaly_detected = actual_usage > threshold
    # Calculate recent consumption trend.
    recent_usage = history["consumption"].tail(3)
    recent_average = float(
        recent_usage.mean()
    )

    if recent_average > 0:
        trend_change = (
            (recent_average - expected_usage)
            / expected_usage
        ) * 100

    else:
        trend_change = 0.0
    if trend_change > 5:
        trend = "Increasing"
    elif trend_change < -5:
        trend = "Decreasing"
    else:
        trend = "Stable"

    # Determine severity using percentage change.
    if not anomaly_detected:
        severity = "NORMAL"
    elif percentage_change >= 75:
        severity = "CRITICAL"
    elif percentage_change >= 40:
        severity = "HIGH"
    else:
        severity = "MODERATE"
    # Return structured results.
    return {
        "resource": resource,
        "date": latest["date"].strftime("%Y-%m-%d"),
        "expected_usage": expected_usage,
        "actual_usage": actual_usage,
        "percentage_change": float(percentage_change),
        "standard_deviation": standard_deviation,
        "historical_minimum": minimum_usage,
        "historical_maximum": maximum_usage,
        "anomaly_threshold": threshold,
        "anomaly_detected": bool(anomaly_detected),
        "severity": severity,
        "trend": trend,
        "occupancy": int(latest["occupancy"]),
        "temperature": float(latest["temperature"]),
        "operating_hours": float(latest["operating_hours"])
    }