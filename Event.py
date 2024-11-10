class Event:
    # Define standard weight profiles as class attributes
    STANDARD_WEIGHTS = {
        'response_time': 0.15,
        'attendance_rate': 0.15,
        'task_completion': 0.20,
        'team_performance': 0.15,
        'problem_solving': 0.15,
        'leadership': 0.10,
        'conflict_resolution': 0.10
    }
    
    LEADERSHIP_FOCUSED_WEIGHTS = {
        'response_time': 0.10,
        'attendance_rate': 0.10,
        'task_completion': 0.15,
        'team_performance': 0.15,
        'problem_solving': 0.15,
        'leadership': 0.25,
        'conflict_resolution': 0.10
    }
    
    TEAMWORK_FOCUSED_WEIGHTS = {
        'response_time': 0.10,
        'attendance_rate': 0.10,
        'task_completion': 0.15,
        'team_performance': 0.25,
        'problem_solving': 0.15,
        'leadership': 0.10,
        'conflict_resolution': 0.15
    }

    def __init__(self, name, size, date, event_type="standard"):
        self.name = name
        self.size = size
        self.date = date
        self.participants = []
        self.status = "Scheduled"
        
        # Set weights based on event type
        self.event_type = event_type
        self.metrics_weights = self._get_weights_for_type(event_type)
    
    def _get_weights_for_type(self, event_type):
        weight_profiles = {
            "standard": self.STANDARD_WEIGHTS,
            "leadership": self.LEADERSHIP_FOCUSED_WEIGHTS,
            "teamwork": self.TEAMWORK_FOCUSED_WEIGHTS
        }
        return weight_profiles.get(event_type, self.STANDARD_WEIGHTS)
    
    def set_custom_weights(self, custom_weights):
        """
        Set custom weights for this specific event
        """
        if abs(sum(custom_weights.values()) - 1.0) < 0.001:
            self.metrics_weights = custom_weights
            return True
        return False

    # ... rest of the methods remain the same ... 