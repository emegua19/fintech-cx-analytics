from src.task_2.theme_analyzer import ThemeAnalyzer

# --------------------------------
# Main section to run ThemeAnalyzer
# --------------------------------

if __name__ == "__main__":
    print("\n--- Running ThemeAnalyzer ---\n")

    analyzer = ThemeAnalyzer()
    analyzer.run_pipeline()

    print("\n--- ThemeAnalyzer finished ---\n")
