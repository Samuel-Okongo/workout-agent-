import pytest
from app import App
from app.plugins.fitness_trainer_chat import FitnessTrainerChat  # assuming you have this plugin

def test_app_fitness_command(capfd, monkeypatch):
    """Test that the REPL correctly handles the 'fitness' command."""
    # Simulate user entering 'fitness' followed by 'done'
    inputs = iter(['fitness', 'done'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    app.register_plugin(FitnessTrainerChat())  # assuming this method registers the command
    with pytest.raises(SystemExit) as e:
        app.start()  # Starting the REPL loop
    
    # Verifying that the app started and exited as expected
    assert str(e.value) == "Exiting...", "The app did not exit as expected"

    # Capture the output and perform your assertions here
    out, err = capfd.readouterr()
    assert "Welcome to the Fitness Trainer Chat!" in out
    assert "Thank you for using the Fitness Trainer Chat. Goodbye!" in out
