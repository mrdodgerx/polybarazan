# PolyBarAzan

## Salat Time Tracker

PolyBarAzan is a Python script that retrieves and tracks the daily Islamic prayer times (Salat times) for a specific location. It fetches the prayer timings from the website [Waktu Solat](https://www.waktusolat.my/) and displays the current and next prayer times.

### Requirements

- Python 3.x
- BeautifulSoup (`pip install beautifulsoup4`)
- Requests (`pip install requests`)

### Installation

1. Clone or download the repository to your local machine.
2. Install the required dependencies using pip:

    ```
    pip install -r requirements.txt
    ```

### Description

The script performs the following tasks:

1. Retrieves the HTML content of the webpage containing the Salat times using the `requests` library.
2. Parses the HTML content using `BeautifulSoup`.
3. Extracts the Salat times from the parsed HTML.
4. Converts the Salat times to the desired time format.
5. Determines the current and next prayer times based on the current system time.
6. Prints the current and next prayer times in a formatted manner.
7. Sends desktop notifications when it's time for a prayer.

### Polybar Configuration

To integrate the Salat Time Tracker into Polybar, add the following configuration:

```ini
[module/azan]
type = custom/script
exec = /<path of your script>/azan.sh
interval = 60
```

### Usage

1. Ensure that the virtual environment is activated before running the script. You can do this by running:

~~~bash
source /home/mrdodgerx/Code4Life/PolyBarAzan/venv/bin/activate
~~~
2. Run the Python script using:
~~~
python /home/mrdodgerx/Code4Life/PolyBarAzan/main.py
~~~

The script will automatically update every 60 seconds to display the current and next prayer times. It will also send desktop notifications when it's time for a prayer.

Feel free to customize the script or Polybar configuration to suit your preferences.
~~~

This README.md provides comprehensive instructions on installation, usage, and configuration of the PolyBarAzan script. It includes details about activating the virtual environment, running the Python script, and configuring Polybar to display the prayer times. Additionally, it mentions the desktop notifications feature and provides a complete Polybar configuration snippet.

~~~