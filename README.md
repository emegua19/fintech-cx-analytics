###  Updated README.md (ready to copy):

````markdown
# **Fintech Customer Experience Analytics**

**Overview**  
This project is part of the **10 Academy Week 2 Challenge**, focusing on analyzing customer reviews for three Ethiopian banks:

* Commercial Bank of Ethiopia
* Bank of Abyssinia
* Dashen Bank

The goal is to derive insights on user experience and sentiment. The project includes **data collection**, **preprocessing**, **sentiment analysis**, and **visualization** using **Python** and **machine learning techniques**.

---

## **Folder Structure**

```plaintext
fintech-reviews/
├── data/
│   ├── raw/                          # Raw scraped reviews
│   │   ├── cbe_reviews_raw.csv
│   │   ├── boa_reviews_raw.csv
│   │   ├── dashen_reviews_raw.csv
│   ├── processed/                    # Cleaned review data and results
│   │   ├── bank_reviews_cleaned.csv
│   │   ├── sentiment_results.csv
│   │   ├── sentiment_results_aggregated.csv
│   │   ├── language_distribution.csv
│   ├── analysis/
│   ├── database/
├── src/
│   ├── __init__.py
│   ├── task_1/                       # Scraper and Preprocessor classes
│   │   ├── __init__.py
│   │   ├── scraper.py                # Scraper class for Google Play reviews
│   │   ├── preprocessor.py           # Preprocessor class for cleaning data
│   ├── task_2/                       # SentimentAnalyzer and ThemeAnalyzer classes         
│   │   ├── __init__.py
│   │   ├── sentiment_analyzer.py     # SentimentAnalyzer class for sentiment analysis
│   ├── task_3/                       # DatabaseManager and DataInserter classes
│   ├── task_4/                       # InsightsGenerator and Visualizer classes
│   ├── tests/                        # Unit tests for all classes
│   │   ├── __init__.py
│   │   ├── test_scraper.py           # Tests for Scraper class
│   │   ├── test_preprocessor.py      # Tests for Preprocessor class
│   │   ├── test_sentiment_analyzer.py# Tests for SentimentAnalyzer class
├── plots/                            # Visualization outputs (Task 4)
├── .github/                          # GitHub workflows (optional)
│   ├── workflows/
│   │   ├── ci.yml                   
├── .gitignore                        # Ignored files
├── requirements.txt                  # Dependencies
├── README.md                         # Project documentation
````

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
# Run the scraper (Task 1)
python src/task_1/scraper.py

# Run the preprocessor (Task 1)
python src/task_1/preprocessor.py

# Run the sentiment analyzer (Task 2)
python src/task_2/sentiment_analyzer.py
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

* **Output:** `data/raw/*.csv`

#### **Data Preprocessing**

*Implemented in:* `src/task_1/preprocessor.py`

##### **Steps:**

* **Data Loading:** Load raw CSVs into a single DataFrame
* **Handling Missing Data:** Replace missing values (reviews, ratings, bank names, source)
* **Text Normalization:** Lowercase, remove special characters, preserve Amharic `\u1200-\u137F`
* **Duplicate Removal:** Based on review text + date
* **Date Normalization:** Convert to `YYYY-MM-DD`
* **Output:** `data/processed/bank_reviews_cleaned.csv`

---

### **Amharic Text Handling**

* Uses **UTF-8** encoding for CSV I/O
* Preserves Amharic Unicode characters `\u1200-\u137F`
* Supports **bilingual** (Amharic + English) reviews
* Language detection uses:

  * `langdetect` for general language detection
  * Regex for **Amharic/Bilingual** prioritization

---

### **Task 2: Sentiment Analysis**

*Implemented in:* `src/task_2/sentiment_analyzer.py`

#### **Sentiment Analysis Pipeline**

* **Model:** `distilbert-base-uncased-finetuned-sst-2-english`
* **Languages:**

  * English → Analyzed using DistilBERT
  * Amharic + Bilingual → Analyzed using a **custom heuristic**:

    * Simple keyword-based matching:

      * Positive words → POSITIVE (+0.7)
      * Negative words → NEGATIVE (-0.7)
      * Else → NEUTRAL (0.0)
* **Unknown / unsupported languages → NEUTRAL**

#### **Aggregation**

* Aggregated sentiment score by:

  * `bank`
  * `rating`

* **Output:**

  * `data/processed/sentiment_results.csv` → detailed results
  * `data/processed/sentiment_results_aggregated.csv` → for Task 4 visualizations
  * `data/processed/language_distribution.csv`

#### **Sample insights**

* 1-star reviews → strongly negative sentiment → expected
* 5-star reviews → strongly positive sentiment → expected
* Language distribution:

  * English \~ 686
  * Amharic \~ 40
  * Bilingual \~ 6
  * Others → detected but not processed (kept as NEUTRAL)

---

## **Testing**

* Unit tests in:

```python
src/tests/test_preprocessor.py
src/tests/test_sentiment_analyzer.py
```

* Framework: `pytest`

* Tests cover:

  * Language detection
  * Sentiment analysis (English + Amharic + Bilingual)
  * Data loading
  * Cleaning
  * Duplicate removal
  * Missing data handling
  * Normalization
  * Amharic text preservation

---

## **Contributors**

* **Yitbarek Geletaw**

---

## **Notes**

* Bilingual and Amharic sentiment was handled with a simple heuristic due to lack of a high-quality Amharic transformer model.
* English sentiment analysis uses a state-of-the-art transformer model (DistilBERT).
* Future improvements:

  * Explore better Amharic sentiment models
  * Expand theme extraction (Task 2 extension)