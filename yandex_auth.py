import requests

def get_access_token():
    """ Obtain access token from Yandex OAuth """
    url = "https://oauth.yandex.com/token"
    data = {
        "grant_type": "authorization_code",
        "code": "your_authorization_code",
        "client_id": "your_client_id",
        "client_secret": "your_client_secret",
        "redirect_uri": "your_redirect_uri"
    }
    response = requests.post(url, data=data)
    return response.json().get("access_token")

# Дополнительно вы можете реализовать функцию для обновления токена с помощью refresh_token.
