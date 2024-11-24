import random
import math
from sim1 import VolunteerMetrics
from Event import Event
from config import *

#random.seed(1)
class Participant:
    def __init__(self, name, base_score, personality):
        self.name = name
        self.base_score = base_score

        self.response_time = 0
        self.attendance_rate = 0
        self.task_completion_rate = 0
        self.response_time = 0
        self.attendance_rate = 0
        self.task_completion_rate = 0

        self.event_score = 0
        self.metrics_score = 0  # The current position of the participant in the metrics

        self.hours_commitment = 0
        self.team_performance = 0
        self.problem_solving = 0
        self.conflict_resolution = 0
        self.leadership_metrics = 0
        self.leadership_appointments = 0
        self.hours_commitment = 0
        self.team_performance = 0
        self.problem_solving = 0
        self.conflict_resolution = 0
        self.leadership_metrics = 0
        self.leadership_appointments = 0

        self.total_score = base_score
        self.rank = ""
        self.inactivity_period = 0
        self.personality = personality
        self.personality = personality

    def calculate_event_score(self, event_size):
        # If participant is inactive, event_score is 0
        if self.inactivity_period >= 1:
            self.event_score = 0
            return

        # Ensure minimum event size
        if event_size < 10:
            raise ValueError(f"Event size cannot be less than 10 (got {event_size})")

        # Direct threshold checks from largest to smallest
        if event_size >= 200:
            self.event_score = 50
        elif event_size >= 100:
            self.event_score = 100
        elif event_size >= 50:
            self.event_score = 150
        else:  # event_size <= 50
            self.event_score = 200

    def update_metrics_score(self, event,
                             response_time,
                             late_arrivals,
                             completed_tasks,
                             successful_solutions,
                             conflicts_resolved):
        """Update metrics score based on event's metrics weights and provided metric values"""
        new_response_time = response_time
        new_attendance = late_arrivals
        new_task_completion = completed_tasks
        new_conflict = conflicts_resolved

        # Update metrics by averaging with previous values
        self.response_time = (self.response_time + new_response_time) / 2
        self.attendance_rate = (self.attendance_rate + new_attendance) / 2
        self.task_completion_rate = (self.task_completion_rate + new_task_completion) / 2
        self.conflict_resolution = (self.conflict_resolution + new_conflict) / 2

        # Calculate the final metrics score
        new_metric = round((
            self.response_time +
            self.task_completion_rate +
            self.conflict_resolution +
            self.attendance_rate
        ), 2) / 4

        if new_metric > 10:
            new_metric = 10
        self.metrics_score = new_metric

    def determine_rank(self, thresholds):
        if self.total_score >= thresholds[0] and self.metrics_score >= PLATINUM_METRICS_THRESHOLD:
            self.rank = 'Platinum'
        elif self.total_score >= thresholds[1]:
            self.rank = 'Gold'
        elif self.total_score >= thresholds[2]:
            self.rank = 'Silver'
        elif self.total_score >= thresholds[3]:
            self.rank = 'Bronze'
        else:
            self.rank = 'Bronze'

    def apply_decay(self, inactivity_threshold=2):
        previous_metrics = getattr(self, '_previous_metrics_score', self.metrics_score)
        if self.inactivity_period >= 1 or (hasattr(self, '_previous_metrics_score') and 
                                           (previous_metrics - self.metrics_score) > METRICS_DECLINE_THRESHOLD):
            current_total = self.total_score
        else:
            metrics_modifier = 1 + (self.metrics_score / 50)
            base_value = 100 if self.base_score == 0 else self.base_score
            current_total = (base_value + self.event_score) * metrics_modifier

        total_score_before_decay = current_total
        metrics_modifier = 1 + (self.metrics_score / 50)
        base_value = 100 if self.base_score == 0 else self.base_score
        current_total = (base_value + self.event_score) * metrics_modifier

        total_score_before_decay = current_total

        # Apply inactivity decay
        if self.inactivity_period == inactivity_threshold:
            if self.rank in DECAY_RATES:
                inactivity_decay = total_score_before_decay * DECAY_RATES[self.rank]
                total_score_before_decay -= inactivity_decay
                self.inactivity_period = 0

        # Apply metrics decline decay
        original_score = total_score_before_decay
        if (previous_metrics - self.metrics_score) > METRICS_DECLINE_THRESHOLD:
            metrics_decay = original_score * METRICS_DECLINE_DECAY_RATE
            total_score_before_decay -= metrics_decay

        self._previous_metrics_score = self.metrics_score
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
        print(f"{'Name':<10} | {'Base Score':<10} | {'Metrics_Score':<15} | {'Event Score':<15} | {'Personality':<12} | {'Total Score':<15} | {'Rank':<6} | {'Inactivity':<10}")
        print("-" * 92)

        for participant in participants:
            previous_total = participant.total_score
            participant_number = int(participant.name[1:])

            # Ensure varied randomization
            random.seed(event_number + participant_number)

            # Generate varied random values
            if participant.personality == "lazy":
                response_time = random.randint(1, 3)
                late_arrivals = random.randint(1, 3)
                completed_tasks = random.randint(1, 4)
                successful_solutions = random.randint(1, 4)
                conflicts_resolved = random.randint(1, 4)
            elif participant.personality == "ideal":
                response_time = random.randint(9, 11)
                late_arrivals = random.randint(9, 11)
                completed_tasks = random.randint(9, 11)
                successful_solutions = random.randint(9, 11)
                conflicts_resolved = random.randint(9, 11)
            elif participant.personality == "inconsistent":
                response_time = random.randint(5, 11)
                late_arrivals = random.randint(5, 11)
                completed_tasks = random.randint(5, 11)
                successful_solutions = random.randint(5, 11)
                conflicts_resolved = random.randint(5, 11)
            elif participant.personality == "growing":
                response_time = random.randint(max(1, round(participant.response_time)), 11)
                late_arrivals = random.randint(max(1, round(participant.attendance_rate)), 11)
                completed_tasks = random.randint(max(1, round(participant.task_completion_rate)), 11)
                successful_solutions = random.randint(max(1, round(participant.task_completion_rate)), 11)
                conflicts_resolved = random.randint(max(1, round(participant.conflict_resolution)), 11)
                print(f"[DEBUG] Growing participant {participant.name}: Response Time {response_time}, Attendance {late_arrivals}, Task Completion {completed_tasks}")
            elif participant.personality == "average":
                response_time = random.randint(4, 8)
                late_arrivals = random.randint(4, 8)
                completed_tasks = random.randint(4, 8)
                successful_solutions = random.randint(4, 8)
                conflicts_resolved = random.randint(4, 8)

            # Update metrics if participant is active
            if participant.inactivity_period == 0:
                participant.update_metrics_score(
                    None, response_time, late_arrivals, completed_tasks, 
                    successful_solutions, conflicts_resolved
                )

            # Calculate scores and determine ranks
            participant.calculate_event_score(event_size)
            participant.determine_rank(thresholds)
            participant.apply_decay(inactivity_threshold=inactivity_threshold)
            participant.determine_rank(thresholds)

            # Store the updated base score
            participant.base_score = previous_total

            # Print participant details
            inactivity_display = f"{participant.inactivity_period} months" if participant.inactivity_period > 0 else "Active"
            print(f"{participant.name:<10} | {participant.base_score:<10.1f} | {participant.metrics_score:<15.2f} | {participant.event_score:<15.2f} | {participant.personality:<12} | {participant.total_score:<15.1f} | {participant.rank:<6} | {inactivity_display:<10}")

        print("=" * 50)

switch_between_reset_modes=True # changing the reset methods used below
participants = []
personality_counter = 0
skip = NUMBER_OF_VOLUNTEERS//len(PERSONALITIES)
leftovers = NUMBER_OF_VOLUNTEERS%len(PERSONALITIES)
for batch in range(0,NUMBER_OF_VOLUNTEERS,skip): 
    if personality_counter<len(PERSONALITIES):
        for v in range(batch,batch+skip):
            participants.append(Participant("v"+str(v+1),INITIAL_BASE_SCORES["v"+str(v+1)],PERSONALITIES[personality_counter]))
        personality_counter+=1

if leftovers!=0:
    for leftover in range(leftovers):
        v+=1
        participants.append(Participant("v"+str(v+1),INITIAL_BASE_SCORES["v"+str(v+1)],PERSONALITIES[leftover]))



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
