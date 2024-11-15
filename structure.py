import random

from sim1 import VolunteerMetrics
from Event import Event
from config import NUMBER_OF_SEASONS, THRESHOLDS , INACTIVITY_THRESHOLDS, DECAY_RATES, INITIAL_BASE_SCORES, EVENT_SIZES, METRICS_DECLINE_THRESHOLD, METRICS_DECLINE_DECAY_RATE
#random.seed(1)
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
        # Add a maximum score cap for each rank
        if self.total_score >= thresholds[0]:
            if self.total_score > thresholds[0] * 1.5:  # Cap Platinum growth
                self.total_score = thresholds[0] * 1.5
            self.rank = 'Platinum'
        elif self.total_score >= thresholds[1]:
            if self.total_score > thresholds[0] * 0.95:  # Cap Gold near Platinum threshold
                self.total_score = thresholds[0] * 0.95
            self.rank = 'Gold'
        elif self.total_score >= thresholds[2]:
            if self.total_score > thresholds[1] * 0.95:  # Cap Silver near Gold threshold
                self.total_score = thresholds[1] * 0.95
            self.rank = 'Silver'
        elif self.total_score >= thresholds[3]:
            if self.total_score > thresholds[2] * 0.95:  # Cap Bronze near Silver threshold
                self.total_score = thresholds[2] * 0.95
            self.rank = 'Bronze'
        else:
            self.rank = 'Bronze'
    

    def apply_decay(self, inactivity_threshold=3):
        # Store the initial calculation before any decay
        if self.inactivity_period >= 1:
            total_score_before_decay = self.base_score + self.event_score
        else:
            # Reduce the metrics modifier impact
            metrics_modifier = 1 + (self.metrics_score / 100)  # Changed from 50 to 100 - now 1% to 10% increase
            
            if self.base_score == 0:
                base_value = 100
            else:
                base_value = self.base_score
            
            total_score_before_decay = (base_value + self.event_score) * metrics_modifier

        # Increase decay rates for higher ranks
        if self.inactivity_period >= inactivity_threshold:
            if self.rank in DECAY_RATES:
                decay_multiplier = 1.5 if self.rank in ['Platinum', 'Gold'] else 1.0  # Higher ranks decay faster
                inactivity_decay = total_score_before_decay * (DECAY_RATES[self.rank] * decay_multiplier)
                total_score_before_decay -= inactivity_decay
                print(f"Decay applied for inactivity to {self.name} ({self.rank}): -{inactivity_decay:.2f}")
        
        # Apply metrics decline decay
        previous_metrics = getattr(self, '_previous_metrics_score', self.metrics_score)
        if hasattr(self, '_previous_metrics_score') and (previous_metrics - self.metrics_score) > METRICS_DECLINE_THRESHOLD:
            print(f"Total Score before decay: {total_score_before_decay:.2f}")
            metrics_decay = total_score_before_decay * METRICS_DECLINE_DECAY_RATE
            total_score_before_decay -= metrics_decay
            print(f"Decay applied for metrics decline to {self.name}: -{metrics_decay:.2f} (Metrics dropped from {previous_metrics:.2f} to {self.metrics_score:.2f})")
        
        # Store current metrics score for next comparison
        self._previous_metrics_score = self.metrics_score
        
        # Set the total score after all decays
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
    return NUMBER_OF_SEASONS, distrubte_events_across_seasons(event_sizes, NUMBER_OF_SEASONS), 0

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

