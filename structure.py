import random

from sim1 import VolunteerMetrics
from Event import Event

class Participant:
    def __init__(self, name, base_score):
        self.name = name
        self.base_score = base_score

        self.response_time = 0.0
        self.attendance_rate = 0.0
        self.task_completion_rate = 0.0

        self.event_score = 0.0
        self.metrics_score = 0.0  # the current position of the participant in the metrics

        self.hours_commitment = 0.0
        self.team_performance = 0.0
        self.problem_solving = 0.0
        self.conflict_resolution = 0.0
        self.leadership_metrics = 0.0
        self.leadership_appointments = 0.0

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
    
    def update_metrics_score(self, event, response_time_mins, late_arrivals, early_departures, 
                             unscheduled_absences, completed_tasks, total_tasks,
                             logged_hours, expected_hours, team_completed, team_total,
                             actual_time, planned_time, problem_time, expected_problem_time,
                             successful_solutions, total_solutions, conflicts_resolved, 
                             total_conflicts):
        """Update metrics score based on event's metrics weights and provided metric values"""
        # Get weights from event object
        weights = event._get_weights_for_type(event.event_type)
        
        # Calculate new metric scores with weights applied
        metrics = VolunteerMetrics()
        
        # Calculate new metric scores with weights applied
        new_response_time = metrics.calculate_response_time(response_time_mins) * weights['response_time']
        new_attendance = metrics.calculate_attendance(late_arrivals, early_departures, unscheduled_absences, 5) * weights['attendance_rate']
        new_task_completion = metrics.calculate_task_completion(completed_tasks, total_tasks) * weights['task_completion']
        new_hours = metrics.calculate_hours_commitment(logged_hours, expected_hours)  # No weight for hours
        new_team_perf = metrics.calculate_team_performance(team_completed, team_total, actual_time, planned_time) * weights['team_performance']
        new_problem_solving = metrics.calculate_problem_solving(problem_time, expected_problem_time, successful_solutions, total_solutions) * weights['problem_solving']
        new_conflict = metrics.calculate_conflict_resolution(conflicts_resolved, total_conflicts) * weights['conflict_resolution']
        new_leadership = metrics.calculate_leadership_metrics(team_completed, team_total, self.leadership_appointments) * weights['leadership']
        
        # Update metrics by averaging with previous weighted values
        self.response_time = (self.response_time + new_response_time) / 2
        self.attendance_rate = (self.attendance_rate + new_attendance) / 2
        self.task_completion_rate = (self.task_completion_rate + new_task_completion) / 2
        self.hours_commitment = (self.hours_commitment + new_hours) / 2
        self.team_performance = (self.team_performance + new_team_perf) / 2
        self.problem_solving = (self.problem_solving + new_problem_solving) / 2
        self.conflict_resolution = (self.conflict_resolution + new_conflict) / 2
        self.leadership_metrics = (self.leadership_metrics + new_leadership) / 2
        
        # Sum up all weighted metrics for final score
        self.metrics_score = (
            self.response_time +
            self.attendance_rate + 
            self.task_completion_rate +
            self.team_performance +
            self.problem_solving +
            self.leadership_metrics +
            self.conflict_resolution
        )

    def determine_rank(self, thresholds):
        if self.total_score >= thresholds[0]:
            self.rank = 'Platinum'
        elif self.total_score >= thresholds[1]:
            self.rank = 'Gold'
        elif self.total_score >= thresholds[2]:
            self.rank = 'Silver'
        elif self.total_score >= thresholds[3]:
            self.rank = 'Bronze'
        else:
            self.rank = 'Bronze'

    @staticmethod
    def award_badges(rank, hours_logged, leadership_score, conflict_resolution_score):
        badges = []
        if leadership_score >= 8 and conflict_resolution_score >= 8:
            badges.append("Skills Badge")
        if hours_logged >= 50:
            badges.append("Hours Served Badge")
        if rank == 'Platinum':
            badges.append("Platinum Achievement Badge")
        elif rank == 'Gold':
            badges.append("Gold Achievement Badge")
        elif rank == 'Silver':
            badges.append("Silver Achievement Badge")
        elif rank == 'Bronze':
            badges.append("Bronze Achievement Badge")
        return badges

    def apply_decay(self):
        # Calculate the total score before applying decay
        total_score_before_decay = self.base_score + (self.event_score) + (self.metrics_score)

        # Apply inactivity decay if applicable and rank is Platinum
        if self.inactivity_period > 3 and self.rank == "Platinum":
            print(f"Total Score before decay for {self.name}: {total_score_before_decay:.2f}")
            inactivity_decay = total_score_before_decay * 0.10  # 10% decay for inactivity
            total_score_before_decay -= inactivity_decay
            print(f"Decay applied for inactivity to {self.name}: -{inactivity_decay:.2f}")

        # Set the total score after decay
        self.total_score = total_score_before_decay

