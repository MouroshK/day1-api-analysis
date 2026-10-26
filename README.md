# Pesa Pulse Partner Customer Directory Analysis

---

## 1. Project Overview
This project establishes an automated data ingestion, cleaning, normalization, aggregation, and visualization pipeline for Pesa Pulse's partner customer directory. 

The pipeline fetches raw partner records from an external REST API (`https://jsonplaceholder.typicode.com/users`), navigates arbitrarily nested JSON data structures, unpacks relational entities into clean tabular models, validates aggregation results across pure Python and `pandas`, and exports analysis-ready datasets alongside reporting visualizations.

---

## 2. Repository Layout

```text
day1-api-analysis/
├── .venv/                         # Local virtual environment managed via uv
├── output/                        # Pipeline export destination
│   ├── city_counts.csv            # Aggregated customer metrics per city
│   ├── customer_distribution.png  # City distribution visualization (300 DPI)
│   ├── customers.csv              # Fully flattened & typed customer directory
│   └── email_domain_distribution.png # Email TLD distribution chart (300 DPI)
├── src/
│   └── analysis.py                # Core pipeline script (Tasks 1 through 8)
├── pyproject.toml                 # uv project configuration and dependencies
└── README.md                      # Project documentation and strategic findings
```


## 3. Data Schema & Structural Exploration

The ingested customer schema contains multi-level hierarchical records with dictionaries nested up to three tiers deep:

```text
- id: int
- name: str
- username: str
- email: str
- address: dict
  - street: str
  - suite: str
  - city: str
  - zipcode: str
  - geo: dict
    - lat: str
    - lng: str
- phone: str
- website: str
- company: dict
  - name: str
  - catchPhrase: str
  - bs: str
```


### Key Structural Attributes

* **Nested Entities:** `address` and `company` are compound objects containing relational metadata.
* **Deepest Properties:** Geographical coordinates (`lat`, `lng`) reside inside `address['geo']` and are transmitted by the API as string representations.
* **Coordinate Parsing:** The pipeline casts `lat` and `lng` to native Python `float` values (`record["address"]["geo"]["lat"]` and `record["address"]["geo"]["lng"]`) to enable geospatial analysis.

---

## 4. Pipeline Task Architecture

| Task # | Routine | Functional Objective | Implementation Details |
| :--- | :--- | :--- | :--- |
| **Task 1** | `get_customers()` | Resilient API data retrieval | Uses `requests.get()` with a 10-second timeout, `raise_for_status()`, and non-crashing exception handling. |
| **Task 2** | `explore()` | Schema type introspection | Recursive traversal function that computes key depth indentation and prints native Python type names. |
| **Task 3** | `extract_attributes()` | Record unnesting & type casting | Normalizes 10 records into flat row dictionaries containing 12 target fields, parses domain names, and casts coordinate pairs to `float`. |
| **Task 4** | `unique_cities()` | Set-based zone deduplication | Uses a set comprehension `{...}` to identify unique coverage points with $O(1)$ membership checks. |
| **Task 5a** | `city_counts()` | Algorithmic frequency count | Pure Python accumulator loop using `dict.get()` (no external helper libraries) sorted descending by frequency. |
| **Task 5b** | `email_domain_counts()` | Email TLD extraction & count | Dictionary comprehension calculating occurrences across unique Top-Level Domains (`.biz`, `.net`, `.org`, etc.). |
| **Task 6** | `to_dataframe()` | Tabular conversion & validation | Generates a `pandas.DataFrame` and runs `assert` checks confirming `Series.value_counts()` matches the pure Python count. |
| **Task 7** | `export_csv()` | File persistence | Writes standard header-compliant CSV files to `output/customers.csv` and `output/city_counts.csv`. |
| **Task 8** | `plot_distribution()` | Publication-quality visualizations | Generates styled bar charts using `matplotlib` with integer tick marks, angled labels, and numeric bar annotations. |

---

## 5. Strategic Findings & Marketing Insights

### A. Regional Distribution & Market Concentration
* **Metrics:** 10 customer accounts are distributed across 10 distinct cities (`Aliyaview`, `Bartholomebury`, `Gwenborough`, `Howemouth`, `Lebsackbury`, `McKenziehaven`, `Roscoeview`, `South Christy`, `South Elvis`, `Wisokyburgh`).
* **Customer-to-City Ratio:** Exactly **1:1** (1.0).
* **Strategic Takeaway:** The partner network currently displays complete geographic fragmentation with zero local density. Offline marketing initiatives (e.g., regional billboards, local pop-ups, community events) will suffer from low return on investment due to lack of geographic scale. Outreach should prioritize digital-first and non-localized onboarding funnels.

### B. Partner Domain Classifications
* **Metrics:** 8 distinct email Top-Level Domains were identified (`biz`, `net`, `org`, `io`, `me`, `tv`, `ca`, `info`).
* **Dominant Domain:** `.biz` accounts for the largest cohort (30% / 3 customers), followed by engineering/technical extensions (`.io`, `.net`, `.org`).
* **Strategic Takeaway:** Partner communications should accommodate business-to-business (B2B) messaging rather than general retail consumer copy.

---

## 6. Execution Instructions

### Prerequisites
* Windows PowerShell / Command Prompt / Terminal
* Python 3.12+
* `uv` package manager

### Running the Pipeline

1. **Activate the Virtual Environment:**
   ```powershell
   .\.venv\Scripts\Activate.ps1


2. **Execute the Pipeline Script:**
   ```powershell
   python src/analysis.py

   (Or execute directly via the uv runner:)

    ```powershell
   uv run python src/analysis.py
