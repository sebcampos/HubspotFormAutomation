from app import main


def test_help_flag():
    main(['-h'])


def test_list_form_names():
    main(['-l'])


def test_show_required_fields():
    main(['-sfr', 'Logistics Management Test'])


def test_show_field_names():
    main(['-sf', 'Logistics Management Test'])


def test_invalid_form_in_main():
    main(['../test_data/TestFile.xlsx', 'Logistics Management Test'])


def test_main():
    main(['../test_data/TestFile2.xlsx', 'Logistics Management Test'])
