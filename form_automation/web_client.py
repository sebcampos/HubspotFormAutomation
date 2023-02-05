from requests import Session, Response
from .credentials import OAUTH_TOKEN_REFRESH, CLIENT_SECRET, CLIENT_ID
from Logger import set_up_logger, logging

logger = set_up_logger('webclient-logger')
logger.setLevel(logging.WARNING)


class WebClient(Session):
    form_endpoint = 'https://api.hubapi.com/forms/v2/forms'
    form_fields_endpoint = 'https://api.hubapi.com/forms/v2/fields/'
    access_token_endpoint = 'https://api.hubapi.com/oauth/v1/access-tokens/'
    refresh_token_endpoint = 'https://api.hubapi.com/oauth/v1/token'
    refresh_token_info_endpoint = 'https://api.hubapi.com/oauth/v1/refresh-tokens/'
    submit_api_url = f'https://api.hsforms.com/submissions/v3/integration/secure/submit/'
    forms = {}
    oauth_access: str

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.refresh_bearer_token()
        self.headers.update({'Authorization': f'Bearer {self.oauth_access}'})
        for form in self.get_forms().json():
            name = form['name']
            guid = form['guid']
            portal_id = form['portalId']
            self.forms[name] = (guid, portal_id)

    def show_form_names(self) -> None:
        print('Names')
        for name in self.forms:
            print(name)

    def get_access_tokens_endpoint(self) -> Response:
        """
        Provides info on user, and token
        :return:
        """
        return self.get(f'{self.access_token_endpoint}/{self.oauth_access}')

    def oauth_refresh_token_data(self):
        return self.get(f'{self.refresh_token_info_endpoint}/{OAUTH_TOKEN_REFRESH}')

    def refresh_bearer_token(self):
        r = self.post(self.refresh_token_endpoint, data={
            "grant_type": 'refresh_token',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': "http://localhost",
            'refresh_token': OAUTH_TOKEN_REFRESH
        }).json()
        self.oauth_access = r['access_token']
        logger.debug(r)

    def get_forms(self) -> Response:
        return self.get(self.form_endpoint)

    def get_form_fields(self, form_id) -> Response:
        return self.get(f'{self.form_fields_endpoint}{form_id}')

    def get_required_form_fields(self, form_name):
        form_id = self.forms.get(form_name)[0]
        r = self.get_form_fields(form_id)
        return tuple(i['name'] for i in r.json() if i['required'])

    def get_form_field_names(self, form_name):
        form_id = self.forms.get(form_name)[0]
        r = self.get_form_fields(form_id)
        return tuple(i['name'] for i in r.json())

    def submit_form_api(self, form) -> Response:
        form_id, portal_id = self.forms[form.name]
        return self.post(f'{self.submit_api_url}{portal_id}/{form_id}', json=form.to_dict())
