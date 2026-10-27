def investigate_cause(result):
    resource = result["resource"]
    change = result["percentage_change"]
    causes = []
    recommendations = []
    # Investigate electricity consumption.
    if resource == "electricity":
        if result["operating_hours"] > 12:
            causes.append(
                "Recorded equipment operating hours are high."
            )
            recommendations.append(
                "Review equipment schedules and verify "
                "whether the extended operating time was necessary."
            )
        if result["temperature"] >= 30:
            causes.append(
                "High ambient temperature may have increased "
                "cooling demand."
            )
            recommendations.append(
                "Compare consumption with weather and "
                "air-conditioning operating records."
            )
        causes.append(
            "Increased appliance usage or equipment malfunction "
            "is another possibility."
        )
        recommendations.append(
            "Inspect high-consumption equipment and review "
            "equipment-level measurements if available."
        )
    # Investigate water consumption.
    elif resource == "water":
        causes.append(
            "A leak or unusually high water usage may explain "
            "the increase."
        )

        recommendations.append(
            "Inspect plumbing, taps, toilets, and water meters."
        )

        recommendations.append(
            "Check whether water was used for cleaning, "
            "maintenance, or other unusual activities."
        )

    # Compare occupancy against the previous day's reading
    # only when the actual data supports the comparison.
    # The main application will provide this additional context.
    if not result["anomaly_detected"]:
        causes = [
            "The reading does not exceed the configured "
            "statistical anomaly threshold."
        ]
        recommendations = [
            "Continue monitoring and investigate if unusual "
            "readings persist."
        ]
    # Return the investigation.
    return {
        "possible_causes": causes,
        "recommendations": recommendations,
        "confidence": (
            "Low — aggregate consumption data alone cannot "
            "confirm the actual cause."
        )
    }