import requests

url = "https://flask-app-backend-updated.el.r.appspot.com/api/token?key=AIzaSyB6Qp7R6BAFoDD93L0wG_EEhY7oQuQXf3I"

payload = {'email': 'sarthakvashisth@yahoo.com',
'password': 'Vannya@1234'}
files = [

]
headers= {}

response = requests.request("GET", url, headers=headers, data = payload, files = files)

print(response.text.encode('utf8'))
