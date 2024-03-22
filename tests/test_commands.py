import pytest
from app import App
from app.commands.start_workout import StartWorkoutCommand
from app.commands.end_workout import EndWorkoutCommand

def test_app_start_workout_command(capfd, monkeypatch):
    """Test that the application correctly handles the 'start_workout' command."""
    # Simulate user entering 'start_workout' followed by 'exit'
    inputs = iter(['start_workout', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    app.command_handler.register_command(StartWorkoutCommand())
    app.command_handler.register_command(EndWorkoutCommand())
    app.start()  # Assuming App.start() initiates a loop for command input

    out, err = capfd.readouterr()
    assert "Workout session has started!" in out, "The start workout command did not execute as expected"

def test_app_end_workout_command(capfd, monkeypatch):
    """Test that the application correctly handles the 'end_workout' command."""
    # Simulate user entering 'end_workout' followed by 'exit'
    inputs = iter(['end_workout', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    app.command_handler.register_command(StartWorkoutCommand())
    app.command_handler.register_command(EndWorkoutCommand())
    app.start()  # Assuming App.start() initiates a loop for command input

    out, err = capfd.readouterr()
    assert "Workout session has ended." in out, "The end workout command did not execute as expected"
