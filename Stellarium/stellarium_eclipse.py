import requests
import time
import numpy as np
STELLARIUM_URL='http://localhost:8090'

def set_time(julian_day,timerate):
    url = f"{STELLARIUM_URL}/api/main/time"
    data = "time="+str(julian_day)
    print(f"Request URL: {url}")
    print(f"Request Data: {data}")
    try:
        response = requests.post(url, data=data)
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        response.raise_for_status()
        if response.text.strip() == "ok":
            return {"status": "success", "message": "Time set successfully"}
        else:
            return {"status": "error", "message": response.text}
    except requests.exceptions.RequestException as e:
        print(f"Error setting time: {e}")
        return {"status": "error", "message": str(e)}

def focus_on_target(target):
    url = f"{STELLARIUM_URL}/api/main/focus"
    data = "target="+str(target)
    print(f"Request URL: {url}")
    print(f"Request Data: {data}")
    try:
        response = requests.post(url, data=data)
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        response.raise_for_status()
        if response.text.strip() == "ok":
            return {"status": "success", "message": "Target set successfully"}
        else:
            return {"status": "error", "message": response.text}
    except requests.exceptions.RequestException as e:
        print(f"Error setting target: {e}")
        return {"status": "error", "message": str(e)}


t_start = 2460409.1902778
t_end = 2460409.3833333
N = 1000
dt = (t_end - t_start)/N

focus_on_target("sun")

t = t_start
times = []

eclipse_magnitude = []
eclipse_obscuration = []

while t <= t_end:
    set_time(t, 0.0)
    time.sleep(0.1)
    r = requests.get(f"{STELLARIUM_URL}/api/objects/info?format=json")
    data = r.json()
    times.append(t)
    eclipse_obscuration.append(data["eclipse-obscuration"])
    eclipse_magnitude.append(data["eclipse-magnitude"])    
    t += dt

results = np.column_stack([times, eclipse_obscuration, eclipse_magnitude])

np.savetxt("stellarium_lightcurve.csv", results, delimiter=",")

print(eclipse_obscuration)


#set_time(2460409.295573, 1.0)
#focus_on_target("sun")
#r = requests.get(f"{STELLARIUM_URL}/api/objects/info?format=json")
#data = r.json()
#print(data["eclipse-obscuration"])




