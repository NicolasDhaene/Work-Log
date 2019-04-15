from menus import Menu
from work_log_entry import WorkLogEntry
import os
import datetime


def cls():
    os.system("cls" if os.name == "nt" else "clear")


MAIN_OPTIONS = ["Add New Entry", "Lookup Entry", "Quit"]
LOOKUP_OPTIONS = ["Employee",
                  "Exact Date",
                  "Range of Dates",
                  "Task or Notes",
                  "Time Spent",
                  "Return to Main Menu"]
CONSULT_OPTIONS = ["Next", "Previous", "Edit", "Delete", "Quit"]
EDITION_OPTIONS = ["Date", "Title", "Time Spent", "Notes"]


def is_valid_date(date):
    try:
        datetime.datetime.strptime(date, "%m/%d/%Y")
        return True
    except ValueError:
        print("Unrecognized date format,",
              "please try again.",
              "Don't forget to use the 'mm/dd/yyyy' format ")
        return False

        
def is_valid_integer(time_spent):
    try:
        int(time_spent)
        return True
    except ValueError:
        print("Time spent is measured in rounded minutes,",
              "please try again\n")
        return False

def get_employee_name():
    while True:
        employee_name = input("Employee Name: ")
        if len(employee_name) != 0:
            return employee_name
        else:
            print("You need to type an employee name")

def get_task_date():
    while True:
        date = input("Date (mm/dd/yyyy) of the task: ")
        if is_valid_date(date):
            date = datetime.datetime.strptime(date, "%m/%d/%Y")
            return date
            break

def get_task_name():
        while True:
            task_name = input("Task Name: ")
            if len(task_name) != 0:
                return task_name
            else:
                print("You need to type a task name")

def get_time_spent():
    while True:
        time_spent = input("Time spent (rounded minutes): ")
        if is_valid_integer(time_spent):
            time_spent = int(time_spent)
            return time_spent
            break

def get_notes():
    notes = input("Notes (optional): ")
    return notes

def add_new_entry():
    employee_name = get_employee_name()
    date = get_task_date()
    task_name = get_task_name()
    time_spent = get_time_spent()
    notes = get_notes()
    WorkLogEntry.create(employee=employee_name,
                        date=date,
                        task_name=task_name,
                        time_spent=time_spent,
                        notes=notes)
    input("\nThe entry has been add. Press enter to continue")
    cls()

def employee():
    employee_searched = input("Which Employee are you looking for? ")
    employee_list = []
    search1 = WorkLogEntry.select().where(
        WorkLogEntry.employee.contains(employee_searched))
    for each in search1:
        if each.employee not in employee_list:
            employee_list.append(each.employee)
    if len(employee_list) > 1:
        cls()
        print("Which", employee_searched, "more specifically?\n")
        EmployeeMenu = Menu(employee_list, "value", "asis")
        employee_searched_specific = EmployeeMenu.query_answer_vertical()
        return WorkLogEntry.select().where(
            WorkLogEntry.employee == employee_searched_specific)
    else:
        return WorkLogEntry.select().where(
            WorkLogEntry.employee.contains(employee_searched))

def exact_date():
    while True:
        exact_date = input("Which date (mm/dd/yyyy) are you looking for? ")
        if is_valid_date(exact_date):
            exact_date = datetime.datetime.strptime(exact_date, "%m/%d/%Y")
            cls()
            break
    return WorkLogEntry.select().where(WorkLogEntry.date == exact_date)    

def range_of_dates():
    while True:
        range1_date = input("From which date are you looking for? ")
        if is_valid_date(range1_date):
            range1 = datetime.datetime.strptime(range1_date, "%m/%d/%Y")
            cls()
            break
    while True:
        range2_date = input("To which date are you looking for? ")
        if is_valid_date(range2_date):
            range2 = datetime.datetime.strptime(range2_date, "%m/%d/%Y")
            cls()
            break
    return WorkLogEntry.select().where(
        (WorkLogEntry.date >= range1) & (WorkLogEntry.date <= range2))
    cls()

def task_or_notes():
    term_searched = input("Enter search term: ")
    return WorkLogEntry.select().where(
        (WorkLogEntry.task_name.contains(term_searched)) |
        (WorkLogEntry.notes.contains(term_searched)))
    cls()


