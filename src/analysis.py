"""
Day 1 - API Data Analysis Using Python Structures
Squad Python Specialization - Data Science, AI & Analytics
Author: Junior Data Analyst
"""
from pathlib import Path
from typing import Any
import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_DIR = Path("output")


# --- Task 1: Retrieve customer data ---
def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Error fetching customers: {error}")
        return []


# --- Task 2: Explore nested dictionaries and lists ---
def explore(record: Any, indent: int = 0) -> None:
    """
    Recursively walk a dictionary or list and print every key/item
    with its Python data type, indented by depth.
    """
    indent_space = "  " * indent
    if isinstance(record, dict):
        for key, value in record.items():
            print(f"{indent_space}- {key}: {type(value).__name__}")
            if isinstance(value, (dict, list)):
                explore(value, indent + 1)
    elif isinstance(record, list):
        for index, item in enumerate(record):
            print(f"{indent_space}- [{index}]: {type(item).__name__}")
            if isinstance(item, (dict, list)):
                explore(item, indent + 1)


# --- Task 3: Extract customer attributes ---
def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dict per customer with the attributes listed in the task."""
    flattened_customers = []

    for cust in customers:
        email = cust.get("email", "")
        email_domain = email.split("@")[1] if "@" in email else ""

        address = cust.get("address", {})
        geo = address.get("geo", {})
        company = cust.get("company", {})

        row = {
            "id": cust.get("id"),
            "name": cust.get("name"),
            "username": cust.get("username"),
            "email": email,
            "email_domain": email_domain,
            "phone": cust.get("phone"),
            "city": address.get("city"),
            "zipcode": address.get("zipcode"),
            "latitude": float(geo.get("lat", 0.0)),
            "longitude": float(geo.get("lng", 0.0)),
            "company": company.get("name", ""),
            "website": cust.get("website"),
        }
        flattened_customers.append(row)

    return flattened_customers


# --- Task 4: Unique cities ---
def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    return {c["city"] for c in customers if c.get("city")}


# --- Task 5a: Count customers per city ---
def city_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per city using a loop and/or a dict comprehension (no Counter, no pandas)."""
    counts: dict[str, int] = {}
    for cust in customers:
        city = cust.get("city")
        if city:
            counts[city] = counts.get(city, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))


