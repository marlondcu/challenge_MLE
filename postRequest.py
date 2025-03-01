import requests

# Define the URL and JSON 
url = "https://advana-challenge-check-api-cr-k4hdbggvoq-uc.a.run.app/software-engineer"
payload = {
    "name": "Marlon Oliveira",
    "mail": "oliwer.marlon@gmail.com",
    "github_url": "https://github.com/marlondcu/challenge_MLE.git",
    "api_url": "https://api-service-179269865167.us-central1.run.app"
}

response = requests.post(url, json=payload)# Make the POST request
    
