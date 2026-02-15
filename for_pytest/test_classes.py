from classes import AnonymousSurvey
import pytest


# def test_store_single_response():
#     question = "What Language did you first learn to speak?"
#     language_survey = AnonymousSurvey(question)
#     language_survey.store_responses("English")
#     assert "English" in language_survey.responses
    
    
    
    
@pytest.fixture
def language_survey():
    question = "What Language did you first learn to speak?"
    language_survey = AnonymousSurvey(question)
    return language_survey

def test_store_single_response(language_survey):
    language_survey.store_responses("English")
    assert "English" in language_survey.responses
    