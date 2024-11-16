import random
# Simulation Configuration Parameters
NUMBER_OF_SEASONS = 4
NUMBER_OF_VOLUNTEERS = 19
PERSONALITIES = ["lazy","average","growing","unconsistent","ideal"]
# Threshold configurations
THRESHOLDS = {
    "standard": [1000, 800, 600, 400],
    "competitive": [1500, 900, 700, 500],
    "strict": [2000, 900, 600, 200]
} 

INACTIVITY_THRESHOLDS = [1, 2, 3, 4]

DECAY_RATES = {
    "Platinum": 0.20,  # 10% decay
    "Gold": 0.15,      # 7% decay
    "Silver": 0.10,    # 5% decay
    "Bronze": 0.08     # 3% decay
}
HIGHEST_POSSIBLE_SCORE=1000
INITIAL_BASE_SCORES={}
for v in range(NUMBER_OF_VOLUNTEERS):
    if v%3==0:
        INITIAL_BASE_SCORES["v"+str(v+1)]=0  # Setting some of the scores to 0 as if they are new
    else:
        INITIAL_BASE_SCORES["v"+str(v+1)]=random.randint(0,HIGHEST_POSSIBLE_SCORE)
# INITIAL_BASE_SCORES = {
#     "Osama": 0,
#     "Iman": 250,
#     "Ayoub": 601,
#     "Bisma": 750,
#     "Fatima": 1000
# }

# Event size configuration
EVENT_SIZES = [50, 100, 150, 200, 250] * 4  # Multiply by 4 to get 20 events total

METRICS_DECLINE_THRESHOLD = 2.0  # Threshold for metrics score decline

METRICS_DECLINE_DECAY_RATE = 0.15 

EVENT_SCORE_CONFIG = {
    'thresholds': [200, 100, 50, 10],  # Size thresholds in descending order
    'scores': [50, 100, 150, 200]     # Corresponding scores
}