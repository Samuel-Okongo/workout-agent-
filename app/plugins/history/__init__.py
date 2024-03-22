import os
import logging
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.commands import Command

class FitnessHistory(Command):
    """Command for interacting with a user's workout history."""

    def __init__(self, user_id):
        super().__init__()
        self.name = "fitness_history"
        self.description = "Interact with your fitness history to track your progress."
        self.history = []  # List to store the workout sessions
        self.user_id = user_id  # Assuming each user has a unique ID

    def add_workout_session(self, session_data):
        """Add a workout session to the history."""
        session_data['timestamp'] = datetime.now().isoformat()  # Automatically add the current timestamp
        self.history.append(session_data)
        logging.info(f"User {self.user_id}: Added workout session to history: {session_data}")
        # Here you might also want to persist this data to a database or file

    def get_last_session(self):
        """Get the last workout session if available."""
        return self.history[-1] if self.history else None

    def summarize_history(self):
        """Create a summary of the workout history."""
        total_time = sum(session['duration'] for session in self.history)
        total_workouts = len(self.history)
        # Assuming each session has 'calories_burned' recorded
        total_calories = sum(session['calories_burned'] for session in self.history)

        summary = {
            "total_sessions": total_workouts,
            "total_time_spent": total_time,
            "total_calories_burned": total_calories
        }
        return summary

    def execute(self, *args, **kwargs):
        """Execute the fitness history command."""
        user_input = kwargs.get('user_input', 'summary')  # Default to showing summary

        if user_input == 'add':
            session_data = kwargs.get('session_data')
            if session_data:
                self.add_workout_session(session_data)
            else:
                logging.error("No session data provided for 'add' operation.")
        elif user_input == 'last':
            return self.get_last_session()
        elif user_input == 'summary':
            return self.summarize_history()
        else:
            logging.error(f"Invalid user input for fitness history: {user_input}")
            # Depending on your error handling, you might want to raise a custom exception here

# Example of how this class could be used
if __name__ == "__main__":
    user_id = "user123"
    history_cmd = FitnessHistory(user_id=user_id)

    # Adding a workout session
    history_cmd.execute(user_input='add', session_data={
        'workout_type': 'Running',
        'duration': 30,  # Duration in minutes
        'calories_burned': 300
    })

    # Getting the last workout session
    last_session = history_cmd.execute(user_input='last')
    print(f"Last workout session: {last_session}")

    # Getting a summary of all workouts
    summary = history_cmd.execute(user_input='summary')
    print(f"Workout summary: {summary}")