def simulate_events(num_events, event_size, participants, start_event_number, thresholds, inactivity_threshold=3):
    print(f"\nSimulating with Event Size: {event_size}")
    print("=" * 80)
    for event_number in range(start_event_number, start_event_number + num_events):
        
        print(f"\nEvent {event_number} (Event Size: {event_size}):")
        print("=" * 50)
        print(f"{'Name':<10} | {'Base Score':<10} | {'Metrics_Score':<15} | {'Event Score':<15} | {'Total Score':<15} | {'Rank':<6} | {'Inactivity':<10}")
        print("-" * 92)

        for participant in participants:
            # Store the previous total score before calculating new scores
            previous_total = participant.total_score
            
            event = Event("Test Event", event_size, "2024-01-01", "standard")
            
            # Track inactivity without resetting
            was_inactive = False
            if (participant.name == "Ayoub" and event_number < 6) or \
               (participant.name == "Iman" and 7 <= event_number <= 9) or \
               (participant.name == "Bisma" and event_number % 3 == 0) or \
               (participant.name == "Fatima" and 12 <= event_number <= 16):  # Now inactive only between events 12-16
                participant.inactivity_period += 1
                was_inactive = True
            else:
                participant.inactivity_period = 0

            event = Event("Test Event", event_size, "2024-01-01", "standard")
            
            # Generate much more varied random values for each participant
            if participant.name == "Osama":
                # More extreme variations for Osama
                if event_number % 2 == 0:  # Every other event
                    response_time = random.randint(5, 15)        # Excellent response time
                    late_arrivals = 0                           # No late arrivals
                    completed_tasks = random.randint(9, 10)      # Nearly perfect completion
                    team_completed = random.randint(9, 10)       # Excellent team performance
                    successful_solutions = random.randint(9, 10)  # Excellent problem solving
                    conflicts_resolved = random.randint(9, 10)   # Excellent conflict resolution
                else:
                    response_time = random.randint(80, 120)      # Very poor response time
                    late_arrivals = random.randint(3, 5)        # Many late arrivals
                    completed_tasks = random.randint(1, 3)       # Very poor completion
                    team_completed = random.randint(1, 3)        # Very poor team performance
                    successful_solutions = random.randint(1, 3)   # Very poor problem solving
                    conflicts_resolved = random.randint(1, 3)    # Very poor conflict resolution
                
            elif participant.name == "Iman":
                # Even more dramatic swings for Iman
                if event_number % 3 == 0:  # Every third event
                    response_time = random.randint(5, 10)
                    late_arrivals = 0
                    completed_tasks = 10
                    team_completed = 10
                    successful_solutions = 10
                    conflicts_resolved = 10
                else:
                    response_time = random.randint(90, 120)
                    late_arrivals = random.randint(4, 5)
                    completed_tasks = random.randint(0, 2)
                    team_completed = random.randint(0, 2)
                    successful_solutions = random.randint(0, 2)
                    conflicts_resolved = random.randint(0, 2)
            elif participant.name == "Ayoub":
                if event_number % 4 == 0:  # Every 4th event
                    response_time = random.randint(80, 120)      # Poor response
                    late_arrivals = random.randint(3, 5)         # Many issues
                    completed_tasks = random.randint(1, 4)       # Poor completion
                    team_completed = random.randint(1, 4)        # Poor team performance
                    successful_solutions = random.randint(1, 4)   # Poor solutions
                    conflicts_resolved = random.randint(1, 4)    # Poor conflict resolution
                else:
                    response_time = random.randint(20, 45)       # Average response
                    late_arrivals = random.randint(0, 2)         # Occasional issues
                    completed_tasks = random.randint(4, 8)       # Average completion
                    team_completed = random.randint(4, 8)        # Average team performance
                    successful_solutions = random.randint(4, 7)   # Average solutions
                    conflicts_resolved = random.randint(4, 7)    # Average conflict resolution
            elif participant.name == "Bisma":
                if event_number % 3 == 0:  # Every 3rd event
                    response_time = random.randint(90, 120)      # Very poor response
                    late_arrivals = random.randint(3, 5)         # Many issues
                    completed_tasks = random.randint(1, 3)       # Poor completion
                    team_completed = random.randint(1, 3)        # Poor team performance
                    successful_solutions = random.randint(1, 3)   # Poor problem solving
                    conflicts_resolved = random.randint(1, 3)    # Poor conflict resolution
                else:
                    response_time = random.randint(10, 30)       # Good response
                    late_arrivals = random.randint(0, 1)         # Rare issues
                    completed_tasks = random.randint(6, 9)       # Good completion
                    team_completed = random.randint(6, 9)        # Good team performance
                    successful_solutions = random.randint(6, 9)   # Good problem solving
                    conflicts_resolved = random.randint(6, 9)    # Good conflict resolution
            else:  # Fatima
                if event_number % 5 == 0:  # Every 5th event
                    response_time = random.randint(70, 100)     # Poor performance
                    late_arrivals = random.randint(2, 4)        # Multiple issues
                    completed_tasks = random.randint(2, 5)      # Below average
                else:
                    response_time = random.randint(5, 35)       # Usually excellent
                    late_arrivals = random.randint(0, 1)        # Very rarely late
                    completed_tasks = random.randint(6, 10)     # Generally good

            # More variable common random values
            early_departures = random.randint(0, 2)
            unscheduled_absences = random.randint(0, 2)
            total_tasks = 10
            logged_hours = random.randint(25, 40)          # More variable hours
            expected_hours = 40
            team_total = 10
            actual_time = random.randint(25, 40)           # More variable time management
            planned_time = 40
            problem_time = random.randint(25, 40)          # More variable problem solving
            expected_problem_time = 40
            total_solutions = 10
            total_conflicts = 10
            
            # Only update metrics if participant is active
            if not was_inactive:
                participant.update_metrics_score(
                    event=event,
                    response_time_mins=response_time,
                    late_arrivals=late_arrivals,
                    early_departures=early_departures,
                    unscheduled_absences=unscheduled_absences,
                    completed_tasks=completed_tasks,
                    total_tasks=total_tasks,
                    logged_hours=logged_hours,
                    expected_hours=expected_hours,
                    team_completed=team_completed,
                    team_total=team_total,
                    actual_time=actual_time,
                    planned_time=planned_time,
                    problem_time=problem_time,
                    expected_problem_time=expected_problem_time,
                    successful_solutions=successful_solutions,
                    total_solutions=total_solutions,
                    conflicts_resolved=conflicts_resolved,
                    total_conflicts=total_conflicts
                )
            
            participant.calculate_event_score(event_size)
            participant.apply_decay(inactivity_threshold=inactivity_threshold)
            participant.determine_rank(thresholds)
            
            # Update base_score to previous event's total score
            participant.base_score = previous_total

            inactivity_display = f"{participant.inactivity_period} months" if participant.inactivity_period > 0 else "Active"
            
            print(f"{participant.name:<10} | {participant.base_score:<10.1f} | {participant.metrics_score:<15.2f} | {participant.event_score:<15.2f} | {participant.total_score:<15.1f} | {participant.rank:<6} | {participant.inactivity_period:<10}")

        print("=" * 50)


