import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Command Pattern classes
class Command:
    """Base class for all command plugins, with metadata for dynamic menu generation."""
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def execute(self, *args, **kwargs):
        """Execute the command with the provided arguments."""
        raise NotImplementedError("Command execution not implemented.")

class CommandHandler:
    """Handles registration and execution of commands."""
    def __init__(self):
        self.commands = {}

    def register_command(self, command):
        """Register a command instance."""
        if command.name in self.commands:
            logging.warning(f"Command '{command.name}' is already registered. Overwriting.")
        self.commands[command.name] = command
        logging.info(f"Command '{command.name}' registered successfully.")

    def get_commands(self):
        """Return a list of command metadata for all registered commands."""
        return [(cmd.name, cmd.description) for cmd in self.commands.values()]

    def execute_command(self, name, *args):
        """Execute a command by name."""
        command = self.commands.get(name)
        if not command:
            logging.error(f"Command '{name}' not found.")
            return
        try:
            command.execute(*args)
        except Exception as e:
            logging.error(f"Error executing command '{name}': {e}")

# Concrete Command implementations
class StartWorkoutCommand(Command):
    def __init__(self):
        super().__init__("start_workout", "Start a new workout session")

    def execute(self, *args, **kwargs):
        print("Workout session has started! Let's do some exercises.")
        # Here you would add logic to start the workout session.

class EndWorkoutCommand(Command):
    def __init__(self):
        super().__init__("end_workout", "End the current workout session")

    def execute(self, *args, **kwargs):
        print("Workout session has ended. Great job!")
        # Here you would add logic to end the workout session.

# Application class that uses the CommandHandler
class WorkoutAgentApp:
    def __init__(self):
        self.command_handler = CommandHandler()
        self.setup_commands()

    def setup_commands(self):
        """Register all commands with the command handler."""
        self.command_handler.register_command(StartWorkoutCommand())
        self.command_handler.register_command(EndWorkoutCommand())

    def run(self):
        """Run the main application loop."""
        print("Welcome to the Workout Agent!")
        print("Available commands: ")
        for name, description in self.command_handler.get_commands():
            print(f"{name} - {description}")
        print("Type 'exit' to quit.")

        while True:
            command_input = input("Enter a command: ")
            if command_input.lower() == "exit":
                print("Exiting the Workout Agent. Goodbye!")
                break
            self.command_handler.execute_command(command_input)

# Entry point for the application
if __name__ == "__main__":
    app = WorkoutAgentApp()
    app.run()
