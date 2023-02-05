from app import main


def test_help_flag():
    main(['-h'])


def test_list_form_names():
    main(['-l'])


def test_show_required_fields():
    main(['-sfr', '94fd4aa4-c4b7-4449-b668-dcee349809f4'])


def test_show_field_names():
    main(['-sf', '94fd4aa4-c4b7-4449-b668-dcee349809f4'])


def test_invalid_form_in_main():
    main(['../test_data/TestFile.xlsx', '94fd4aa4-c4b7-4449-b668-dcee349809f4'])


def test_main():
    main(['../test_data/TestFile2.xlsx', '94fd4aa4-c4b7-4449-b668-dcee349809f4'])
