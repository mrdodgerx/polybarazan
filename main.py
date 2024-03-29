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
        key = box.find('h4').text
        value = box.find('span').text
        salat_times[key] = value
    return salat_times

def is_time_in_range(start, end, current):
    start_time = datetime.datetime.strptime(start, '%H:%M')
    end_time = datetime.datetime.strptime(end, '%H:%M')
    current_time = datetime.datetime.strptime(current, '%H:%M:%S')
    return start_time <= current_time <= end_time

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
        
        current_time = datetime.datetime.now().time().strftime('%H:%M:%S')
        convert_from = "%H:%M"
        wanted_time_format = "%I:%M %p"
        list_timings = list(timings.items())  
        
        for i in range(len(list_timings)):
            prayer, time_range = list_timings[i]
            
            is_prayer_time(prayer,time_range) # Send Notification Prayer Time
            
            if i < len(list_timings) - 1:
    
                start = time_range
                end = list_timings[i + 1][1]
                prayer_time = list_timings[i + 1][1]
                prayer = list_timings[i + 1][0]
                    
                if is_time_in_range(start, end, current_time):
                    # print(f"Current Time: {prayer}, Next: {list_timings[i + 1][0]} at {list_timings[i + 1][1]}")
                    print(f" {prayer} at {prayer_time}")
                    break
            else:
                end = time_range
                start = list_timings[0][1]
                prayer_time = list_timings[0][1]
                prayer = list_timings[0][0]
                # print(f"Current Time: {list_timings[len(list_timings) - 1][0]}, Next: {list_timings[0][0]} at {list_timings[0][1]}")
                print(f" {prayer} at {prayer_time}")
                break
        
    except Exception as err:
        print('Error, cannot get the page')
