import random

from sim1 import VolunteerMetrics
from Event import Event
random.seed(1)
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

        # Apply inactivity decay if inactivity_period > 3, with different rates per rank
        if self.inactivity_period >= 3:
            decay_rates = {
                "Platinum": 0.10,  # 10% decay
                "Gold": 0.07,      # 7% decay
                "Silver": 0.05,    # 5% decay
                "Bronze": 0.03     # 3% decay
            }
            
            if self.rank in decay_rates:
                print(f"Total Score before decay for {self.name}: {total_score_before_decay:.2f}")
                inactivity_decay = total_score_before_decay * decay_rates[self.rank]
                total_score_before_decay -= inactivity_decay
                print(f"Decay applied for inactivity to {self.name} ({self.rank}): -{inactivity_decay:.2f}")
                self.inactivity_period = 0  # Reset inactivity only when decay is applied
                
        # Set the total score after decay
        self.total_score = total_score_before_decay

def apply_reset(list_participants,rank_distribution): #this will apply the reset for all classes
    plat=rank_distribution[0]
    gold=rank_distribution[1]
    silver=rank_distribution[2]
    for participant in list_participants:
        if participant.base_score>=plat: #will change this to be if they are above platinum they will be reset to platinum
            participant.base_score=plat
        elif participant.base_score>=gold:
            participant.base_score-=100 #demote them by 2 tiers
            #print("In gold:\t"+participant.name+"\t"+str(participant.base_score))
        elif participant.base_score>=silver:
            participant.base_score-=50 #demote by 1 tier
            #print("In silver:\t"+participant.name+"\t"+str(participant.base_score))
        else:
            participant.base_score-=20 #demote by a small amount because they are already doing bad
            #print("In bronze:\t"+participant.name+"\t"+str(participant.base_score))


def prepare_distributed_reset(event_sizes):
    return 5,distrubte_events_across_seasons(event_sizes, 5),0 # default values for the number of seasons, current season, list of the season,counter

def distrubte_events_across_seasons(num_of_events,num_of_seasons):
    counter=0
    while True: 
        event_assignment=[]
        for i in range(num_of_seasons):
            num_of_event=random.randint(1,num_of_events) #generate a random number of events
            event_assignment.append(num_of_event) # append that number
        if sum(event_assignment)==num_of_events: # make sure that my generated number of event is equal to all_events
            break
        counter+=1
        if counter==2000: #safeguard
            print("out")
            break
    return event_assignment

def simulate_events(num_events, event_size, participants, start_event_number, thresholds):
   
    print(f"\nSimulating with Event Size: {event_size}")
    print("=" * 80)
    for event_number in range(start_event_number, start_event_number + num_events):
        
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

            

            # Different inactivity patterns for each participant
            if participant.name == "Ayoub" and event_number <= 6:  # Inactive for first 5 events
                participant.inactivity_period += 1
            elif participant.name == "Iman" and 7 <= event_number <= 9:  # Inactive during events 7-9
                participant.inactivity_period += 1
            elif participant.name == "Bisma" and event_number % 3 == 0:  # Inactive every 3rd event
                participant.inactivity_period += 1
            elif participant.name == "Fatima" and event_number >= 8:  # Inactive for last few events
                participant.inactivity_period += 1
            else:
                participant.inactivity_period = 0
           
            participant.calculate_event_score(event_size)  # Use the given event size for score calculation

            # Apply decay before updating final total score
           
            # Calculate the real metrics_score but display 0 if inactive
            display_metrics_score = 0 if participant.inactivity_period >= 1 else participant.metrics_score
             
            participant.apply_decay()
            

            participant.determine_rank(thresholds)

            
            badge = participant.award_badge()
            inactivity_display = f"{participant.inactivity_period} months" if participant.inactivity_period > 0 else "Active"
            
            # Use display_metrics_score for printing
            print(f"{participant.name:<10} | {participant.base_score:<10.1f} | {display_metrics_score:<15.2f} | {participant.event_score:<15.2f} | {participant.total_score:<15.1f} | {participant.rank:<6} | {participant.inactivity_period:<10} | Badge: {badge}")
            participant.base_score = participant.total_score

        print("=" * 50)  # Separator between events


switch_between_reset_modes=True # changing the reset methods used below
# Initialize participants once
participants = [
    Participant(name="Osama", base_score=0),
    Participant(name="Iman", base_score=250),
    Participant(name="Ayoub", base_score=601),
    Participant(name="Bisma", base_score=750),
    Participant(name="Fatima", base_score=1000)
]

THRESHOLDS = {
    "standard": [1000, 800, 600, 400],
    "competitive": [1500, 900, 700, 500],
    "strict": [2000, 900, 600, 200]
}