switch_between_reset_modes=True # changing the reset methods used below
# Initialize participants once
participants = [
    Participant(name="Osama", base_score=INITIAL_BASE_SCORES["Osama"]),
    Participant(name="Iman", base_score=INITIAL_BASE_SCORES["Iman"]),
    Participant(name="Ayoub", base_score=INITIAL_BASE_SCORES["Ayoub"]),
    Participant(name="Bisma", base_score=INITIAL_BASE_SCORES["Bisma"]),
    Participant(name="Fatima", base_score=INITIAL_BASE_SCORES["Fatima"])
]

# Test different event sizes with continuous event numbering
shuffled_sizes = EVENT_SIZES.copy()



for inactivity_threshold in INACTIVITY_THRESHOLDS:
    print(f"\n\n{'='*50}")
    print(f"TESTING WITH INACTIVITY THRESHOLD = {inactivity_threshold}")
    print(f"{'='*50}\n")

    # Reset participants for new threshold test
    for participant in participants:
        participant.base_score = INITIAL_BASE_SCORES[participant.name]
        participant.total_score = participant.base_score
        participant.inactivity_period = 0

    # First simulation with standard thresholds
    current_event_number = 1
    shuffled_sizes = EVENT_SIZES.copy()
    random.shuffle(shuffled_sizes)
    print(f"\nUsing standard thresholds: {THRESHOLDS['standard']}")
    print(f"Shuffled event sizes: {shuffled_sizes}")
    number_of_seasons,event_distribution,counter = prepare_distributed_reset(len(EVENT_SIZES))
    breakpoint = event_distribution[counter]
    if switch_between_reset_modes:
        print(event_distribution)
    print("Season", counter+1)
    print("#" * 90)     
    for event_size in shuffled_sizes:
        if not switch_between_reset_modes:
            if (current_event_number)==((((counter+1)*len(EVENT_SIZES))//number_of_seasons)+1):
                apply_reset(participants,THRESHOLDS["standard"])
                counter+=1
                print("Season",counter+1)
                print("#"*90)
        simulate_events(1, event_size, participants, current_event_number, THRESHOLDS["standard"], inactivity_threshold)
        if switch_between_reset_modes:
            if (current_event_number) == breakpoint:
                apply_reset(participants,THRESHOLDS["standard"])
                counter += 1
                try:
                    breakpoint += event_distribution[counter]
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
    shuffled_sizes = EVENT_SIZES.copy()
    random.shuffle(shuffled_sizes)
    print(f"\nUsing competitive thresholds: {THRESHOLDS['competitive']}")
    print(f"Shuffled event sizes: {shuffled_sizes}")
    number_of_seasons,event_distribution,counter = prepare_distributed_reset(len(EVENT_SIZES))
    breakpoint = event_distribution[counter]
    if switch_between_reset_modes:
        print(event_distribution)
    counter=0
    for event_size in shuffled_sizes:
        if not switch_between_reset_modes:
            if (current_event_number)==((((counter+1)*len(EVENT_SIZES))//number_of_seasons)+1):
                apply_reset(participants,THRESHOLDS["competitive"])
                counter+=1
                print("Season",counter+1)
                print("#"*90)
        simulate_events(1, event_size, participants, current_event_number, THRESHOLDS["competitive"], inactivity_threshold)
        if switch_between_reset_modes:
            if (current_event_number) == breakpoint:
                apply_reset(participants,THRESHOLDS["competitive"])
                counter += 1
                try:
                    breakpoint += event_distribution[counter]
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
    shuffled_sizes = EVENT_SIZES.copy()
    random.shuffle(shuffled_sizes)
    print(f"\nUsing strict thresholds: {THRESHOLDS['strict']}")
    print(f"Shuffled event sizes: {shuffled_sizes}")
    number_of_seasons,event_distribution,counter = prepare_distributed_reset(len(EVENT_SIZES))
    breakpoint = event_distribution[counter]
    if switch_between_reset_modes:
        print(event_distribution)
    print("Season", counter+1)
    print("#" * 90)
    for event_size in shuffled_sizes:
        if not switch_between_reset_modes:
            if (current_event_number)==((((counter+1)*len(EVENT_SIZES))//number_of_seasons)+1):
                apply_reset(participants,THRESHOLDS["strict"])
                counter+=1
                print("Season",counter+1)
                print("#"*90)
        simulate_events(1, event_size, participants, current_event_number, THRESHOLDS["strict"], inactivity_threshold)
        if switch_between_reset_modes:
            if (current_event_number) == breakpoint:
                apply_reset(participants,THRESHOLDS["strict"])
                counter += 1
                try:
                    breakpoint += event_distribution[counter]
                    print("Season", counter+1)
                    print("#" * 90)
                except:
                    pass
        current_event_number += 1
