import requests
import pprint
import datetime

def get_upload_link(days_count, tag):
    upload_url = "https://api.stackexchange.com/2.2/search"
    headers = {"Content-type": "application/json"}
    to_date = datetime.datetime.now()
    from_date = to_date - datetime.timedelta(days=days_count)
    params = {"fromdate": int(from_date.timestamp()), "todate":  int(to_date.timestamp()), "tagged": tag, "site": "stackoverflow"}
    response = requests.get(upload_url, headers=headers, params=params)
    return response.json()

response = get_upload_link(2, "Python")
#pprint.pprint(response)

for item in response["items"]:
    print(item["question_id"], item["link"])
