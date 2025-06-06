# Fintech Reviews Analysis

---

This project analyzes customer satisfaction for mobile apps of three Ethiopian banks (**CBE**, **BOA**, **Dashen Bank**) using an **OOP approach**.  

It:

* Scrapes **Google Play Store reviews**
* Performs **sentiment** and **thematic analysis**
* Stores data in an **Oracle database**
* Generates insights with **visualizations**

Built for the **10 Academy Week 2 Challenge** (04–10 June 2025).

---

##  Folder Structure
```plaintext
fintech-reviews/
├── data/
│   ├── raw/                          # Raw scraped reviews
│   │   ├── cbe_reviews_raw.csv
│   │   ├── boa_reviews_raw.csv
│   │   ├── dashen_reviews_raw.csv
│   ├── processed/                    # Cleaned review data
│   │   ├── bank_reviews_cleaned.csv
│   ├── analysis/                     # Sentiment and theme outputs
│   │   ├── sentiment_results.csv
│   │   ├── themes_per_bank.csv
│   ├── database/                     # SQL scripts for Oracle
│   │   ├── bank_reviews.sql
├── src/
│   ├── __init__.py
│   ├── task_1/                       # Scraper and Preprocessor classes
│   │   ├── __init__.py
│   │   ├── scraper.py                # Scraper class for Google Play reviews
│   │   ├── preprocessor.py           # Preprocessor class for cleaning data
│   ├── task_2/                       # SentimentAnalyzer and ThemeAnalyzer classes
│   │   ├── __init__.py
│   │   ├── sentiment_analyzer.py     # SentimentAnalyzer class for NLP
│   │   ├── theme_analyzer.py         # ThemeAnalyzer class for keyword extraction
│   ├── task_3/                       # DatabaseManager and DataInserter classes
│   │   ├── __init__.py
│   ├── task_4/                       # InsightsGenerator and Visualizer classes
│   │   ├── __init__.py
│   ├── tests/                        # Unit tests for all classes
│   │   ├── __init__.py
│   │   ├── test_scraper.py           # Tests for Scraper class
│   │   ├── test_preprocessor.py      # Tests for Preprocessor class
│   │   ├── test_sentiment.py         # Tests for SentimentAnalyzer class
│   │   ├── test_theme.py             # Tests for ThemeAnalyzer class
│   │   ├── test_database.py          # Tests for DatabaseManager/DataInserter
│   │   ├── test_insights.py          # Tests for InsightsGenerator/Visualizer
├── plots/
├── .github/                          # GitHub workflows (optional)
│   ├── workflows/
│   │   ├── ci.yml                   
├── .gitignore                        # Ignored files
├── requirements.txt                  # Dependencies
├── README.md                         # Project documentation
```
---

##  Setup

###  Clone Repository

```bash
git clone https://github.com/emegua19/fintech-cx-analytics.git
cd fintech-reviews
```

###  Install Dependencies

```bash
pip install -r requirements.txt
```

###  Run Task 1

**Scraper**  
```bash
python -m src.task_1.scraper
```

**Preprocessor**  
```bash
python -m src.task_1.preprocessor
```

###  Run Tests

```bash
pytest src/tests/ -v
```

---
---
##  Dependencies

See `requirements.txt`. Key packages:

* `google-play-scraper` — Review scraping
* `pandas`, `numpy` — Data handling
* `transformers`, `spacy` — NLP analysis
* `matplotlib`, `seaborn` — Visualizations
* `oracledb` — Oracle database connection
* `pytest` — Unit testing

---

##  Notes

* Use **branches** (`task-1` to `task-4`) with **pull requests** for merging.
* Update app IDs in `src/utils/config.py`.
* Fallback to **PostgreSQL** if **Oracle XE** fails; contact facilitators.
* Use Slack channel **#all-week-2** for support.

---

##  Contact

* **Slack**: `#all-week-2`

---
