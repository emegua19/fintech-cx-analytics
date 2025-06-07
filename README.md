# **Fintech Customer Experience Analytics**

**Overview**
This project is part of the **10 Academy Week 2 Challenge**, focusing on analyzing customer reviews for three Ethiopian banks:

* Commercial Bank of Ethiopia
* Bank of Abyssinia
* Dashen Bank

The goal is to derive insights on user experience and sentiment. The project includes **data collection**, **preprocessing**, and **analysis** using **Python** and **machine learning techniques**.

---

## **Folder Structure**

```plaintext
fintech-reviews/
├── data/
│   ├── raw/                          # Raw scraped reviews
│   │   ├── cbe_reviews_raw.csv
│   │   ├── boa_reviews_raw.csv
│   │   ├── dashen_reviews_raw.csv
│   ├── processed/                    # Cleaned review data
│   │   ├── bank_reviews_cleaned.csv
│   ├── analysis/
│   ├── database/
├── src/
│   ├── __init__.py
│   ├── task_1/                       # Scraper and Preprocessor classes
│   │   ├── __init__.py
│   │   ├── scraper.py                # Scraper class for Google Play reviews
│   │   ├── preprocessor.py           # Preprocessor class for cleaning data
│   ├── task_2/                       # SentimentAnalyzer and ThemeAnalyzer classes         
│   ├── task_3/                       # DatabaseManager and DataInserter classes
│   ├── task_4/                       # InsightsGenerator and Visualizer classes
│   ├── tests/                        # Unit tests for all classes
│   │   ├── __init__.py
│   │   ├── test_scraper.py           # Tests for Scraper class
│   │   ├── test_preprocessor.py      # Tests for Preprocessor class
├── plots/
├── .github/                          # GitHub workflows (optional)
│   ├── workflows/
│   │   ├── ci.yml                   
├── .gitignore                        # Ignored files
├── requirements.txt                  # Dependencies
├── README.md                         # Project documentation
```

---

## **Installation**

```bash
# Clone the repository
git clone https://github.com/emegua19/fintech-cx-analytics.git

# Install dependencies
pip install -r requirements.txt

# Ensure Python 3.10 is used
```

---

## **Usage**

```bash
# Run the scraper
python src/task_1/scraper.py

# Run the preprocessor
python src/task_1/preprocessor.py

# (Task 2 analysis scripts to be added)
```

---

## **Methodology**

### **Task 1: Data Collection and Preprocessing**

#### **Data Collection**

* **Source:** Google Play Store reviews
* **Banks:** CBE, BOA, Dashen Bank
* **Tool:** `google-play-scraper` Python library
* **Target:** 400+ reviews per bank (1200+ total)
* **Data Fields:**

  * Review text
  * Rating (1-5)
  * Date
  * Bank name
  * Source (Google Play)
* **Output:**

  ```
  data/raw/
  ├── cbe_reviews_raw.csv
  ├── boa_reviews_raw.csv
  └── dashen_reviews_raw.csv
  ```

#### **Data Preprocessing**

*Implemented in:* `src/task_1/preprocessor.py`

##### **Steps:**

* **Data Loading:**

  * Loads raw CSVs into a single `DataFrame`
  * Gracefully handles missing or empty files

* **Handling Missing Data:**

  * Missing reviews → `''`
  * Missing ratings → `0`
  * Missing bank names → `'Unknown'`
  * Missing source → `'Google Play'`

* **Text Normalization:**

  * Converts text to lowercase
  * Removes special characters (preserving Amharic `\u1200-\u137F`)
  * Strips whitespace
  * Normalizes bank names (e.g., `CBE` → `cbe`)

* **Duplicate Removal:**

  * Based on review text, date, and bank
  * Keeps the first occurrence
  * Reduces duplicates (<5%)

* **Date Normalization:**

  * Converts to `YYYY-MM-DD` using `pd.to_datetime()`
  * Invalid dates → `NaT`

* **Output:**

  ```
  data/processed/bank_reviews_cleaned.csv
  Columns: review, rating, date, bank, source
  ```

  * Prints first 5 rows before and after cleaning

---

### **Amharic Text Handling**

* Uses **UTF-8** encoding for CSV I/O
* Retains Amharic characters using regex `\u1200-\u137F`
* Supports **bilingual** (Amharic + English) reviews

---

## **Testing**

* Unit tests in:

  ```python
  src/tests/test_preprocessor.py
  ```
* Framework: `pytest`
* Tests cover:

  * Data loading
  * Cleaning
  * Duplicate removal
  * Missing data handling
  * Normalization
  * Amharic text preservation
---

## **Contributors**

* **\Yitbarek Geletaw**