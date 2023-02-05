from typing import Self
from .form import Form
from requests import Session, Response
from .credentials import OAUTH_TOKEN_REFRESH, CLIENT_SECRET, CLIENT_ID
from Logger import set_up_logger

logger = set_up_logger('webclient-logger')


class WebClient(Session):
    oauth_access: str
    form_endpoint: str = 'https://api.hubapi.com/forms/v2/forms'
    form_submissions: str = 'https://api.hubapi.com/form-integrations/v1/submissions/forms/'
    form_fields_endpoint: str = 'https://api.hubapi.com/forms/v2/fields/'
    access_token_endpoint: str = 'https://api.hubapi.com/oauth/v1/access-tokens/'
    refresh_token_endpoint: str = 'https://api.hubapi.com/oauth/v1/token'
    refresh_token_info_endpoint: str = 'https://api.hubapi.com/oauth/v1/refresh-tokens/'
    submit_api_url: str = f'https://api.hsforms.com/submissions/v3/integration/secure/submit/'
    forms: dict = {}

    def __init__(self) -> Self:
        """
        This method calls the init method of the Session Class.
        Then, using an authenticated hubspot app, it will use the oath refresh
        token to obtain a new access token and set it in the headers
        """
        super().__init__()
        self.refresh_bearer_token()
        self.headers.update({'Authorization': f'Bearer {self.oauth_access}'})

        # collect all the form names, ids, and portal ids
        for form in self.get_forms().json():
            name = form['name']
            guid = form['guid']
            portal_id = form['portalId']
            self.forms[guid] = (name, portal_id)

    def show_form_names(self) -> None:
        """
        Displays the name and guid for every form
        connected to the users account
        :return: void
        """
        name = 'name'
        guid = 'guid'
        print(f'{name:50} {guid:20}')
        for guid, name in self.forms.items():
            print(f'{name[0]:50}', end='')
            print(f'{guid:20}')

    def get_access_tokens_endpoint(self) -> Response:
        """
        Provides info on user, and token
        :return: HTTPResponse
        """
        return self.get(f'{self.access_token_endpoint}/{self.oauth_access}')

    def oauth_refresh_token_data(self) -> Response:
        """
        Provides info on the refresh token
        :return: HTTPResponse
        """
        return self.get(f'{self.refresh_token_info_endpoint}/{OAUTH_TOKEN_REFRESH}')

    def refresh_bearer_token(self) -> None:
        """
        Creates a post request to the refresh token endpoint
        to obtain a new access token, then sets the token
        as an instance var
        :return: void
        """

        r = self.post(self.refresh_token_endpoint, data={
            "grant_type": 'refresh_token',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': "http://localhost",
            'refresh_token': OAUTH_TOKEN_REFRESH
        }).json()
        # set the new access token
        self.oauth_access = r['access_token']
        logger.debug(r)

    def get_forms(self) -> Response:
        """
        returns a request for all forms data
        :return: HTTPResponse
        """
        return self.get(self.form_endpoint)

    def get_form_fields(self, form_id: str) -> Response:
        """
        Makes a request to the fields endpoing for a specified form
        :param form_id: form id as a string for form lookup
        :return: HTTPResponse
        """
        return self.get(f'{self.form_fields_endpoint}{form_id}')

    def get_required_form_fields(self, form_id: str) -> tuple:
        """
        Returns all required field names for the specified form
        :param form_id: form id as a string for form lookup
        :return: tuple for required field names
        """
        r = self.get_form_fields(form_id)
        return tuple(i['name'] for i in r.json() if i['required'])

    def get_form_field_names(self, form_id) -> tuple:
        """
        Returns all field names for the specified form
        :param form_id: form id as a string for form lookup
        :return: tuple for field names
        """
        r = self.get_form_fields(form_id)
        return tuple(i['name'] for i in r.json())

    def submit_form_api(self, form: Form) -> Response:
        """
        Creates a post request to submit a form
        :param form: instance of the Form class
        :return: HTTPResponse
        """
        return self.post(f'{self.submit_api_url}{form.portal_id}/{form.form_id}', json=form.to_dict())

    def get_form_submissions(self, form_id: str) -> Response:
        """
        Makes a request to the form submissions endpoint
        for the specified form
        :param form_id: form id as a string for form lookup
        :return: HTTPResponse
        """
        self.get(self.form_submissions + form_id)
