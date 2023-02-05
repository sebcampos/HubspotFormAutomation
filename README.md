# HubspotFormAutomation

This project aims to automate submitting hubspot forms by
creating a hubspot developer account, and using the form api.

### Hubspot app 
1. To create a developer account and generate access tokens visit [hubspot-devloper](https://developers.hubspot.com/get-started])
2. Create an app for this account
3. Using your apps App ID, Client ID, and Client secret build a url similar to this

https://app.hubspot.com/oauth/authorize?client_id=CLIENT_ID&redirect_uri=http://localhost&scope=actions%20forms%20forms-uploaded-files%20external_integrations.forms.access

4. If you are using your own hubspot account then you can visit this link. If this is for a client you can send them this link
5. Once they accept the will be redirected to their localhost with a url that contains a code `http://localhost?code=CODE`
6. Create a request to this endpoint
```
# Authorize code here to get OAUTH REFRESH TOKEN
r = requests.post('https://api.hubapi.com/oauth/v1/token', data={
        "grant_type": 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': "http://localhost",
        'code': '<CODE_HERE>'
})
```
7. The result will hold an access token, and a refresh token. The access token can be set in a request header to send requests to hubspot api. Save the refresh token to get new access tokens once they expire
8. Getting a new token
```
# Use this endpoint to refresh and create a new api token
r = requests.post('https://api.hubapi.com/oauth/v1/token', data={
        "grant_type": 'refresh_token',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': "http://localhost",
        'refresh_token': OAUTH_TOKEN_REFRESH
})
```

### Using the WebClient
1. Create a file called credentials.py inside of the form_automation directory
2. Populate it with this information
```
APP_ID = 'XXXXX'
CLIENT_ID = 'XXXXXX-XXXX-XXXXX-XXXX'
CLIENT_SECRET = 'XXXXX-XXXXX-XXXX-XXX-XXXXXX'

OAUTH_TOKEN_REFRESH = 'XXXXX-XXX-XXX-XXXXX-XXXXXXX'
```
3. Now you should be able to use the client
```
from form_automation.web_client import WebClient
c = WebClient()
c.show_form_names()
```