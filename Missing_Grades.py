"""Scans CSV of Student Grades and Notifies Parents of Missing Assignments"""
import re
import smtplib
import pandas as pd
import numpy as np

# import login information
from login_info import *

# Student Gradebook
Gradebook = pd.read_csv("")

# number of columns of interest
numcolumns = len(Gradebook.columns)

# parent emails
parents = pd.read_csv("")

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

# merge df
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

# raw input
teacher_email = input("teacher_email: ")
password = input("password: ")

for i in range(0, len(Gradebook['First Name'])):

    # grab students name and lowercase it
    students_name = (Gradebook['First Name'][i]).title()

    # grab student email
    student_email = Gradebook['Student Email'][i]
    # grab parents name
    if Gradebook['Parent Email'][i] is np.nan:
        pass

   # check if student actually missing any assignments
    else:
        parents_first_name = (Gradebook['Parents First Name'][i]).title()
        parents_last_name = (Gradebook['Parents Last Name'][i]).title()
        # grab parents email
        parents_email = Gradebook['Parent Email'][i]

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
            message = "Hello " + parents_first_name + " " + parents_last_name + ",\n \n" + students_name + " is missing the following assignments in " + teacher_subject + " this week at " + teacher_school + \
                ". In order to end the school year on the best note possible, let's strive to have zero missing assignments this quarter. Missing assignments are below and should be made-up as soon as possible.\n \n Missing Assignments:\n" + \
                names_missing_assignments + "\n \nThank you,\n" + teacher_name + \
                "\n " + teacher_subject + "\n " + teacher_school

            fromaddr = teacher_email
            toaddrs = parents_email
            msg = "\r\n".join([
                "From: " + fromaddr + "",
                "To: " + toaddrs + "",
                "Subject: Missing Assignments Update",
                "",
                "" + message + ""
            ])

            server = smtplib.SMTP()
            server.connect('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(teacher_email, password)
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()

        else:
            # message to parent
            message = "Hello " + parents_first_name + " " + parents_last_name + ",\n \n" + \
                students_name + " is missing zero assignments this week in " + teacher_subject + " at " + teacher_school + \
                ". Please congratulate them on all their hard work and dedication this week. \n \nThank you,\n" + teacher_name + \
                "\n " + teacher_subject + "\n " + teacher_school

            # send email
            fromaddr = teacher_emailimport
            toaddrs = parents_email
            msg = "\r\n".join([
                "From: " + fromaddr + "",
                "To: " + toaddrs + "",
                "Subject: Missing Assignments Update",
                "",
                "" + message + ""
            ])

            server = smtplib.SMTP()
            server.connect('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(teacher_email, password)
            server.sendmail(fromaddr, toaddrs, msg)
            server.quit()
