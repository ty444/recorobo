

class FirstQuestions:
    bar1 = "\n==================================================\n Hi, What's your name ?? \n=================================================="
    bar2 = "\n==================================================\n"

    def __init__(self):
        # user input name
        print(self.bar1)
        user_name = input("→ :")
        self.question1(user_name)

    def question1(self, name):
        print(self.bar2)
        print("{}".format(name) + "!! " + "Where restaurant do you like??")
        print(self.bar2)




o = FirstQuestions()
