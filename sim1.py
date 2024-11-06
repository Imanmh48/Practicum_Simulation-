import random
from datetime import datetime, timedelta

class VolunteerMetrics:
    @staticmethod
    def calculate_response_time(response_time_minutes):
        """Calculate points for response time (0-10, lower time is better)"""
        if response_time_minutes <= 30:
            return 10
        elif response_time_minutes <= 60:
            return 7
        elif response_time_minutes <= 120:
            return 4
        else:
            return max(0, 10 - (response_time_minutes / 30))

    @staticmethod
    def calculate_attendance(late_arrivals, early_departures, unscheduled_absences, total_shifts):
        """Calculate overall attendance score (0-10)"""
        late_points = max(0, 10 - (late_arrivals / total_shifts * 10))
        early_points = max(0, 10 - (early_departures / total_shifts * 10))
        absence_points = max(0, 10 - (unscheduled_absences / total_shifts * 10))
        return (late_points + early_points + absence_points) / 3

    @staticmethod
    def calculate_task_completion(completed_tasks, total_tasks):
        """Calculate task completion rate (0-10)"""
        if total_tasks == 0:
            return 0
        return (completed_tasks / total_tasks) * 10

    @staticmethod
    def calculate_hours_commitment(logged_hours, expected_hours):
        """Calculate commitment based on hours (0-10)"""
        if expected_hours == 0:
            return 0
        return min(10, (logged_hours / expected_hours) * 10)

    @staticmethod
    def calculate_team_performance(team_completed_tasks, team_total_tasks, 
                                 actual_completion_time, planned_time):
        """Calculate overall team performance (0-10)"""
        if team_total_tasks == 0 or actual_completion_time == 0:
            return 0
        task_completion = (team_completed_tasks / team_total_tasks) * 10
        time_efficiency = (planned_time / actual_completion_time) * 10
        return (task_completion + time_efficiency) / 2

    @staticmethod
    def calculate_problem_solving(time_taken, expected_time, 
                                successful_solutions, total_solutions):
        """Calculate problem-solving score (0-10)"""
        if expected_time == 0 or total_solutions == 0:
            return 0
        time_efficiency = (expected_time / time_taken) * 10
        success_rate = (successful_solutions / total_solutions) * 10
        return (time_efficiency + success_rate) / 2

    @staticmethod
    def calculate_conflict_resolution(conflicts_resolved, total_conflicts):
        """Calculate conflict resolution score (0-10)"""
        if total_conflicts == 0:
            return 0
        return (conflicts_resolved / total_conflicts) * 10

    @staticmethod 
    def calculate_leadership_metrics(team_completed_tasks, team_total_tasks,
                                   leadership_appointments):
        """Calculate leadership metrics score (0-10)"""
        if team_total_tasks == 0:
            return 0
        leadership_score = (team_completed_tasks / team_total_tasks) * 10
        leadership_appointment_score = min(10, leadership_appointments * 2)  # Assuming each appointment is worth 2 points
        return (leadership_score + leadership_appointment_score) / 2

def run_simulation(num_volunteers=10):
    final_results = []
    new_scores_list = []
    
    # Create initial values for each volunteer
    initial_values = {}
    for i in range(num_volunteers):
        initial_values[f'V{i+1:03d}'] = {
            'response_time': random.uniform(5.0, 10.0),
            'attendance': random.uniform(5.0, 10.0),
            'task_completion': random.uniform(5.0, 10.0),
            'hours_commitment': random.uniform(5.0, 10.0)
        }
    
    for i in range(num_volunteers):
        volunteer_id = f'V{i+1:03d}'
        
        # Simulate random metrics for each volunteer
        response_time = random.randint(15, 180)
        late_arrivals = random.randint(0, 5)
        early_departures = random.randint(0, 5)
        unscheduled_absences = random.randint(0, 3)
        completed_tasks = random.randint(20, 30)
        total_tasks = 30
        logged_hours = random.randint(40, 60)
        expected_hours = 50
        
        # Calculate new scores
        new_scores = {
            'volunteer_id': volunteer_id,
            'response_time': VolunteerMetrics.calculate_response_time(response_time),
            'attendance': VolunteerMetrics.calculate_attendance(late_arrivals, early_departures, unscheduled_absences,5),
            'task_completion': VolunteerMetrics.calculate_task_completion(completed_tasks, total_tasks),
            'hours_commitment': VolunteerMetrics.calculate_hours_commitment(logged_hours, expected_hours)
        }
        new_scores_list.append(new_scores)
        
        # Calculate average between initial and new scores
        final_scores = {
            'volunteer_id': volunteer_id,
            'response_time': (initial_values[volunteer_id]['response_time'] + new_scores['response_time']) / 2,
            'attendance': (initial_values[volunteer_id]['attendance'] + new_scores['attendance']) / 2,
            'task_completion': (initial_values[volunteer_id]['task_completion'] + new_scores['task_completion']) / 2,
            'hours_commitment': (initial_values[volunteer_id]['hours_commitment'] + new_scores['hours_commitment']) / 2
        }
        
        # Calculate final average score
        final_scores['average'] = sum(v for k, v in final_scores.items() if k != 'volunteer_id') / 5
        final_results.append(final_scores)
    
    return final_results, initial_values, new_scores_list

# Run simulation and display results
simulation_results, initial_values, new_scores_list = run_simulation(5)

# Display Initial Values
print("\nInitial Values:")
print("-" * 80)
print(f"{'ID':<8} {'Response':<10} {'Attend':<10} {'Tasks':<10} {'Hours':<10}")
print("-" * 80)
for vol_id, values in initial_values.items():
    print(f"{vol_id:<8} "
          f"{values['response_time']:<10.1f} "
          f"{values['attendance']:<10.1f} "
          f"{values['task_completion']:<10.1f} "
          f"{values['hours_commitment']:<10.1f}")

# Display New Values (from current simulation)
print("\nNew Values:")
print("-" * 80)
print(f"{'ID':<8} {'Response':<10} {'Attend':<10} {'Tasks':<10} {'Hours':<10}")
print("-" * 80)
for result in new_scores_list:
    vol_id = result['volunteer_id']
    print(f"{vol_id:<8} "
          f"{result['response_time']:<10.1f} "
          f"{result['attendance']:<10.1f} "
          f"{result['task_completion']:<10.1f} "
          f"{result['hours_commitment']:<10.1f}")

# Display Final Results (averages)
print("\nFinal Results (Average of Initial and New Values):")
print("-" * 80)
print(f"{'ID':<8} {'Response':<10} {'Attend':<10} {'Tasks':<10} {'Hours':<10} {'Avg':<10}")
print("-" * 80)
for result in simulation_results:
    print(f"{result['volunteer_id']:<8} "
          f"{result['response_time']:<10.1f} "
          f"{result['attendance']:<10.1f} "
          f"{result['task_completion']:<10.1f} "
          f"{result['hours_commitment']:<10.1f} "
          f"{result['average']:<10.1f}") 