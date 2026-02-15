import functions


print('Enter "q" for exit ')
while True:
    first_name = input('\n Please enter your first name: ')
    if first_name == 'q':
        break
    last_name = input("\n Please enter your last name: ")
    if last_name == 'q':
        break
    
    formatted_name = functions.get_formated_name(first_name, last_name)
    print(f'\n\t your name: {formatted_name} ')
    
    
    
from classes import AnonymousSurvey


question = "What Language did you first learn to speak?"
language_survey = AnonymousSurvey(question)

language_survey.show_question()
print("Enter 'q' to any time to quit.\n")

while True:
    response = input("Language: ")
    if response == 'q':
        break
    language_survey.store_responses(response)
    
    print("\n Thank you to everyone ...")
    language_survey.show_results()
    