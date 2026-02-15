from functions import get_formated_name

def test_first_last_name():
    formatted_name = get_formated_name('alireza','e' ,'ghorbani')
    assert formatted_name == 'Alireza E Ghorbani'
    
    