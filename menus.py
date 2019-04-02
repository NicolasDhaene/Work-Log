import string
import os


class Menu():
    def __init__(self, choices, output, *args, **kwargs):
        self.choices = choices
        self.answer = ""
        self.output = output

    def query_answer_vertical(self):
        numbering = string.ascii_lowercase[0:len(self.choices)]
        options = dict(zip(numbering, self.choices))
        trial = 0

        def cls():
            os.system("cls" if os.name == "nt" else "clear")

        while True:
            if trial > 0:
                print("That is not a valid choice, try again")
            print("Select one of the options below:")
            for key, value in options.items():
                print(key, ") ", value)
            self.answer = input(">")
            try:
                options[self.answer]
            except KeyError:
                trial += 1
                cls()
            else:
                break
        cls()
        if self.output == "key":
            return self.answer
        if self.output == "value":
            return options[self.answer]

    def query_answer_horizontal(self):
        capital_letter = []
        beg_of_word = []
        rest_of_word = []
        for w in self.choices:
            count = 0
            while True:
                if w[count] not in capital_letter:
                    capital_letter.append(w[count].upper())
                    try:
                        beg_of_word.append(w[:count])
                    except ValueError:
                        beg_of_word.append("")
                    rest_of_word.append(w[count+1:])
                    break
                else:
                    count += 1

        def cls():
            os.system("cls" if os.name == "nt" else "clear")

        beg_and_rest = []
        for number in range(len(self.choices)):
            beg_and_rest.append([beg_of_word[number], rest_of_word[number]])
        options = dict(zip(capital_letter, beg_and_rest))
        trial = 0
        while True:
            if trial > 0:
                print("That is not a valid choice, try again")
            print("Select one of the options below:")
            print("".join(["{0}[{1}]{2}  ".format(value[0], key, value[1])
                  for key, value in options.items()]))
            self.answer = input(">")
            try:
                options[self.answer.upper()]
            except KeyError:
                trial += 1
                cls()
            else:
                break
        cls()
        if self.output == "key":
            return self.answer
        if self.output == "value":
            return options[self.answer]
