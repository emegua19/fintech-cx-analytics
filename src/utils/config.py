class Config:
    def __init__(self):
        """Initialize configuration with app IDs."""
        self.app_ids = {
            'Commercial Bank of Ethiopia': 'com.combanketh.mobilebanking',  # Replace with actual ID
            'Bank of Abyssinia': 'com.boa.boaMobileBanking',                # Replace with actual ID
            'Dashen Bank': 'com.dashen.dashensuperapp'                      # Replace with actual ID
        }

    def get_app_ids(self):
        """Return app IDs dictionary."""
        return self.app_ids