# --- Task 5b: Count customers per email TLD ---
def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per email top-level domain (e.g. 'biz', 'tv')."""
    tlds = [
        c["email_domain"].split(".")[-1]
        for c in customers
        if c.get("email_domain") and "." in c["email_domain"]
    ]
    counts = {tld: tlds.count(tld) for tld in set(tlds)}
    return dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))


# --- Task 6: Convert to DataFrame ---
def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    """Convert the flattened customer dictionary rows into a pandas DataFrame."""
    return pd.DataFrame(rows)


# --- Task 7: Export datasets to CSV ---
def export_csv(
    df_customers: pd.DataFrame,
    df_city_counts: pd.DataFrame,
    out_dir: Path = OUTPUT_DIR,
) -> None:
    """Save both processed datasets to the output directory."""
    out_dir.mkdir(parents=True, exist_ok=True)
    customers_path = out_dir / "customers.csv"
    city_counts_path = out_dir / "city_counts.csv"

    df_customers.to_csv(customers_path, index=False)
    df_city_counts.to_csv(city_counts_path, index=False)
    print(f"[+] Exported: {customers_path}")
    print(f"[+] Exported: {city_counts_path}")


# --- Task 8: Visualize distributions ---
def plot_distribution(
    counts: dict[str, int],
    path: Path,
    title: str = "Customer Distribution",
    xlabel: str = "Category",
) -> None:
    """Save a labelled chart of the distribution to path."""
    path.parent.mkdir(parents=True, exist_ok=True)

    labels = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(10, 5), dpi=300)
    bars = plt.bar(labels, values, color="#1B4965", edgecolor="#62B6CB", width=0.6)

    plt.title(title, fontsize=14, fontweight="bold", pad=15)
    plt.xlabel(xlabel, fontsize=11, labelpad=10)
    plt.ylabel("Customer Count", fontsize=11, labelpad=10)
    plt.xticks(rotation=40, ha="right", fontsize=9)
    plt.yticks(range(0, max(values) + 2, 1))
    plt.grid(axis="y", linestyle="--", alpha=0.4)

    for bar in bars:
        height = bar.get_height()
        plt.annotate(
            f"{height}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
        )

    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    print(f"[+] Saved visualization: {path}")


if __name__ == "__main__":
    print("=" * 65)
    print("PESA PULSE - PARTNER CUSTOMER DIRECTORY PIPELINE")
    print("=" * 65)

    # 1. Fetch data
    print("\n[Step 1] Fetching customer data from API...")
    raw_customers = get_customers()
    if not raw_customers:
        print("[-] Pipeline stopped: Unable to fetch data from API.")
        exit(1)
    print(f"[+] Retrieved {len(raw_customers)} raw customer records.")

    # 2. Explore schema
    print("\n[Step 2] Recursive Schema Exploration (First Record):")
    explore(raw_customers[0])

    # 3. Extract and flatten attributes
    print("\n[Step 3] Flattening nested records and casting types...")
    flat_customers = extract_attributes(raw_customers)
    print(f"[+] Successfully extracted {len(flat_customers)} structured records.")

    # 4. Identify unique cities
    cities = unique_cities(flat_customers)
    print(f"\n[Step 4] Unique Cities Identified: {len(cities)} total")
    print(f"         {sorted(cities)}")

    # 5. Count aggregations (pure Python)
    print("\n[Step 5] Computing frequency distributions...")
    c_counts = city_counts(flat_customers)
    d_counts = email_domain_counts(flat_customers)

    # 6. DataFrame conversion and verification
    print("\n[Step 6] Converting to pandas DataFrame & validating counts...")
    df_customers = to_dataframe(flat_customers)
    df_city_counts = pd.DataFrame(
        list(c_counts.items()), columns=["city", "customer_count"]
    )

    pandas_city_counts = df_customers["city"].value_counts().to_dict()
    assert (
        pandas_city_counts == c_counts
    ), "Discrepancy detected between Python and pandas counts!"
    print("[+] Validation passed: Python dictionary counts match pandas value_counts().")

    # 7. Export CSV files
    print("\n[Step 7] Exporting cleaned datasets to CSV...")
    export_csv(df_customers, df_city_counts, OUTPUT_DIR)

    # 8. Visualizations
    print("\n[Step 8] Generating distribution plots...")
    plot_distribution(
        c_counts,
        OUTPUT_DIR / "customer_distribution.png",
        title="Customer Distribution by City",
        xlabel="City",
    )
    plot_distribution(
        d_counts,
        OUTPUT_DIR / "email_domain_distribution.png",
        title="Customer Distribution by Email Top-Level Domain (TLD)",
        xlabel="Top-Level Domain",
    )

    # Summary of findings
    print("\n" + "=" * 65)
    print("FINDINGS SUMMARY (MARKETING & STRATEGY INSIGHTS)")
    print("=" * 65)
    print("1. Regional Density:")
    print(f"   - {len(flat_customers)} total customers are distributed across {len(cities)} distinct cities.")
    print("   - Customer-to-city ratio is 1:1. There is currently no localized clustering,")
    print("     meaning geographic-targeted marketing campaigns will lack economies of scale.")
    print("2. Email Domain Profiles:")
    top_tld = max(d_counts, key=d_counts.get)
    print(f"   - Identified {len(d_counts)} unique top-level domains ({', '.join(d_counts.keys())}).")
    print(f"   - Most frequent extension is '.{top_tld}' with {d_counts[top_tld]} customers.")
    print("3. Deliverables Status:")
    print(f"   - Cleaned directory:    {OUTPUT_DIR / 'customers.csv'}")
    print(f"   - Aggregated metrics:   {OUTPUT_DIR / 'city_counts.csv'}")
    print(f"   - Visualizations:       {OUTPUT_DIR / 'customer_distribution.png'}")
    print(f"                           {OUTPUT_DIR / 'email_domain_distribution.png'}")
    print("=" * 65)