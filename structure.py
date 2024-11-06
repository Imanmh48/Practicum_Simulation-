import random

class Participant:
    def __init__(self, name, base_score):
        self.name = name
        self.base_score = base_score

        self.response_time = 0.0
        self.attendance_rate = 0.0
        self.task_completion_rate = 0.0

        self.event_score = 0.0

        self.hours_commitment = 0.0
        self.team_performance = 0.0
        self.problem_solving = 0.0
        self.conflict_resolution = 0.0
        self.leadership_metrics = 0.0
        self.leadership_appointments = 0.0
        self.cancellations_rate = 0.0

        self.total_score = base_score
        self.rank = ""
        self.inactivity_period = 0


    def calculate_event_score(self, event_size):
        # Assign event_score based on event_size thresholds
        if event_size > 200:
            self.event_score = 300
        elif event_size > 100:
            self.event_score = 200
        elif event_size > 50:
            self.event_score = 150
        else:
            self.event_score = 100  # Default score for small events

    def determine_rank(self):
        if self.total_score >= 600:
            self.rank = "Platinum"
        elif self.total_score >= 500:
            self.rank = "A"
        elif self.total_score >= 300:
            self.rank = "B"
        elif self.total_score >= 100:
            self.rank = "C"
        else:
            self.rank = "D"

    def award_badge(self):
        if self.task_completion_rate >= 0.9:
            return "Gold Badge"
        elif self.task_completion_rate >= 0.7:
            return "Silver Badge"
        elif self.task_completion_rate >= 0.5:
            return "Bronze Badge"
        else:
            return "No Badge"

    def apply_decay(self):
        # Calculate the total score before applying decay
        total_score_before_decay = self.base_score + (self.event_score * 100) + (self.task_completion_rate * 100)

        # Apply inactivity decay if applicable and rank is Platinum
        if self.inactivity_period > 3 and self.rank == "Platinum":
            print(f"Total Score before decay for {self.name}: {total_score_before_decay:.2f}")
            inactivity_decay = total_score_before_decay * 0.10  # 10% decay for inactivity
            total_score_before_decay -= inactivity_decay
            print(f"Decay applied for inactivity to {self.name}: -{inactivity_decay:.2f}")

        # Set the total score after decay
        self.total_score = total_score_before_decay

def simulate_events(num_events, event_size):  # Function to handle a specific event size
    participants = [
        Participant(name="Osama", base_score=500),
        Participant(name="Iman", base_score=550),
        Participant(name="Ayoub", base_score=600),
        Participant(name="Bisma", base_score=400),
        Participant(name="Fatima", base_score=450)
    ]

    print(f"\nSimulating with Event Size: {event_size}")  # Print the event size before the events
    print("=" * 80)
    for event_number in range(1, num_events + 1):
        print(f"\nEvent {event_number} (Event Size: {event_size}):")
        print("=" * 50)
        print(f"{'Name':<10} | {'Base Score':<10} | {'Completion Rate':<15} | {'Event Score':<15} | {'Total Score':<15} | {'Rank':<6} | {'Inactivity':<10}")
        print("-" * 92)

        for participant in participants:
            participant.task_completion_rate = random.uniform(0.0, 1.0)
            participant.calculate_event_score(event_size)  # Use the given event size for score calculation

            if participant.name == "Ayoub" and event_number <= 5:
                participant.inactivity_period += 1
            else:
                participant.inactivity_period = 0

            # Apply decay before updating final total score
            participant.apply_decay()

            # Determine rank and award badge
            participant.determine_rank()
            badge = participant.award_badge()
            print(f"{participant.name:<10} | {participant.base_score:<10.1f} | {participant.task_completion_rate:<15.2f} | {participant.event_score:<15.2f} | {participant.total_score:<15.1f} | {participant.rank:<6} | {participant.inactivity_period:<10} | Badge: {badge}")
        print("=" * 50)  # Separator between events

# Test different event sizes
event_sizes = [50, 100, 150, 200, 250]  # List of different event sizes to test

for event_size in event_sizes:
    simulate_events(10, event_size)  # Simulate 10 events for each event size