def simulate_events(num_events, event_size, threshold_type="even_spread"):
    THRESHOLDS = {
        "standard": [1000, 800, 600, 400],
        "competitive": [1500, 900, 700, 500],
        "strict": [2000, 900, 600, 200]
    }
    
    thresholds = THRESHOLDS.get(threshold_type, THRESHOLDS["standard"])

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
        print(f"{'Name':<10} | {'Base Score':<10} | {'Metrics_Score':<15} | {'Event Score':<15} | {'Total Score':<15} | {'Rank':<6} | {'Inactivity':<10}")
        print("-" * 92)

        for participant in participants:
            event = Event("Test Event", event_size, "2024-01-01", "standard")
            if participant.name == "Ayoub":  # Highest base score (600) - Best performer
                participant.update_metrics_score(
                    event=event,
                    response_time_mins=15,   # Exceptional response time
                    late_arrivals=0,         # Perfect attendance
                    early_departures=0,
                    unscheduled_absences=0,
                    completed_tasks=10,      # Perfect task completion
                    total_tasks=10,
                    logged_hours=40,         # Full hours commitment
                    expected_hours=40,
                    team_completed=10,       # Perfect team performance
                    team_total=10,
                    actual_time=40,          # Perfect time management
                    planned_time=40,
                    problem_time=40,         # Excellent problem solving
                    expected_problem_time=40,
                    successful_solutions=10,  # Perfect solutions
                    total_solutions=10,
                    conflicts_resolved=10,    # Perfect conflict resolution
                    total_conflicts=10
                )
            elif participant.name == "Iman":  # Second highest (550) - Very good performer
                participant.update_metrics_score(
                    event=event,
                    response_time_mins=20,   # Very good response time
                    late_arrivals=0,
                    early_departures=1,      # Occasional early departure
                    unscheduled_absences=0,
                    completed_tasks=9,       # Very good completion rate
                    total_tasks=10,
                    logged_hours=38,         # Strong hours commitment
                    expected_hours=40,
                    team_completed=9,
                    team_total=10,
                    actual_time=38,
                    planned_time=40,
                    problem_time=38,
                    expected_problem_time=40,
                    successful_solutions=9,
                    total_solutions=10,
                    conflicts_resolved=9,
                    total_conflicts=10
                )
            elif participant.name == "Osama":  # Middle score (500) - Good performer
                participant.update_metrics_score(
                    event=event,
                    response_time_mins=30,   # Average response time
                    late_arrivals=1,         # Some late arrivals
                    early_departures=1,
                    unscheduled_absences=0,
                    completed_tasks=8,       # Good task completion
                    total_tasks=10,
                    logged_hours=35,         # Fair hours commitment
                    expected_hours=40,
                    team_completed=8,
                    team_total=10,
                    actual_time=35,
                    planned_time=40,
                    problem_time=35,
                    expected_problem_time=40,
                    successful_solutions=8,
                    total_solutions=10,
                    conflicts_resolved=8,
                    total_conflicts=10
                )
            elif participant.name == "Bisma":  # Lower score (400) - Moderate performer
                participant.update_metrics_score(
                    event=event,
                    response_time_mins=40,   # Slow response time
                    late_arrivals=1,
                    early_departures=2,      # Fair attendance
                    unscheduled_absences=0,
                    completed_tasks=6,       # Fair completion rate
                    total_tasks=10,
                    logged_hours=30,         # Fair hours commitment
                    expected_hours=40,
                    team_completed=7,
                    team_total=10,
                    actual_time=30,
                    planned_time=40,
                    problem_time=30,
                    expected_problem_time=40,
                    successful_solutions=7,
                    total_solutions=10,
                    conflicts_resolved=6,
                    total_conflicts=10
                )
            elif participant.name == "Fatima":  # Lowest score (450) - Needs improvement
                participant.update_metrics_score(
                    event=event,
                    response_time_mins=60,   # Slow response time
                    late_arrivals=3,
                    early_departures=3,      # Frequent departures
                    unscheduled_absences=1,  # Occasional absences
                    completed_tasks=5,       # Fair task completion
                    total_tasks=10,
                    logged_hours=25,         # Limited hours commitment
                    expected_hours=40,
                    team_completed=6,
                    team_total=10,
                    actual_time=25,
                    planned_time=40,
                    problem_time=25,
                    expected_problem_time=40,
                    successful_solutions=5,
                    total_solutions=10,
                    conflicts_resolved=5,
                    total_conflicts=10
                )

            participant.calculate_event_score(event_size)
            participant.apply_decay()
            participant.total_score += participant.event_score + participant.metrics_score

            participant.determine_rank(thresholds)
            inactivity_display = f"{participant.inactivity_period} months" if participant.inactivity_period > 0 else "Active"
            print(f"{participant.name:<10} | {participant.base_score:<10} | {participant.metrics_score:<15.2f} | {participant.event_score:<15} | {participant.total_score:<15.2f} | {participant.rank:<6} | {inactivity_display:<10}")
