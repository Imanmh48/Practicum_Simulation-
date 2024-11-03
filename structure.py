import math

class Participant:
    def __init__(self, name, base_score, volunteer_hours=0, badges=None):
        self.name = name
        self.base_score = base_score
        self.volunteer_hours = volunteer_hours
        
        # Initialize volunteer-related attributes
        self.attendance_rate = 0           
        self.task_completion_rate = 0      
        self.group_task_completion_rate = 0 
        self.problem_resolution_rate = 0   
        self.conflict_resolution_rate = 0  
        self.communication_score = 0       
        
        # Leadership attributes
        self.leadership_tasks_completed = 0 
        self.leadership_appointments = 0    
        
        self.rank = None
        self.justification = ""
        self.badges = badges if badges is not None else []

        # Total scores
        self.volunteer_score = 0  # To be calculated based on metrics
        self.score = self.base_score  # Total score initialized with base score

    def calculate_volunteer_score(self):
        self.volunteer_score = math.ceil((self.attendance_rate * 0.1 +
                                           self.task_completion_rate * 0.1 +
                                           self.group_task_completion_rate * 0.1 +
                                           self.problem_resolution_rate * 0.1 +
                                           self.conflict_resolution_rate * 0.1 +
                                           self.communication_score * 0.2 +  
                                           self.leadership_tasks_completed * 0.2 +  
                                           self.leadership_appointments * 0.1) * 10)
        self.score = self.base_score + self.volunteer_score

    def update_metrics(self, communication_score, attendance_rate, task_completion_rate,
                       group_task_completion_rate, problem_resolution_rate,
                       conflicts_resolved, total_conflicts,
                       leadership_tasks_completed, leadership_appointments):
        self.communication_score = communication_score
        self.attendance_rate = attendance_rate
        self.task_completion_rate = task_completion_rate
        self.group_task_completion_rate = group_task_completion_rate
        self.problem_resolution_rate = problem_resolution_rate
        
        self.conflict_resolution_rate = (conflicts_resolved / total_conflicts) if total_conflicts > 0 else 0
        self.leadership_tasks_completed = leadership_tasks_completed
        self.leadership_appointments = leadership_appointments

        self.calculate_volunteer_score()

    def assign_rank_based_on_points(self):
        # Assign rank based on total score points
        if self.score < 500:
            self.rank = 1
            self.justification = "Rank 1: Beginner (0 - 499 points)"
        elif 500 <= self.score < 1000:
            self.rank = 2
            self.justification = "Rank 2: Intermediate (500 - 999 points)"
        elif 1000 <= self.score < 2000:
            self.rank = 3
            self.justification = "Rank 3: Advanced (1000 - 1999 points)"
        else:
            self.rank = 4
            self.justification = "Rank 4: Expert (2000+ points)"

    def add_badge(self, badge):
        # Only add badge if it doesn't already exist
        if badge not in self.badges:
            self.badges.append(badge)

    def __repr__(self):
        return (f"{self.name} | Base Score: {self.base_score} | Volunteer Score: {self.volunteer_score} | "
                f"Total Score: {self.score} | Rank: {self.rank} | Justification: {self.justification} | "
                f"Badges: {', '.join(self.badges)}")


class RankingSystem:
    def __init__(self, participants, seasonal_reset_interval=4):
        self.participants = participants
        self.seasonal_reset_interval = seasonal_reset_interval
        self.calculation_count = 0

    def calculate_ranks(self):
        for participant in self.participants:
            participant.assign_rank_based_on_points()

        # Increment calculation count
        self.calculation_count += 1

    
        # if self.calculation_count >= self.seasonal_reset_interval:
        #     self.seasonal_reset_average()
        #     self.calculation_count = 0

    def seasonal_reset_average(self):
        avg_base_score = sum(p.base_score for p in self.participants) / len(self.participants)
        for participant in self.participants:
            participant.base_score = avg_base_score
            participant.calculate_volunteer_score()
            participant.assign_rank_based_on_points()
            participant.justification += " | Seasonal reset applied, base score set to average."

    def award_badges(self):
        for participant in self.participants:
            if participant.volunteer_hours >= 20:
                participant.add_badge("Volunteer Star")
            if participant.rank == 4:
                participant.add_badge("Top Performer")

    def apply_penalties(self):
        for participant in self.participants:
            if participant.score < 0:
                pass

    def display_results(self):
        # Print header
        header = f"{'Name':<10} | {'Base Score':<12} | {'Volunteer Score':<15} | {'Total Score':<12} | {'Rank':<5} | {'Justification':<30} | {'Badges'}"
        print(header)
        print("-" * len(header))

        # Print each participant's details
        for participant in sorted(self.participants, key=lambda p: p.rank):
            badges = ", ".join(participant.badges) if participant.badges else "None"
            row = (f"{participant.name:<10} | {participant.base_score:<12.1f} | {participant.volunteer_score:<15} | "
                   f"{participant.score:<12.1f} | {participant.rank:<5} | {participant.justification:<30} | {badges}")
            print(row)


# Example usage
if __name__ == "__main__":
    # Create a list of participants with realistic base scores to simulate different ranks
    participants = [
        Participant(name="Osama", base_score=22, volunteer_hours=25),
        Participant(name="Iman", base_score=20, volunteer_hours=30),
        Participant(name="Ayoub", base_score=30, volunteer_hours=15),
        Participant(name="Bisma", base_score=50000, volunteer_hours=35),
        Participant(name="Fatima", base_score=80, volunteer_hours=40)
    ]

    # Update metrics for each participant with adjusted values to reach different ranks
    participants[0].update_metrics(7, 0.85, 0.8, 0.78, 0.82, 5, 5, 2, 1)  # Osama, around Rank 1 or 2
    participants[1].update_metrics(8, 0.9, 0.85, 0.8, 0.88, 4, 5, 3, 2)   # Iman, should reach Rank 2
    participants[2].update_metrics(9, 0.95, 0.9, 0.85, 0.9, 6, 7, 4, 3)   # Ayoub, should reach Rank 3
    participants[3].update_metrics(10, 1.0, 0.95, 0.9, 0.92, 8, 10, 6, 5) # Bisma, close to Rank 3 or 4
    participants[4].update_metrics(10, 1.0, 0.95, 0.9, 0.95, 10, 10, 7, 6) # Fatima, should reach Rank 4

    # Create a Ranking System instance
    ranking_system = RankingSystem(participants)

    # Simulate multiple score calculations to test the seasonal reset
    for _ in range(5):  # Run the calculation multiple times
        ranking_system.calculate_ranks()          # Calculate ranks based on scores
        ranking_system.award_badges()             # Award badges based on achievements
        ranking_system.apply_penalties()          # Apply decay penalties if necessary

    # Display final results
    ranking_system.display_results()
