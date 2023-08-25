#!/usr/bin/env python3

import csv
import datetime
import requests

FILE_URL = "https://storage.googleapis.com/gwg-content/gic215/employees-with-date.csv"

def get_start_date():
    """Interactively get the start date to query for."""
    print()
    print('Getting the first start date to query for.')
    print()
    print('The date must be greater than Jan 1st, 2018')
    year = int(input('Enter a value for the year: '))
    month = int(input('Enter a value for the month: '))
    day = int(input('Enter a value for the day: '))
    print()

    return datetime.datetime(year, month, day)

def get_file_lines(url):
    """Returns the lines contained in the file at the given URL"""

    # Download the file over the internet
    response = requests.get(url, stream=True)
    lines = []

    for line in response.iter_lines():
        lines.append(line.decode("UTF-8"))
    return lines

def preprocess_data(url):
    """Download and preprocess the file data"""
    lines = get_file_lines(url)
    data = [line.split(',') for line in lines[1:]]
    sorted_data = sorted(data, key=lambda row: datetime.datetime.strptime(row[3], '%Y-%m-%d'))
    return sorted_data

def get_same_or_newer(preprocessed_data, start_date):
    """Returns the employees that started on the given date, or the closest one."""
    min_date = datetime.datetime.today()
    min_date_employees = []

    for row in preprocessed_data:
        row_date = datetime.datetime.strptime(row[3], '%Y-%m-%d')

        if row_date < start_date:
            continue

        if row_date < min_date:
            min_date = row_date
            min_date_employees = []

        if row_date == min_date:
            min_date_employees.append("{} {}".format(row[0], row[1]))

    return min_date, min_date_employees

def main():
    start_date = get_start_date()
    preprocessed_data = preprocess_data(FILE_URL)
    list_newer(preprocessed_data, start_date)

def list_newer(preprocessed_data, start_date):
    while start_date < datetime.datetime.today():
        start_date, employees = get_same_or_newer(preprocessed_data, start_date)
        print("Started on {}: {}".format(start_date.strftime("%b %d, %Y"), employees))
        start_date = start_date + datetime.timedelta(days=1)

if __name__ == "__main__":
    main()
