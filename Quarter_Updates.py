"""Quarterly Updates to Parents."""
import re
import smtplib
import pandas as pd
import numpy as np

# import login information
from login_info import *

# Student Gradebook
Gradebook = pd.read_csv("/Users/tylerworthington/Desktop/extract (4).csv")
# period2 = pd.read_csv("/Users/tylerworthington/Desktop/extract (5).csv")
# period3 = pd.read_csv("/Users/tylerworthington/Desktop/extract (6).csv")
# period4 = pd.read_csv("/Users/tylerworthington/Desktop/extract (7).csv")
# period5 = pd.read_csv("/Users/tylerworthington/Desktop/extract (8).csv")
# number of columns of interest
numcolumns = len(Gradebook.columns)

# parent emails
parents = pd.read_csv("/Users/tylerworthington/Desktop/Missing Assignments Data - Sheet1.csv")

# renaming blank columns
Gradebook = Gradebook.rename(columns={'Unnamed: 0': 'Names'})

# extracting grade weights to calculate later
Weights = Gradebook[Gradebook.Names.isnull()]

# filtering out weights row
Gradebook = Gradebook[~Gradebook.Names.isnull()]

# Separating name into 3 variables
Gradebook['Last Name'] = Gradebook['Names'].apply(lambda row: str(row).split(',')[0])
Gradebook['First Name'] = Gradebook['Names'].apply(lambda row: (str(row).split())[1])

# common key
Gradebook["Full Name"] = Gradebook['First Name'].map(str) + Gradebook['Last Name']

parents['Last Name'] = parents['Name of Student'].apply(lambda row: str(row).split(',')[0])
parents['First Name'] = parents['Name of Student'].apply(lambda row: (str(row).split())[1])

parents = parents[~parents["Name of Parent"].isnull()]
parents['Parents Last Name'] = parents['Name of Parent'].apply(lambda row: str(row).split(',')[0])
parents['Parents First Name'] = parents['Name of Parent'].apply(
    lambda row: (str(row).split(",")[1]))

# common key
parents["Full Name"] = parents['First Name'].map(str) + parents['Last Name']

Gradebook = pd.merge(Gradebook, parents, how="left")


# create id variable and dictionary
keys = np.array(range(0, len(Gradebook)))
Gradebook['id'] = keys
Missing_assignments = dict.fromkeys(keys)

# loop through columns
for i in range(0, numcolumns):
    # grab column name
    column = Gradebook.columns[i]
    try:
        # find id's of students with grades marked missing
        who_missing = np.where(Gradebook[str(column)] == 'M')[0]
        for j in who_missing:
            # add assignment missing to id of person
            if j in keys:
                try:
                    Missing_assignments[j].append(column)
                except AttributeError:
                    Missing_assignments[j] = [column]
    except TypeError:
        pass

for i in range(0, len(Gradebook['First Name'])):

    # grab students name and lowercase it
    students_name = (Gradebook['First Name'][i]).title()

    # grab parents name
    parents_first_name = (Gradebook['Parents First Name'][i]).title()
    parents_last_name = (Gradebook['Parents Last Name'][i]).title()

    # grab parents email
    parents_email = Gradebook['Parent Email'][i]

    # grab student email
    student_email = Gradebook['Student Email'][i]

    # check if missing
    if Gradebook['Parent Email'][i] is np.nan:
        pass

   # check if student actually missing any assignments
    else:
        if Missing_assignments[i] is not None:

            # how many assignments
            number_missing_assignments = len(Missing_assignments[i])

            # names of assignments
            names_missing_assignments = str(Missing_assignments[i])

            # format names
            names_missing_assignments = names_missing_assignments.strip("[]")
            names_missing_assignments = names_missing_assignments.replace("'", "")
            names_missing_assignments = names_missing_assignments.replace('"', "")
            names_missing_assignments = names_missing_assignments.replace(',', "\n")

            # email to be sent
            message = "Hello" + parents_first_name + " " + parents_last_name + ",\n \nThis is " + \
                teacher_name + ", I teach " + teacher_subject + " at " + \
                teacher_school + ". I will be emailing weekly summaries of " + quarter + \
                " quarter missing assignments to ensure your student ends the school year on the best note possible.\n \nBelow is a summary of " + \
                students_name + "s missing assignments from the " + last_quarter + \
                " quarter. These assignments may not be turned in late unless prior permission has been given, but I want to ensure that we are aspiring to have zero missing assignments in the " + \
                quarter + " quarter of the school year. " + students_name + \
                " missed " + \
                str(number_missing_assignments) + " assignments in the last quarter. " + custom_sentence + \
                " Make sure to be looking for upcoming weekly updates.\n \nThank you,\n" + teacher_name

            message = message.encode('ascii', 'ignore').decode('ascii')

            # send email
            toaddrs = []
            fromaddr = input("teacher_email")
            password = input("password")
            toaddrs.append(parents_email)
            toaddrs.append(student_email)
            msg = "\r\n".join([
                "From: " + fromaddr + "",
                "To: " + parents_email + "",
                "CC: " + student_email + "",
                "Subject: Missing Assignments Update",
                "",
                "" + message + ""
            ])

            # server = smtplib.SMTP()
            # server.connect('smtp.gmail.com', 587)
            # server.ehlo()
            # server.starttls()
            # server.login(teacher_email, password)
            # server.sendmail(fromaddr, toaddrs, msg)
            # server.quit()
        else:
            pass
