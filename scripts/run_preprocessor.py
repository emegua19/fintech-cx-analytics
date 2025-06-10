from src.utils.data_handler import DataHandler
from src.task_1.preprocessor import Preprocessor

# --------------------------------
# Main section to run preprocessor
# --------------------------------

if __name__ == "__main__":
    print("\n--- Running Preprocessor ---\n")

    data_handler = DataHandler()
    preprocessor = Preprocessor(data_handler)

    # Run Preprocessor main()
    preprocessor.main()

    print("\n--- Preprocessing completed ---\n")
