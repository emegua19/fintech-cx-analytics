# **Fintech Customer Experience Analytics**

**Overview**
This project is part of the **10 Academy Week 2 Challenge**, focusing on analyzing customer reviews for three Ethiopian banks:

* Commercial Bank of Ethiopia
* Bank of Abyssinia
* Dashen Bank

The goal is to derive insights on user experience and sentiment. The project includes **data collection**, **preprocessing**, **sentiment analysis**, **database integration**, **thematic analysis**, and **visualization** using **Python**, **PostgreSQL**, and **machine learning techniques**.

---

## **Folder Structure**

```plaintext
fintech-reviews/
├── data/
│   ├── raw/                          # Raw scraped reviews
│   ├── processed/                    # Cleaned review data and results
│   ├── analysis/                     # Thematic outputs
│   ├── database/                     # SQL schema and inserts
├── src/
│   ├── task_1/                       # Scraper and Preprocessor
│   ├── task_2/                       # SentimentAnalyzer and ThemeAnalyzer
│   ├── task_3/                       # DatabaseManager and DataInserter
│   ├── task_4/                       # Visualizer and Insight classes
│   ├── utils/                        # Config and DataHandler
│   │   ├── config.py
│   │   ├── data_handler.py
│   ├── tests/                        # Unit tests
│   │   ├── test_scraper.py
│   │   ├── test_preprocessor.py
│   │   ├── test_sentiment.py
│   │   ├── test_theme.py
├── scripts/                          # Execution scripts
│   ├── run_scraper.py
│   ├── run_preprocessor.py
│   ├── run_sentiment_analysis.py
│   ├── run_theme_analyzer.py
│   ├── run_database_insert.py
│   ├── run_visualizations.py
├── plots/                            # Task 4 output images
├── .github/                          # Optional CI workflows
├── .gitignore
├── requirements.txt
├── README.md                         # This documentation
```

---

## **Installation**

```bash
# Clone the repository
git clone https://github.com/emegua19/fintech-cx-analytics.git
cd fintech-cx-analytics

# Install dependencies
pip install -r requirements.txt
```

---

## **Git Setup**

```bash
# Set up Git for collaboration
# Create and switch to a new task branch (e.g., task-1)
git checkout -b task-1

# Stage changes
git add .

# Commit with a meaningful message
git commit -m "Add scraper implementation"

# Push to GitHub
git push origin task-1

# Create a pull request to merge into main
```

---

## **Usage**

```bash
# Task 1: Scraping and Preprocessing
python scripts/run_scraper.py
python scripts/run_preprocessor.py

# Task 2: Sentiment + Thematic Analysis
python scripts/run_sentiment_analysis.py
python scripts/run_theme_analyzer.py

# Task 3: Store cleaned data into PostgreSQL
python scripts/run_database_insert.py

# Task 4: Generate final visualizations
python scripts/run_visualizations.py
```

---

## **Task 1: Data Collection and Preprocessing**

### **Data Collection**

* Scrape reviews using `google-play-scraper` in English and Amharic
* Apps: CBE, BOA, Dashen
* Fields: `review`, `rating`, `date`, `bank`, `source`
* Output: `data/raw/*.csv`

### **Preprocessing**

* Remove duplicates, handle missing data, normalize text (Amharic preserved)
* Normalize dates, filter invalid ratings
* Language detection via regex + langdetect
* Output: `data/processed/bank_reviews_cleaned.csv`

---

## **Task 2: Sentiment and Thematic Analysis**

### **Sentiment Analysis**

* Model: `distilbert-base-uncased-finetuned-sst-2-english`
* Custom rule-based heuristics for Amharic and bilingual reviews
* Score range: \[-1, 1]
* Output:

  * `sentiment_results.csv`
  * `sentiment_results_aggregated.csv`

### **Thematic Analysis**

* Extract keywords using TF-IDF
* Group into 3–5 themes per bank:

  * Account Access Issues
  * Transaction Performance
  * User Experience
  * Support & Communication
  * Feature Requests
* Output includes themes with examples per review

---

## **Task 3: Database Integration**

* PostgreSQL used (fallback from Oracle)
* Two tables:

  * `banks`: ID, name
  * `reviews`: review text, rating, sentiment, theme, date, foreign key to bank
* Data inserted using `psycopg2`
* Dump file: `data/database/postgres_dump.sql`

---

## **Task 4: Visualization**

* 7 plots generated in `plots/`:

  * Language distribution
  * Rating distribution per bank
  * Sentiment vs rating
  * Sentiment by bank
  * Theme frequency
  * Sentiment vs theme
  * WordCloud per bank

---

## **Testing**

Unit tests with `pytest` in `src/tests/`:

* Scraper (`test_scraper.py`)
* Preprocessor (`test_preprocessor.py`)
* Sentiment Analyzer (`test_sentiment.py`)
* Thematic Analyzer (`test_theme.py`)

---

## **Contributors**

* Yitbarek Geletaw

---

## **Notes**

* DistilBERT is reliable for English but struggles with mixed-language or noisy input
* Amharic handled using Unicode-aware regex + keyword heuristics
* PostgreSQL integration used to simulate enterprise pipelines
* Future: Improve Amharic model, enhance clustering using LDA or BERTopic
