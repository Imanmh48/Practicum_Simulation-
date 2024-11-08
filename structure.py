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
        self.metrics_score = 0.0 # the current postion of the participant in the metrics

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
        # If participant is inactive, event_score is 0
        if self.inactivity_period >= 1:
            self.event_score = 0
            return

        # Otherwise, assign event_score based on event_size thresholds
        if event_size > 200:
            self.event_score = 100
        elif event_size > 100:
            self.event_score = 150
        elif event_size > 50:
            self.event_score = 200
        else:
            self.event_score = 300  # Default score for small events
    
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

    def determine_rank(self):
        if self.total_score >= 600:
            self.rank = "Platinum"
        elif self.total_score >= 500:
            self.rank = "Gold"
        elif self.total_score >= 300:
            self.rank = "Silver"
        elif self.total_score >= 100:
            self.rank = "Bronze"
        else:
            self.rank = "No Rank"
    

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
        # Calculate total score differently based on inactivity
        if self.inactivity_period >= 1:
            total_score_before_decay = self.base_score + self.event_score  # Exclude metrics_score when inactive
        else:
            total_score_before_decay = self.base_score + self.event_score + self.metrics_score

        # Apply inactivity decay if applicable and rank is Platinum
        if self.inactivity_period > 3 and self.rank == "Platinum":
            print(f"Total Score before decay for {self.name}: {total_score_before_decay:.2f}")
            inactivity_decay = total_score_before_decay * 0.10  # 10% decay for inactivity
            total_score_before_decay -= inactivity_decay
            print(f"Decay applied for inactivity to {self.name}: -{inactivity_decay:.2f}")

        # Set the total score after decay
        self.total_score = total_score_before_decay

def apply_reset(list_participants,highest_rank=15000): #this will apply the reset for all classes
    for participant in list_participants:
        if participant.base_score>=highest_rank: #will change this to be if they are above platinum they will be reset to platinum
            participant.base_score=highest_rank
        else:
            participant.base_score-=50 #will change this value once we determine the ranks

def distrubte_events_across_seasons(num_of_events,num_of_seasons):
    counter=0
    while True: 
        event_assignment=[]
        for i in range(num_of_seasons):
            num_of_event=random.randint(1,num_of_events) #generate a random number of events
            event_assignment.append(num_of_event) # append that number
        if sum(event_assignment)==num_of_events: # make sure that my generated number of event is equal to all_events
            print("number of events distribution")
            print(event_assignment)
            break
        counter+=1
        if counter==2000: #safeguard
            print("out")
            break
    return event_assignment

