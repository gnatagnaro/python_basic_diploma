import requests

url = "https://car-api2.p.rapidapi.com/api/models"

querystring = {"sort":"id","direction":"asc","verbose":"yes"}

headers = {
	"X-RapidAPI-Key": "95874cdb02msh3addaa568aec48fp17359ajsn5cc91c4bcfb5",
	"X-RapidAPI-Host": "car-api2.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
