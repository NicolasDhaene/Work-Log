import csv
from menus import Menu
import os
import datetime
import re


def cls():
  os.system("cls" if os.name == "nt" else "clear")

MAIN_OPTIONS = ["Add New Entry", "Consult/Edit An Existing Entry", "Quit"]
SEARCH_OPTIONS = ["Exact Date", "Range of Dates", "Exact Search", "Regex Pattern", "Time Spent", "Return to Main Menu"]
CONSULT_OPTIONS = ["Next", "Previous", "Edit", "Delete", "Quit"]
EDITION_OPTIONS = ["Date", "Title", "Time Spent", "Notes"]
results = []


def add_new_entry():
  while True:
    cls()
    while True:
      date_of_task = input("Date of the task: ")
      try:
        test = datetime.datetime.strptime(date_of_task, "%m/%d/%Y")
        break
      except ValueError:
        cls()
        print("Unrecognized date format, please try again. Don't forget to use the 'mm/dd/yyyy' format\n")
    title_of_task = input("Title of the task: ")
    while True:
      time_spent = input("Time spent (rounded minutes): ")
      try:
        test = int(time_spent)
        break
      except ValueError:
        cls()
        print("Time spent is measured in rounded minutes, please try again\n")
        print("Date of the task: ", date_of_task)
        print("Title of the task: ", title_of_task)
    notes = input("Notes (Optional, you can leave this empty):")
    full_entry = [date_of_task, title_of_task, time_spent, notes]
    with open("work_log.csv", "a") as csvFile:
      writer = csv.writer(csvFile)
      writer.writerow(full_entry)
    input("\nThe entry has been add. Press enter to return to the menu")
    cls()
    break


def edit_entry(count):
  EditionMenu = Menu(EDITION_OPTIONS)
  EditionMenu.query_answer_horizontal()
  if EditionMenu.answer.upper() == "D":
    while True:
      print("Date: ", results[count][0])
      print("Title: ", results[count][1])
      print("Time Spent: ", results[count][2])
      print("Notes: ", results[count][3], "\n")
      new_date = input("NEW Date for this task: ")
      try:
        test = datetime.datetime.strptime(new_date, "%m/%d/%Y")
        with open("work_log.csv") as csvfile:
          log_reader = list(csv.reader(csvfile))
          log_reader.remove(results[count])
          results[count][0] = new_date
          log_reader.append(results[count])
        with open("work_log.csv", "w") as csvfile:
          log_writer = csv.writer(csvfile)
          log_writer.writerows(log_reader)
        input("\nYour entry has been updated. Press enter to come back to the main menu")
        cls()
        return results.clear()
        break
      except ValueError:
        cls()
        print("Unrecognized date format, please try again. Don't forget to use the 'mm/dd/yyyy' format\n")
  elif EditionMenu.answer.upper() == "T":
    print("Date: ", results[count][0])
    print("Title: ", results[count][1])
    print("Time Spent: ", results[count][2])
    print("Notes: ", results[count][3], "\n")
    new_title = input("NEW Title for this task: ")
    with open("work_log.csv") as csvfile:
      log_reader = list(csv.reader(csvfile))
      log_reader.remove(results[count])
      results[count][1] = new_title
      log_reader.append(results[count])
    with open("work_log.csv", "w") as csvfile:
      log_writer = csv.writer(csvfile)
      log_writer.writerows(log_reader)
      input("\nYour entry has been updated. Press enter to come back to the main menu")
      cls()
      return results.clear()
  elif EditionMenu.answer.upper() == "I":
    while True:
      print("Date: ", results[count][0])
      print("Title: ", results[count][1])
      print("Time Spent: ", results[count][2])
      print("Notes: ", results[count][3], "\n")
      new_time_spent = input("NEW Time Spent for this task: ")
      try:
        test = int(new_time_spent)
        with open("work_log.csv") as csvfile:
          log_reader = list(csv.reader(csvfile))
          log_reader.remove(results[count])
          results[count][2] = new_time_spent
          log_reader.append(results[count])
        with open("work_log.csv", "w") as csvfile:
          log_writer = csv.writer(csvfile)
          log_writer.writerows(log_reader)
        input("\nYour entry has been updated. Press enter to come back to the main menu")
        cls()
        return results.clear()
        break
      except ValueError:
        cls()
        print("Time Spent is measured in rounded minutes, please try again\n")
  elif EditionMenu.answer.upper() == "N":
    print("Date: ", results[count][0])
    print("Title: ", results[count][1])
    print("Time Spent: ", results[count][2])
    print("Notes: ", results[count][3], "\n")
    new_notes = input("NEW Notes for this task: ")
    with open("work_log.csv") as csvfile:
      log_reader = list(csv.reader(csvfile))
      log_reader.remove(results[count])
      results[count][3] = new_notes
      log_reader.append(results[count])
    with open("work_log.csv", "w") as csvfile:
      log_writer = csv.writer(csvfile)
      log_writer.writerows(log_reader)
      input("\nYour entry has been updated. Press enter to come back to the main menu")
      cls()
      return results.clear()


