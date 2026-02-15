from classes import AnonymousSurvey

def test_store_single_response():
    question = "What Language did you first learn to speak?"
    language_survey = AnonymousSurvey(question)
    language_survey.store_responses("English")
    assert "English" in language_survey.responses