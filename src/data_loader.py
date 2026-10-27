from pathlib import Path

import pandas as pd
# Locate the project root regardless of the terminal directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "resource_consumption.csv"
REQUIRED_COLUMNS = [
    "date",
    "resource",
    "consumption",
    "occupancy",
    "temperature",
    "operating_hours"
]
def load_data():

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )
    # Load CSV into a Pandas DataFrame.
    df = pd.read_csv(DATA_PATH)
    # Check required columns.
    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    # Convert columns to appropriate data types.
    df["date"] = pd.to_datetime(
        df["date"],
        errors="raise"
    )

    numeric_columns = [
        "consumption",
        "occupancy",
        "temperature",
        "operating_hours"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="raise"
        )

    # Validate resource names.
    df["resource"] = (
        df["resource"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    valid_resources = {"water", "electricity"}

    if not df["resource"].isin(valid_resources).all():
        raise ValueError(
            "Resource must be water or electricity."
        )

    # Check for missing values.
    if df[REQUIRED_COLUMNS].isnull().any().any():
        raise ValueError(
            "Dataset contains missing values."
        )

    # Check for duplicate dates within a resource.
    if df.duplicated(
        subset=["date", "resource"]
    ).any():
        raise ValueError(
            "Duplicate date/resource records detected."
        )

    # Validate numerical ranges.
    if (df["consumption"] < 0).any():
        raise ValueError(
            "Consumption cannot be negative."
        )

    if (df["occupancy"] < 0).any():
        raise ValueError(
            "Occupancy cannot be negative."
        )

    if (df["operating_hours"] < 0).any():
        raise ValueError(
            "Operating hours cannot be negative."
        )

    if (df["operating_hours"] > 24).any():
        raise ValueError(
            "Daily operating hours cannot exceed 24."
        )

    if not df["temperature"].between(-50, 60).all():
        raise ValueError(
            "Temperature is outside the configured valid range."
        )

    # Sort records by resource and date.
    df = df.sort_values(
        ["resource", "date"]
    ).reset_index(drop=True)

    return df