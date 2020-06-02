"""Defined a robot model """
from roboter.models import ranking
from roboter.views import console


DEFAULT_ROBOT_NAME = 'Roboko'


class Robot(object):
    """Base model for Robot."""

    def __init__(self, name=DEFAULT_ROBOT_NAME, user_name='',
                speak_color='green'):
        self.name = name
        self.user_name = user_name
        self.speak_color = speak_color

    def hello(self):
        """Returns words to the user that the robot speaks at the begginning."""
        while True:
            template = console.get_template('hello.txt', self.speak_color)
            user_name = input(template.substitute({
                'robot_name': self.name}))

            if user_name:
                self.user_name = user_name.title()
                break

class LanguageRobot(Robot):
    """Handle data model on language"""

    def __init__(self, name=DEFAULT_ROBOT_NAME):
        super().__init__(name=name)
        self.ranking_model = ranking.RankingModel()

    def _hello_decorator(func):
        """Decorator to say a greeting if you are not greeting the user."""
        def wrapper(self):
            if not self.user_name:
                self.hello()
            return func(self)
        return wrapper

    @_hello_decorator
    def recommend_language(self):
        """Show language recommend language to the user."""
        new_recommend_language = self.ranking_model.get_most_popular()
        if not new_recommend_language:
            return None

        will_recommend_languages = [new_recommend_language]
        while True:
            template = console.get_template('greeting.txt', self.speak_color)
            is_yes = input(template.substitute({
                'robot_name': self.name,
                'user_name': self.user_name,
                'language': new_recommend_language
            }))

            if is_yes.lower() == 'y' or is_yes.lower() == 'yes':
                break

            if is_yes.lower() == 'n' or is_yes.lower() == 'no':
                new_recommend_language = self.ranking_model.get_most_popular(
                    not_list = will_recommend_languages)
                if not new_recommend_language:
                    break
                will_recommend_languages.append(new_recommend_language)
    
    @_hello_decorator
    def ask_user_favorite(self):
        """Collect favorite language information from users."""
        while True:
            template = console.get_template(
                'which_language.txt', self.speak_color)
            language = input(template.substitute({
                'robot_name': self.name,
                'user_name': self.user_name,
            }))
            if language:
                self.ranking_model.increment(language)
                break

    @_hello_decorator
    def thank_you(self):
        """Show words appreciation to users."""
        template = console.get_template('good_bye.txt', self.speak_color)
        print(template.substitute({
            'robot_name': self.name,
            'user_name': self.user_name,
        }))