def delete_entry(count):
  confirmation = input("\nAre you sure you want to delete this entry?\nEnter \"Y\" to confirm. ")
  if confirmation.upper() == "Y":
    with open("work_log.csv") as csvfile:
      log_reader = list(csv.reader(csvfile))
      log_reader.remove(results[count])
    with open("work_log.csv", "w") as csvfile:
      log_writer = csv.writer(csvfile)
      log_writer.writerows(log_reader)
      input("\nYour entry has been deleted. Press enter to come back to the main menu")
      cls()
      return results.clear()
  else:
    cls()
    return results.clear()


def find_entry_exact_date():
  while True:
    exact_date_searched = input("Which date are you looking for? ")
    try:
      test = datetime.datetime.strptime(exact_date_searched, "%m/%d/%Y")
      with open("work_log.csv") as csvfile:
        log_reader = list(csv.reader(csvfile))
        for line in log_reader:
          if line[0] == exact_date_searched:
            results.append(line)
        return results
        break
    except ValueError:
      cls()
      print("Unrecognized date format, please try again. Don't forget to use the 'mm/dd/yyyy' format\n")


def find_entry_range_date():
  while True:
    range1_date_searched = input("From which date are you looking for? ")
    try:
      range1 = datetime.datetime.strptime(range1_date_searched, "%m/%d/%Y")
      break
    except ValueError:
      cls()
      print("Unrecognized date format, please try again. Don't forget to use the 'mm/dd/yyyy' format\n")
  while True:
    range2_date_searched = input("To which date are you looking for? ")
    try:
      range2 = datetime.datetime.strptime(range2_date_searched, "%m/%d/%Y")
      cls()
      break
    except ValueError:
      cls()
      print("Unrecognized date format, please try again. Don't forget to use the 'mm/dd/yyyy' format\n")
      print("From which date (mm/dd/yyyy) are you looking for? ", range1_date_searched)
  with open("work_log.csv") as csvfile:
        log_reader = list(csv.reader(csvfile))
        for line in log_reader:
          linedate = datetime.datetime.strptime(line[0], "%m/%d/%Y")
          if range1 <= linedate <= range2:
            results.append(line)
        return results


def find_entry_exact_search():
  cls()
  title_exact_search = input("What activity are you looking for? ")
  with open("work_log.csv") as csvfile:
    log_reader = list(csv.reader(csvfile))
    for line in log_reader:
      if title_exact_search == line[1]:
        results.append(line)
    return results


def find_entry_regex_pattern():
  cls()
  regex_pattern = input("Please enter Regex pattern: ")
  with open("work_log.csv") as csvfile:
    log_reader = list(csv.reader(csvfile))
    for line in log_reader:
      string = ''.join([line[1], line[3]])
      if re.findall(regex_pattern, string):
        results.append(line)
    return results


def find_entry_time_spent():
  while True:
    time_spent_searched = input("Please enter time spent (rounded minutes) on assignment: ")
    try:
      test = int(time_spent_searched)
      with open("work_log.csv") as csvfile:
        log_reader = list(csv.reader(csvfile))
        for line in log_reader:
          if time_spent_searched == line[2]:
            results.append(line)
        return results
        break
    except ValueError:
      cls()
      print("Time spent is measured in rounded minutes, please try again\n")


def display_results():
  count = 0
  while True:
    if not results:
      print("No result found. Sorry\n")
      break
    else:
      cls()
      print("We found {} item(s) in the log matching your search criteria\n".format(len(results)))
      print("Date: ", results[count][0])
      print("Title: ", results[count][1])
      print("Time Spent: ", results[count][2])
      print("Notes: ", results[count][3], "\n")
      if len(results) == 1:
        available_options = [option for option in CONSULT_OPTIONS if option is not "Previous" and option is not "Next"]
      else:
        if count == 0:
          available_options = [option for option in CONSULT_OPTIONS if option is not "Previous"]
        elif count == len(results)-1:
          available_options = [option for option in CONSULT_OPTIONS if option is not "Next"]
        else:
          available_options = CONSULT_OPTIONS
      ConsultMenu = Menu(available_options)
      ConsultMenu.query_answer_horizontal()
      if ConsultMenu.answer.upper() == "N":
        count += 1
      elif ConsultMenu.answer.upper() == "P":
        count -= 1
      elif ConsultMenu.answer.upper() == "E":
        edit_entry(count)
        break
      elif ConsultMenu.answer.upper() == "D":
        delete_entry(count)
        break
      elif ConsultMenu.answer.upper() == "Q":
        return results.clear()
        break


print("Welcome to Work Log")
print("-"*len("Welcome to Work Log"))
# Implemented the differents menus as instances of Menu class.
# Each Menu runs in a while loop in order to be able to break in case of quit/return to main menu command
MainMenu = Menu(MAIN_OPTIONS)
while MainMenu.answer != "c":
  MainMenu.query_answer_vertical()
  if MainMenu.answer == "a":
    add_new_entry()
  elif MainMenu.answer == "b":
    SearchMenu = Menu(SEARCH_OPTIONS)
    while SearchMenu.answer != "e":
      SearchMenu.query_answer_vertical()
      if SearchMenu.answer == "a":
        find_entry_exact_date()
        display_results()
        break
      elif SearchMenu.answer == "b":
        find_entry_range_date()
        display_results()
        break
      elif SearchMenu.answer == "c":
        find_entry_exact_search()
        display_results()
        break
      elif SearchMenu.answer == "d":
        find_entry_regex_pattern()
        display_results()
        break
      elif SearchMenu.answer == "e":
        find_entry_time_spent()
        display_results()
        break
  else:
    break