def simulate_events(num_events, event_size, participants, start_event_number):
    the_gap = 5
    current = 0
    event_distribution = distrubte_events_across_seasons(num_events, 5)
    breakpoint = event_distribution[current]
    counter = 1
    
    print(f"\nSimulating with Event Size: {event_size}")
    print("=" * 80)
    
    for event_number in range(start_event_number, start_event_number + num_events):
        if (event_number - 1) == breakpoint:
            print("Season", counter + 1)
            print("#" * 90)
            # apply_reset(participants)
            counter += 1
            current += 1
            breakpoint += event_distribution[current]
        
        print(f"\nEvent {event_number} (Event Size: {event_size}):")
        print("=" * 50)
        print(f"{'Name':<10} | {'Base Score':<10} | {'Metrics_Score':<15} | {'Event Score':<15} | {'Total Score':<15} | {'Rank':<6} | {'Inactivity':<10}")
        print("-" * 92)

        for participant in participants:
            event = Event("Test Event", event_size, "2024-01-01", "standard")
            
            # Osama (base_score = 0) - New participant, average performance
            if participant.name == "Osama":
                participant.update_metrics_score(
                    event=event,
                    response_time_mins=35,   # Average response time
                    late_arrivals=1,         # Some attendance issues expected
                    early_departures=1,
                    unscheduled_absences=1,
                    completed_tasks=7,       # Average completion rate
                    total_tasks=10,
                    logged_hours=35,         # Average hours commitment
                    expected_hours=40,
                    team_completed=7,
                    team_total=10,
                    actual_time=35,
                    planned_time=40,
                    problem_time=35,
                    expected_problem_time=40,
                    successful_solutions=7,
                    total_solutions=10,
                    conflicts_resolved=7,
                    total_conflicts=10
                )
            # Iman (base_score = 250) - Developing performer
            elif participant.name == "Iman":
                participant.update_metrics_score(
                    event=event,
                    response_time_mins=30,   # Better than average
                    late_arrivals=1,
                    early_departures=1,
                    unscheduled_absences=0,
                    completed_tasks=8,       # Good completion rate
                    total_tasks=10,
                    logged_hours=36,
                    expected_hours=40,
                    team_completed=8,
                    team_total=10,
                    actual_time=36,
                    planned_time=40,
                    problem_time=36,
                    expected_problem_time=40,
                    successful_solutions=8,
                    total_solutions=10,
                    conflicts_resolved=8,
                    total_conflicts=10
                )
            # Ayoub (base_score = 500) - Experienced performer
            elif participant.name == "Ayoub":
                participant.update_metrics_score(
                    event=event,
                    response_time_mins=20,   # Very good response time
                    late_arrivals=0,         # Strong attendance
                    early_departures=0,
                    unscheduled_absences=0,
                    completed_tasks=9,       # Very good completion
                    total_tasks=10,
                    logged_hours=38,
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
            # Bisma (base_score = 750) - Senior performer
            elif participant.name == "Bisma":
                participant.update_metrics_score(
                    event=event,
                    response_time_mins=15,   # Excellent response time
                    late_arrivals=0,
                    early_departures=0,
                    unscheduled_absences=0,
                    completed_tasks=9,
                    total_tasks=10,
                    logged_hours=39,
                    expected_hours=40,
                    team_completed=9,
                    team_total=10,
                    actual_time=39,
                    planned_time=40,
                    problem_time=39,
                    expected_problem_time=40,
                    successful_solutions=9,
                    total_solutions=10,
                    conflicts_resolved=9,
                    total_conflicts=10
                )
            # Fatima (base_score = 1000) - Expert performer
            else:
                participant.update_metrics_score(
                    event=event,
                    response_time_mins=10,   # Outstanding response time
                    late_arrivals=0,         # Perfect attendance
                    early_departures=0,
                    unscheduled_absences=0,
                    completed_tasks=10,      # Perfect completion
                    total_tasks=10,
                    logged_hours=40,         # Full commitment
                    expected_hours=40,
                    team_completed=10,
                    team_total=10,
                    actual_time=40,
                    planned_time=40,
                    problem_time=40,
                    expected_problem_time=40,
                    successful_solutions=10,
                    total_solutions=10,
                    conflicts_resolved=10,
                    total_conflicts=10
                )

            

            if participant.name == "Ayoub" and event_number <= 5:  # Makes Ayoub inactive for first 5 events
                participant.inactivity_period += 1
            else:
                participant.inactivity_period = 0
            
            participant.calculate_event_score(event_size)  # Use the given event size for score calculation

            # Apply decay before updating final total score
            participant.apply_decay()

            # Calculate the real metrics_score but display 0 if inactive
            display_metrics_score = 0 if participant.inactivity_period >= 1 else participant.metrics_score
            
            participant.determine_rank()
            badge = participant.award_badge()
            inactivity_display = f"{participant.inactivity_period} months" if participant.inactivity_period > 0 else "Active"
            
            # Use display_metrics_score for printing
            print(f"{participant.name:<10} | {participant.base_score:<10.1f} | {display_metrics_score:<15.2f} | {participant.event_score:<15.2f} | {participant.total_score:<15.1f} | {participant.rank:<6} | {participant.inactivity_period:<10} | Badge: {badge}")
            participant.base_score = participant.total_score

        print("=" * 50)  # Separator between events

# Initialize participants once
participants = [
    Participant(name="Osama", base_score=0),
    Participant(name="Iman", base_score=250),
    Participant(name="Ayoub", base_score=601),
    Participant(name="Bisma", base_score=750),
    Participant(name="Fatima", base_score=1000)
]

# Test different event sizes with continuous event numbering
event_sizes = [50, 100, 150, 200, 250]
current_event_number = 1
for event_size in event_sizes:
    simulate_events(4, event_size, participants, current_event_number)
    current_event_number += 4  # Increment by 2 since we're running 2 events each time

