class Form:
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

    def __init__(self, fields: dict, form_name):
        self.name = form_name
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

    def to_dict(self):
        # self.legalConsentOptions['consent'] = self.consent
        data = \
            {
                # 'submittedAt': self.submittedAt,
                'fields': self.fields,
                # 'context': self.context,
                # 'legalConsentOptions': self.legalConsentOptions
            }
        return data