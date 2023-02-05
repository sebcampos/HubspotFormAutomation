from typing import Self
class Form:
    """
    The form class serves the purpose of managing important form data
    and formatting the data for a proper form submission
    """
    portal_id: str
    form_id: str
    fields: list
    # submittedAt: str = '1517927174000'
    # context: dict = {'hutk': 'hutk'}
    # legalConsentOptions: dict = {}
    # consent: dict = {
    #     'consentToProcess': True,
    #     'text': 'I agree to allow Example Company to store and process my personal data.',
    #     'communications':
    #         [
    #             {
    #                 'value': True,
    #                 'subscriptionTypeId': 999,
    #                 'text': 'I agree to receive marketing communications from Example Company.'
    #             }
    #         ]
    # }

    def __init__(self, fields: dict, portal_id: str, form_id: str) -> Self:
        """
        recieves a dictionary and two identifiers.
        saves the identifiers as instance variables then
        formats the fields into the required format and saves it as the
        instance variable fields.
        :param fields: dictionary of fields
        :param portal_id: string portal id
        :param form_id: string form id
        """
        self.portal_id = portal_id
        self.form_id = form_id
        self.fields = []
        for name, value in fields.items():
            field = \
                {
                    'objectTypeId': '0-1',
                    'name': name,
                    'value': value
                }
            self.fields.append(field)
        # self.context.update({
        #     "pageUri": "www.example.com/page",
        #     "pageName": "Example page"
        # })

    def __str__(self):
        return str(self.fields)

    def to_dict(self) -> dict:
        """
        Creates a dictionary of the form fields
        :return: dict fields
        """
        # self.legalConsentOptions['consent'] = self.consent
        data = \
            {
                # 'submittedAt': self.submittedAt,
                'fields': self.fields,
                # 'context': self.context,
                # 'legalConsentOptions': self.legalConsentOptions
            }
        return data