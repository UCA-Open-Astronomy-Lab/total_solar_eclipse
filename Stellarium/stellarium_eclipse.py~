import requests
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

set_time(2460409.285573, 1.0)
focus_on_target("sun")

r = requests.get(f"{STELLARIUM_URL}/api/objects/info?format=json")
data = r.json()
print(data["eclipse-obscuration"])



