import requests
import datetime
from bs4 import BeautifulSoup
import time

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
        key = box.find('h4').text
        value = box.find('span').text
        salat_times[key] = value
    return salat_times

def is_time_in_range(start, end, current):
    start_time = datetime.datetime.strptime(start, '%H:%M')
    end_time = datetime.datetime.strptime(end, '%H:%M')
    current_time = datetime.datetime.strptime(current, '%H:%M:%S')
    return start_time <= current_time <= end_time
        
def convert_time(time, convert_from, convert_to):
    return datetime.datetime.strptime(time, convert_from).time().strftime(convert_to)

if __name__ == "__main__":
    try:
        html = get_html_page()
        timings = get_prayer_time(html)
        
        current_time = datetime.datetime.now().time().strftime('%H:%M:%S')
        convert_from = "%H:%M"
        wanted_time_format = "%I:%M %p"

        # print(timings)
        # print(current_time)
        
        # Convert dict_items object to list of tuples
        prayer_times = list(timings.items())
        
        for i in range(len(prayer_times)):
            prayer, time_range = prayer_times[i]
            # print(prayer, time_range)
            if i < len(prayer_times) - 1:
                start = time_range
                end = prayer_times[i + 1][1]  # Accessing the end time from the next tuple
                if is_time_in_range(start, end, current_time):
                    print(f"Current Time: {prayer}, Next: {prayer_times[i + 1][0]} at {prayer_times[i + 1][1]}")
                    break
            else:
                end = time_range
                start = prayer_times[0][1]  # Accessing the end time from the next tuple
                print(start, end)
                print(f"Current Time: {prayer_times[len(prayer_times) - 1][0]}, Next: {prayer_times[0][0]} at {prayer_times[0][1]}")
                break
        
    except Exception as err:
        print(err)
    