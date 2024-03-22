import logging

class Command:
    """Base class for all command plugins, with metadata for dynamic menu generation."""
    def __init__(self, name, description):
        self.name = name  # Command name for menu display
        self.description = description  # Command description for menu display

    def execute(self, *args, **kwargs):
        """Execute the command with given arguments."""
        raise NotImplementedError("Command execution not implemented.")

class CommandHandler:
    """Handles registration and execution of commands."""
    def __init__(self):
        self.commands = {}
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
            return False
        try:
            command.execute(*args)
            return True
        except Exception as e:
            logging.error(f"Error executing command '{name}': {e}")
            return False

    def parse_natural_language_command(self, input_string):
        """Parse natural language input to find and execute a command (Placeholder)."""
        # This is a placeholder for natural language processing logic.
        # You would typically use NLP techniques here to extract the command and arguments from the input string.
        logging.info("Parsing natural language command (placeholder function).")
        return False

    # New method to discover commands based on keywords in their descriptions.
    def find_command_by_description(self, keyword):
        """Find commands by keyword in their descriptions."""
        matches = [cmd for cmd in self.commands.values() if keyword.lower() in cmd.description.lower()]
        if not matches:
            logging.info(f"No commands found containing the keyword '{keyword}'.")
            return []
        else:
            return [(cmd.name, cmd.description) for cmd in matches]
