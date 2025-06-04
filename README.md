# Lancaster County Delinquent Tax Scraper

This project automates the extraction of delinquent tax and property information from the Lancaster County, PA public parcel viewer. It loops through a list of parcel numbers, collects data for the years 2022, 2023, and 2024, and stores it in a CSV file.

I am using a **paid proxy from [Geonode](https://geonode.com/)** to handle requests reliably at scale and avoid rate-limiting or IP bans.

---

## ✅ Features

- Fully automated using Selenium
- Scrapes:
  - Parcel ID
  - Property Information (Address, Use, Status, etc.)
  - Delinquent Tax details (Due, Paid, Total Due)
- Covers **Tax Years**: 2022, 2023, and 2024
- Skips parcels with no delinquent taxes
- Saves clean results in a CSV file
- Uses proxy with optional headless browser

---

## 📁 Project Structure
```
tax_data/
├── .venv/ # Python virtual environment
├── .vscode/ # VSCode config (optional)
├── src/
│ ├── core/
│ │ └── BaseClass.py
│ ├── data/
│ │ ├── parcel_ids.txt # Input: list of parcel numbers
│ │ └── parcels_tax_data.csv # Output: scraped data
│ ├── utils/
│ │ ├── driver_factory.py
│ │ ├── logger.py
│ │ └── selenium_helper.py
│ └── app.py # Main entry point
└── .gitignore
```

---

## 🛠 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Syeda/tax_data.git
cd tax_data
```





Here's your complete `README.md` written in a single Markdown block — including the note that you're using a **paid proxy from Geonode**:

---


### 2. Create and activate a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add parcel numbers

Edit the input file:

```
src/data/parcel_ids.txt
```

Each line should contain one parcel number:

```
5408465600000
...
```

### 5. Run the scraper

```bash
python src/app.py
```

---

## 📤 Output

You will get a file at:

```
src/data/parcels_tax_data.csv
```

Each row includes:

* Parcel ID
* Property Details
* Year-wise delinquent tax info (Due, Paid, Total Due)

Only parcels with delinquent taxes are included.

---

## 🔐 Proxy Settings (via `.env`)

This project uses **Geonode** proxies.

Create a `.env` file in the root directory:

```
GEONODE_HOST=your_host
GEONODE_PORT=your_port
GEONODE_USERNAME=your_username
GEONODE_PASSWORD=your_password
```

The script automatically loads and applies the proxy.


