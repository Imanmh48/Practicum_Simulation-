# Simulation Configuration Parameters
NUMBER_OF_SEASONS = 4

# Threshold configurations
THRESHOLDS = {
    "standard": [1000, 800, 600, 400],
    "competitive": [1500, 900, 700, 500],
    "strict": [2000, 900, 600, 200]
} 

INACTIVITY_THRESHOLDS = [1,2, 3, 4]

DECAY_RATES = {
    "Platinum": 0.10,  # 10% decay
    "Gold": 0.07,      # 7% decay
    "Silver": 0.05,    # 5% decay
    "Bronze": 0.03     # 3% decay
}

INITIAL_BASE_SCORES = {
    "Osama": 0,
    "Iman": 250,
    "Ayoub": 601,
    "Bisma": 750,
    "Fatima": 1000
}

# Event size configuration
EVENT_SIZES = [50, 100, 150, 200, 250] * 4  # Multiply by 4 to get 20 events total
