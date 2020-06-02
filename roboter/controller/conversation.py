"""Controller for speaking with robot"""
from roboter.models import robot


def talk_about_language():
    """Function to speak with robot"""
    language_robot = robot.LanguageRobot()
    language_robot.hello()
    language_robot.recommend_language()
    language_robot.ask_user_favorite()
    language_robot.thank_you()

    