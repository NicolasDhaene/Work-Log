import string
import os

#Menu Class is to display and query answer based on a list of options
#Menu Class can query answer horizontally (with key being the first letter of the option) or vertically (with key indenting from a,b,c,d,...) 
class Menu():
  def __init__(self, choices, *args, **kwargs):
    self.choices = choices
    self.answer = ""

  def query_answer_vertical(self):
    numbering = string.ascii_lowercase[0:len(self.choices)]
    options = dict(zip(numbering, self.choices))
    trial = 0

    def cls():
      os.system("cls" if os.name == "nt" else "clear")

    while True:
      if trial > 0:
        print("That is not a valid choice, try again")
      print("What would you like to do?")
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
    return self.answer

  def query_answer_horizontal(self):
    capital_letter = []
    beginning_of_word = []
    rest_of_word = []
    for w in self.choices:
      count = 0
      while True:
        if w[count] not in capital_letter:
          capital_letter.append(w[count].upper())
          try:
            beginning_of_word.append(w[:count])
          except ValueError:
            beginning_of_word.append("")
          rest_of_word.append(w[count+1:])
          break
        else:
          count += 1

    def cls():
      os.system("cls" if os.name == "nt" else "clear")

    beg_and_rest = []
    for number in range(len(self.choices)):
      beg_and_rest.append([beginning_of_word[number], rest_of_word[number]])
    options = dict(zip(capital_letter, beg_and_rest))
    trial = 0
    while True:
      if trial > 0:
        print("That is not a valid choice, try again")
      print("Select one of the options below?")
      print("".join(["{0}[{1}]{2}  ".format(value[0], key, value[1]) for key, value in options.items()]))
      self.answer = input(">")
      try:
        options[self.answer.upper()]
      except KeyError:
        trial += 1
        cls()
      else:
        break
    cls()
    return self.answer
