from form_automation import WebClient, Form
from Logger import set_up_logger
import pandas as pd
from tqdm import tqdm

logger = set_up_logger('form-automation')


def main(args):
    requirements_met = True
    webclient = WebClient()
    form_name = args[-1]
    if form_name == '-l':
        webclient.show_form_names()
        return
    elif form_name == '-h':
        print('Args:')
        print('\tpython form_automation <filepath> <form_name>')
        print('Commands:')
        string = '\tpython form_automation -h' 
        print(f'{string:50} -> help menu')
        string = '\tpython form_automation -l' 
        print(f'{string:50} -> displays a list of form names and their ids')
        string = '\tpython form_automation -sfr <form_name>'
        print(f'{string:50} -> displays required fields for this form id')
        string = '\tpython form_automation -sf  <form_name>'
        print(f'{string:50} -> displays fields for this form id')
        return
    elif args[-2] == '-sfr':
        print(form_name)
        required = webclient.get_required_form_fields(form_name)
        for field in required:
            print(field)
        return

    elif args[-2] == '-sf':
        print(webclient.forms[form_name][0])
        required = webclient.get_form_field_names(form_name)
        for field in required:
            print(field)
        return

    file_path = args[-2]

    # read in excel, clean columns, replace NaN values
    excel_df = pd.read_excel(file_path)
    excel_df.columns = [i.strip().replace(' ', '').lower() for i in excel_df.columns]
    excel_df.fillna('None', inplace=True)

    # collect fields and required fields
    required_fields = webclient.get_required_form_fields(form_name)
    fields = webclient.get_form_field_names(form_name)


    # validate required fields are present in sheet
    for field in required_fields:
        if field not in excel_df.columns:
            logger.warning(f'Required {field} does not exist in excel sheet please verify')
            requirements_met = False

    # validate all fields in excel sheet are valid form fields
    for field in excel_df.columns:
        if field not in fields:
            logger.warning(f'{field} in excel sheet does not exist in form please verify')
            requirements_met = False

    if requirements_met is False:
        logger.error('Please confirm all fields in excel sheet are matching form fields')
        return

    failed = ()
    if webclient.forms.get(form_name, None) is None:
        logger.error(f'Form with name: {form_name} does not exist')
        return
    pbar = tqdm(total=len(excel_df))
    for row in excel_df.itertuples(index=False):
        form = Form(row._asdict(), form_name)
        r = webclient.submit_form_api(form)
        if r.status_code != 200:
            failed += ((form, r),)
            logger.warning('Failed submission:')
            logger.warning(form)
            logger.warning(r.content.decode())
        logger.debug(f'{r.status_code}')
        pbar.update(1)
    pbar.close()

    if len(failed) > 0:
        logger.warning('Some entries were not accepted by the api')
        for form in failed:
            print(form.fields)

