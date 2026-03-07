    #    url = 'https://www.waktusolat.my/terengganu/trg01'
import requests
import datetime
from bs4 import BeautifulSoup
import subprocess

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

def is_prayer_time(prayer, prayer_time):
    time_now = datetime.datetime.now().strftime('%H:%M')
    if time_now == prayer_time:
        send_notification("Prayer Time", f"It's time for {prayer}.")

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

