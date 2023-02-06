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

    def __init__(self, fields: dict = False, api_fields=False):
        self.fields = []
        if api_fields:
            self.fields = api_fields
        else:
            for name, value in fields.items():
                if name == '__len__':
                    continue
                field = \
                    {
                        'objectTypeId': '0-1',
                        'name': name,
                        'value': value
                    }
                self.fields.append(field)

        for i in self.fields:
            setattr(self, i['name'], i['value'])
        self.attributes = tuple(i for i in self.__dir__() if "__" not in i and i != 'to_dict')
        self.my_string = ''
        for attribute in self.attributes:
            if attribute == 'fields':
                continue
            self.my_string +=f'{attribute} : {self.__getattribute__(attribute)}'.lower() + '\n'

    def __str__(self):
        return self.my_string

    def __eq__(self, other):
        result = True
        if len(self.attributes) != len(other.attributes):
            return False
        for attribute in self.attributes:
            if attribute == 'fields':
                continue
            if str(self.__getattribute__(attribute)).lower() != str(other.__getattribute__(attribute)).lower():
                result = False
        return result

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
