import os
import sys
import signal
import configparser
from src.monitor import monitor_idle_time
from src.shutdown import shutdown_system, sleep_system
from src.utils import ensure_log_directory, log_event

def create_default_config(config_path):
    """Create a default settings.ini file if none is found."""
    config = configparser.ConfigParser()
    config['General'] = {
        'idle_time_limit': '120',
        'action': 'sleep',
        'log_file': 'log/winadmin.log',
        'check_interval': '10'
    }

    with open(config_path, 'w') as configfile:
        config.write(configfile)

    print(f"Default configuration file created at {config_path}")

def signal_handler(sig, frame):
    """Handle termination signals."""
    print('Terminating the service...')
    sys.exit(0)

def main():
    print("Starting WinAdminService...")

    config = configparser.ConfigParser()

    # Determine the path to the external config file
    exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    config_path = os.path.join(exe_dir, 'settings.ini')

    # Create default config if not found
    if not os.path.exists(config_path):
        create_default_config(config_path)

    # Read the configuration file
    config.read(config_path)

    # Read the necessary configuration values
    idle_time_limit = config.getint('General', 'idle_time_limit')
    action = config.get('General', 'action')
    log_file = config.get('General', 'log_file')
    check_interval = config.getint('General', 'check_interval')

    print(f"Configuration loaded: idle_time_limit={idle_time_limit}, action={action}, log_file={log_file}, check_interval={check_interval}")

    # Ensure the log directory exists
    ensure_log_directory(log_file)

    # Log service start
    log_event(log_file, "WinAdminService started")

    # Start monitoring idle time
    should_shutdown = monitor_idle_time(idle_time_limit, check_interval, action, log_file)

    # Take the appropriate action based on the configuration
    if should_shutdown:
        print(f"Performing action: {action}")
        if action == 'shutdown':
            shutdown_system(log_file)
        elif action == 'sleep':
            sleep_system(log_file)

if __name__ == "__main__":
    # Set up signal handlers for clean termination
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    main()