# Initialize original base scores
INITIAL_BASE_SCORES = {
    "Osama": 0,
    "Iman": 250,
    "Ayoub": 601,
    "Bisma": 750,
    "Fatima": 1000
}

# Test different event sizes with continuous event numbering
event_sizes = [50, 100, 150, 200, 250] * 4  # Multiply by 4 to get 20 events total

# First simulation with standard thresholds
current_event_number = 1
shuffled_sizes = event_sizes.copy()
random.shuffle(shuffled_sizes)
print(f"\nUsing standard thresholds: {THRESHOLDS['standard']}")
print(f"Shuffled event sizes: {shuffled_sizes}")
number_of_seasons,event_distribution,counter = prepare_distributed_reset(len(event_sizes)) # this is reseting the values, or setting them
breakpoint = event_distribution[counter]
if switch_between_reset_modes:
    print(event_distribution)
print("Season", counter+1)
print("#" * 90)     
for event_size in shuffled_sizes:
    if not switch_between_reset_modes:
        if (current_event_number)==((((counter+1)*len(event_sizes))//number_of_seasons)+1): # this is the case of evenly distributed events accross seasons
            apply_reset(participants,THRESHOLDS["standard"])
            counter+=1
            print("Season",counter+1)
            print("#"*90)
    simulate_events(1, event_size, participants, current_event_number, THRESHOLDS["standard"])
    if switch_between_reset_modes:
        if (current_event_number) == breakpoint:
                
                apply_reset(participants,THRESHOLDS["standard"])
                counter += 1
                try:
                    breakpoint += event_distribution[counter] # this avoids an issue that accurs in the last event
                    print("Season", counter+1)
                    print("#" * 90)
                except:
                    pass
        
    current_event_number += 1
# Reset participants for competitive thresholds
for participant in participants:
    participant.base_score = INITIAL_BASE_SCORES[participant.name]
    participant.total_score = participant.base_score
    participant.inactivity_period = 0

current_event_number = 1
shuffled_sizes = event_sizes.copy()
random.shuffle(shuffled_sizes)
print(f"\nUsing competitive thresholds: {THRESHOLDS['competitive']}")
print(f"Shuffled event sizes: {shuffled_sizes}")
number_of_seasons,event_distribution,counter = prepare_distributed_reset(len(event_sizes)) # this is reseting the values, or setting them
breakpoint = event_distribution[counter]
if switch_between_reset_modes:
    print(event_distribution)
counter=0
for event_size in shuffled_sizes:
    if not switch_between_reset_modes:
        if (current_event_number)==((((counter+1)*len(event_sizes))//number_of_seasons)+1): # this is the case of evenly distributed events accross seasons
            apply_reset(participants,THRESHOLDS["competitive"])
            counter+=1
            print("Season",counter+1)
            print("#"*90)
    simulate_events(1, event_size, participants, current_event_number, THRESHOLDS["competitive"])
    if switch_between_reset_modes:
        if (current_event_number) == breakpoint:
                
                apply_reset(participants,THRESHOLDS["competitive"])
                counter += 1
                try:
                    breakpoint += event_distribution[counter] # this avoids an issue that accurs in the last event
                    print("Season", counter+1)
                    print("#" * 90)
                except:
                    pass
    current_event_number += 1
# Reset participants for strict thresholds
for participant in participants:
    participant.base_score = INITIAL_BASE_SCORES[participant.name]
    participant.total_score = participant.base_score
    participant.inactivity_period = 0

current_event_number = 1
shuffled_sizes = event_sizes.copy()
random.shuffle(shuffled_sizes)
print(f"\nUsing strict thresholds: {THRESHOLDS['strict']}")
print(f"Shuffled event sizes: {shuffled_sizes}")
number_of_seasons,event_distribution,counter = prepare_distributed_reset(len(event_sizes)) # this is reseting the values, or setting them
breakpoint = event_distribution[counter]
if switch_between_reset_modes:
    print(event_distribution)
print("Season", counter+1)
print("#" * 90) 
for event_size in shuffled_sizes:
    if not switch_between_reset_modes:
        if (current_event_number)==((((counter+1)*len(event_sizes))//number_of_seasons)+1): # this is the case of evenly distributed events accross seasons
            apply_reset(participants,THRESHOLDS["strict"])
            counter+=1
            print("Season",counter+1)
            print("#"*90)
    simulate_events(1, event_size, participants, current_event_number, THRESHOLDS["strict"])
    if switch_between_reset_modes:
        if (current_event_number) == breakpoint:
                
                apply_reset(participants,THRESHOLDS["strict"])
                counter += 1
                try:
                    breakpoint += event_distribution[counter] # this avoids an issue that accurs in the last event
                    print("Season", counter+1)
                    print("#" * 90)
                except:
                    pass
    current_event_number += 1