def time_spent():
    while True:
        time_spent = input("How long was the task you are looking for?")
        if is_valid_integer(time_spent):
            break
    return WorkLogEntry.select().where(WorkLogEntry.time_spent == time_spent)
    cls()

def display_entry(results, count):
    print("This is result {} of {}".format(count+1, len(results)),
          "matching your search criteria:\n")
    print("Employee: ", results[count].employee)
    print("Date: ", results[count].date)
    print("Task: ", results[count].task_name)
    print("Time Spent: ", results[count].time_spent)
    print("Notes: ", results[count].notes, "\n")

def check_if_no_result(results):
    if not results:
        return True
        print("No result found. Sorry\n")
        input("")
        cls()
    else:
        return False

def define_navigation_options(results, count):
    if len(results) == 1:
        available_options = [option for option in CONSULT_OPTIONS
                             if option != "Previous" and
                             option != "Next"]
    else:
        if count == 0:
            available_options = [option for option in CONSULT_OPTIONS
                                 if option != "Previous"]
        elif count == len(results)-1:
            available_options = [option for option in CONSULT_OPTIONS
                                 if option != "Next"]
        else:
            available_options = CONSULT_OPTIONS
    return available_options

def navigate_results(results):
    count = 0
    while True:
        if check_if_no_result(results):
            break
        else:
            cls()
            display_entry(results, count)
            ConsultMenu = Menu(define_navigation_options(results, count), "key", "lc")
            ConsultMenu.query_answer_horizontal()
            if ConsultMenu.answer.upper() == "N":
                count += 1
            elif ConsultMenu.answer.upper() == "P":
                count -= 1
            elif ConsultMenu.answer.upper() == "E":
                edit_entry(results[count])
                break
            elif ConsultMenu.answer.upper() == "D":
                delete_entry(results[count])
                break
            elif ConsultMenu.answer.upper() == "Q":
                break

def delete_entry(entry):
    print("Employee: ", entry.employee)
    print("Date: ", entry.date)
    print("Task: ", entry.task_name)
    print("Time Spent: ", entry.time_spent)
    print("Notes: ", entry.notes, "\n")
    confirmation = input("Delete this entry?\nEnter \"Y\" to confirm. ")
    if confirmation.upper() == "Y":
        entry.delete_instance()
        input("\nYour entry has been deleted.")
    cls()


def edit_entry(entry):
    descriptionlist = ["Employee",
                       "Date",
                       "Task",
                       "Time Spent",
                       "Notes"]
    count = 0
    for fields in descriptionlist:
        entrylist = [entry.employee,
                     entry.date,
                     entry.task_name,
                     entry.time_spent,
                     entry.notes]
        count2 = 0
        for item in range(count+1):
            print(descriptionlist[count2], " :", entrylist[count2])
            count2 += 1
        question = ("\n" +
                    "Would you like to update the " +
                    descriptionlist[count] +
                    " field ? (Y/N) ")
        if input(question).upper() == "Y":
            if descriptionlist[count] == "Date":
                while True:
                    new_value = input("New value? ")
                    if is_valid_date(new_value):
                        entrylist[count] = new_value
                        cls()
                        break
            elif descriptionlist[count] == "Time Spent":
                while True:
                    new_value = input("New value? ")
                    if is_valid_integer(new_value):
                        entrylist[count] = new_value
                        cls()
                        break
            else:
                new_value = input("New value? ")
                entrylist[count] = new_value
            entry.employee = entrylist[0]
            entry.date = entrylist[1]
            entry.task_name = entrylist[2]
            entry.time_spent = entrylist[3]
            entry.notes = entrylist[4]
            entry.save()
        count += 1
        cls()

    print("Entry was updated to:\n")
    count = 0
    for fields in descriptionlist:
        print(descriptionlist[count], " :", entrylist[count])
        count += 1
    input("")
    cls()


if __name__ == "__main__":
    cls()
    print("Welcome to Work Log - Now With Database!")
    print("-"*len("Welcome to Work Log - Now With Database!"))
    MainMenu = Menu(MAIN_OPTIONS, "key", "lc")
    while MainMenu.answer != "c":
        MainMenu.query_answer_vertical()
        if MainMenu.answer == "a":
            add_new_entry()
        elif MainMenu.answer == "b":
            LookupMenu = Menu(LOOKUP_OPTIONS, "value", "lc")
            try:
                navigate_results(eval(LookupMenu.query_answer_vertical())())
            except NameError:
                pass
