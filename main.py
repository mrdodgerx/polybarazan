    #    url = 'https://www.waktusolat.my/terengganu/trg01'
import requests
import datetime
from bs4 import BeautifulSoup
import subprocess
import os

def get_html_page():
    url = 'https://www.waktusolat.my/selangor/sgr01'
    r = requests.get(url=url)
    if r.status_code == 200:
        return r.content
    return None

def get_prayer_time(html):
    soup = BeautifulSoup(html, 'html.parser')
    salat_boxes = soup.find_all(class_='salat-times__box')
    salat_times = {}
    for box in salat_boxes:
        key = box.find('h4').text.strip()
        value = box.find('span').text.strip()
        salat_times[key] = value
    return salat_times

def send_notification(title, message):
    command = ['notify-send', title, message]
    subprocess.run(command)


def play_azan(prayer_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    mp3_dir = os.path.join(base_dir, "mp3")

    # Determine which file to play
    lower_name = prayer_name.lower()
    if lower_name == "maghrib":
        filename = "Maghrib.mp3"
    elif lower_name == "subuh":
        filename = "Subuh.mp3"
    else:
        # Do not play anything for Imsak
        if lower_name == "imsak":
            return
        filename = "Azan.mp3"

    file_path = os.path.join(mp3_dir, filename)

    # Start the player in the background so this script can exit quickly
    try:
        subprocess.Popen(["mpv", "--no-video", "--really-quiet", file_path])
    except FileNotFoundError:
        # Fallback: open with default application if mpv is not installed
        subprocess.Popen(["xdg-open", file_path])


def should_play_for_prayer(prayer_name):
    """
    Ensure we only play once per prayer per day.
    Stores last played prayer in a small state file.
    """
    today = datetime.date.today().isoformat()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    state_file = os.path.join(base_dir, ".last_prayer_played")

    last_prayer = None
    last_date = None

    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content:
                last_date, last_prayer = content.split("|", 1)
        except Exception:
            last_prayer = None
            last_date = None

    if last_date == today and last_prayer == prayer_name:
        return False

    try:
        with open(state_file, "w", encoding="utf-8") as f:
            f.write(f"{today}|{prayer_name}")
    except Exception:
        # If we cannot write the file, we still allow playing once.
        pass

    return True

def is_prayer_time(prayer, prayer_time_str):
    """
    Only trigger when the current clock time exactly matches the prayer time.
    Also ensures the azan is only played once per prayer per day.
    """
    time_now = datetime.datetime.now().strftime('%H:%M')
    if time_now == prayer_time_str:
        send_notification("Prayer Time", f"It's time for {prayer}.")

        # Only play for non-Imsak prayers, and only once per day/prayer
        if should_play_for_prayer(prayer):
            play_azan(prayer)

if __name__ == "__main__":
    try:
        html = get_html_page()
        timings = get_prayer_time(html)

        # Convert prayer times into a list of (prayer_name, datetime_object)
        now = datetime.datetime.now()
        prayer_times = []
        
        for prayer, time_str in timings.items():
            prayer_time = datetime.datetime.strptime(time_str, '%H:%M').time()
            prayer_times.append((prayer, prayer_time))

        # Sort prayers by time
        prayer_times.sort(key=lambda x: x[1])

        # Check if it is exactly time for any prayer and, if so, send notification and (optionally) play azan
        for prayer, time_str in timings.items():
            is_prayer_time(prayer, time_str)

        # Find the next upcoming prayer
        next_prayer = None
        next_prayer_time = None

        for prayer, prayer_time in prayer_times:
            if prayer_time > now.time():
                next_prayer = prayer
                next_prayer_time = prayer_time
                break

        # If no future prayer is found, pick the first one (for next day)
        if next_prayer is None:
            next_prayer, next_prayer_time = prayer_times[0]
            next_prayer_datetime = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), next_prayer_time)
        else:
            next_prayer_datetime = datetime.datetime.combine(now.date(), next_prayer_time)

        # Calculate the time left until the next prayer
        time_diff = next_prayer_datetime - now
        remaining_minutes = time_diff.seconds // 60
        remaining_seconds = time_diff.seconds % 60

        #print(f" {next_prayer} at {next_prayer_time.strftime('%H:%M')} ({remaining_minutes}m {remaining_seconds}s left)")
        print(f"{next_prayer} at {next_prayer_time.strftime('%H:%M')} ({remaining_minutes}m {remaining_seconds}s left)")

    except Exception as err:
        print('Error, cannot get the page')

