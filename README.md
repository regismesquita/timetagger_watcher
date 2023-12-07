# TimeTagger Watcher

## Introduction

TimeTagger Watcher is a simple Python script designed to track your current task from TimeTagger and log it to an ActivityWatch bucket. This seamless integration can help you monitor your productivity and understand how your time is being allocated.

## Prerequisites

Before running the script, please ensure you have the following installed on your system:

- Python 3.x
- Requests package: `pip install requests`
- ActivityWatch Client package: `pip install aw-client`

## Setting Up

Set environment variables for your TimeTagger URL, token, and optionally, the log level:

```shell
export TIMETAGGER_URL="https://yourtimetagger.url/api/endpoint"
export TIMETAGGER_TOKEN="yourtimetaggertoken"
export LOG_LEVEL="INFO" # Default is WARNING, options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

For local or self-signed certificates, you may disable SSL verification in the script by keeping `VERIFY_CERTIFICATE = False`.

## Basic Usage

To start tracking your TimeTagger tasks with ActivityWatch, simply run the `timetagger_watcher.py` script:
```shell
python timetagger_watcher.py
```

## Example

Assuming your TimeTagger URL is `https://timetagger.example.com/timetagger/api/v2/records` and you have received a token, the setup would be:

```shell
export TIMETAGGER_URL="https://timetagger.example.com/timetagger/api/v2/records"
export TIMETAGGER_TOKEN="your_unique_token_here"
export LOG_LEVEL="INFO"
```

After setting these environment variables, run the script:
```shell
python timetagger_watcher.py
```

The log level `INFO` allows you to see informative messages providing insight into the script's operations and any issues encountered.

## Note

This script is meant to run continuously. If you wish to execute it in a more robust environment (e.g., background service), you may need to take additional steps to daemonize the script or monitor it with a tool like `supervisor` or `systemd`.

## Contribution

Your contributions to improve TimeTagger Watcher are welcome! Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. Please see the LICENSE.md file for details.