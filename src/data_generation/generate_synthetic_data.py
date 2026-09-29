from pathlib import Path
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


random.seed(42)
np.random.seed(42)

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def random_date():
    start_date = datetime(2020, 1, 1)
    random_days = random.randint(0, 1500)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")


def create_customers(count=500):
    countries = ["USA", "US", "United States", "Canada", "CA", "India", "IN"]
    records = []

    for i in range(1, count + 1):
        customer_id = f"CUST{i:05d}"

        records.append(
            {
                "CUSTOMER_ID": customer_id,
                "CUSTOMER_NAME": f"Customer {i}",
                "COUNTRY": random.choice(countries),
                "POSTAL_CODE": str(random.randint(10000, 99999)),
                "EMAIL": f"customer{i}@example.com",
                "CREATED_DATE": random_date(),
            }
        )

    df = pd.DataFrame(records)

    # Add realistic data-quality problems
    df.loc[5, "CUSTOMER_ID"] = None
    df.loc[10, "EMAIL"] = "invalid-email"
    df.loc[15, "POSTAL_CODE"] = None
    df.loc[20, "CUSTOMER_NAME"] = "  Customer 20  "
    df.loc[25, "CREATED_DATE"] = "03/25/2024"

    # Duplicate records
    df = pd.concat([df, df.iloc[[30, 31]]], ignore_index=True)

    return df


def create_vendors(count=500):
    countries = ["USA", "US", "United States", "Germany", "DE", "India", "IN"]
    records = []

    for i in range(1, count + 1):
        vendor_id = f"VEND{i:05d}"

        records.append(
            {
                "VENDOR_ID": vendor_id,
                "VENDOR_NAME": f"Vendor {i}",
                "COUNTRY": random.choice(countries),
                "POSTAL_CODE": str(random.randint(10000, 99999)),
                "EMAIL": f"vendor{i}@example.com",
                "PAYMENT_TERMS": random.choice(["NET30", "NET45", "NET60"]),
                "CREATED_DATE": random_date(),
            }
        )

    df = pd.DataFrame(records)

    # Add realistic data-quality problems
    df.loc[8, "VENDOR_ID"] = None
    df.loc[12, "EMAIL"] = "vendor-invalid"
    df.loc[18, "POSTAL_CODE"] = None
    df.loc[22, "PAYMENT_TERMS"] = None
    df.loc[28, "VENDOR_NAME"] = " Vendor 28 "
    df.loc[35, "CREATED_DATE"] = "2024/04/15"

    # Duplicate records
    df = pd.concat([df, df.iloc[[40, 41]]], ignore_index=True)

    return df


if __name__ == "__main__":
    customers = create_customers()
    vendors = create_vendors()

    customers.to_csv(OUTPUT_DIR / "customers_source.csv", index=False)
    vendors.to_csv(OUTPUT_DIR / "vendors_source.csv", index=False)

    print(f"Created {len(customers)} customer records.")
    print(f"Created {len(vendors)} vendor records.")
    print(f"Files saved to: {OUTPUT_DIR}")