import requests
from credentials import CLIENT_ID, CLIENT_SECRET, OAUTH_TOKEN_REFRESH


#  c.headers.update({'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'})
# create app and get this url

auth_url = \
"""
https://app.hubspot.com/oauth/authorize?client_id=a67fe08c-32b1-474a-b712-2f69f5116600&redirect_uri=http://localhost&scope=actions%20forms%20forms-uploaded-files%20external_integrations.forms.access
"""

# have user authenticate and they will be returned to the redirect
# url with a code as a url param
# use the url param in this requests



# Authorize code here to get OAUTH REFRESH TOKEN
r = requests.post('https://api.hubapi.com/oauth/v1/token', data={
        "grant_type": 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': "http://localhost",
        'code': '<CODE_HERE>'
})


# Use this endpoint to refresh and create a new api token
r = requests.post('https://api.hubapi.com/oauth/v1/token', data={
        "grant_type": 'refresh_token',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': "http://localhost",
        'refresh_token': OAUTH_TOKEN_REFRESH
})