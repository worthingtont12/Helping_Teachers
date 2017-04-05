"""Scans CSV of Student Grades and Notifies Parents of Missing Assignments"""
import re
import smtplib
import pandas as pd
import numpy as np

# import login information
from login_info import *

# Student Gradebook
Gradebook = pd.read_csv("")

# parent emails
parents = pd.read_csv("")

# renaming blank columns
Gradebook = Gradebook.rename(columns={'Unnamed: 0': 'Names'})

# extracting grade weights to calculate later
Weights = Gradebook[Gradebook.Names.isnull()]

# filtering out weights row
Gradebook = Gradebook[~Gradebook.Names.isnull()]

Gradebook = pd.merge(Gradebook, parents, how="left")
# sample for now
Gradebook = Gradebook.head(2)

# Separating name into 3 variables
Gradebook['Last Name'] = Gradebook['Names'].apply(lambda row: str(row).split(',')[0])
Gradebook['First Name'] = Gradebook['Names'].apply(lambda row: (str(row).split(','))[1][1:-11])

# number of columns of interest
numcolumns = len(Gradebook.columns) - len(Gradebook.columns[-3:])

# create id variable and dictionary
keys = np.array(range(0, len(Gradebook)))
Gradebook['id'] = keys
Missing_assignments = dict.fromkeys(keys)

# loop through columns
for i in range(0, numcolumns + 1):
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
    parents_name = Gradebook['Name of parent'][i]

    # grab parents email
    parents_email = Gradebook['Parent Email'][i]

    # grab student email
    student_email = Gradebook['Student Email'][i]

    # check if student actually missing any assignments
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
        message = "Hello " + parents_name + ",\n \n" + students_name + " is missing " + str(number_missing_assignments) + \
            " assignments. The assignments are:\n \n" + \
            str(names_missing_assignments) + "\n \nBest, \n Teacher Name"

        # send email
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
        pass
