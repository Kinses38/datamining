import pandas as pd
import os
import datetime
import dateutil.relativedelta
import json
import time

DROP_COLUMNS = ['blurb', 'converted_pledged_amount', 'currency', 'currency_symbol', 'currency_trailing_code',
                'current_currency', 'disable_communication', 'friends', 'fx_rate', 'is_backing', 'is_starrable',
                'is_starred', 'location', 'name', 'permissions', 'photo', 'profile', 'slug', 'source_url', 'spotlight',
                'static_usd_rate', 'urls', 'usd_pledged', 'usd_type']


def remove_columns(c, cols=DROP_COLUMNS):
    name = c
    print 'FUNC :- remove_columns CSV:', name
    try:
        c = pd.read_csv(c, error_bad_lines=False)
        c.drop(cols, axis=1, inplace=True)  # drop the entire column axis = 1 indicates a column
        c.to_csv(name, index=False)
    except Exception, err:
        print Exception, err


def parse_json_category(c, column_name, field):
    name = c
    print 'FUNC :- Get Json field:', name
    try:
        c = pd.read_csv(c, error_bad_lines=False)
        for index, row in c.iterrows():
            blob = row[column_name]
            json_data = json.loads(blob)
            slug = json_data[field]
            sep_slug = slug.split('/')
            joined_slug = sep_slug[0].replace(" ", "_")
            # print joined_slug
            c.loc[c.index[index], column_name] = joined_slug
        c.to_csv(name, index=False)
    except Exception, err:
        print Exception, err


def parse_json_creator(c):
    name = c
    print 'FUNC :- Get Json field', name
    try:
        c = pd.read_csv(c, error_bad_lines=False)
        for index, row in c.iterrows():
            blob = row['creator']
            pre_creator = blob.split("name\":")[1]
            creator = pre_creator.split("\",\"")[0].replace("\"", "")
            # print creator
            c.loc[c.index[index], 'creator'] = creator
        c.to_csv(name, index=False)
    except Exception, err:
        print Exception, err


def create_lifetime_in_days(c):
    cols = ['deadline', 'launched_at']
    name = c
    print 'FUNC :- create_lifetime_in_days CSV:', name
    try:
        c = pd.read_csv(c, error_bad_lines=False)
        c['lifetime_in_days'] = ''
        for index, row in c.iterrows():
            deadline = datetime.datetime.fromtimestamp(row['deadline'])
            launched_at = datetime.datetime.fromtimestamp(row['launched_at'])
            lifetime_in_days = dateutil.relativedelta.relativedelta(deadline, launched_at)
            # print lifetime_in_days
            daysToAdd = 0
            daysToAdd += lifetime_in_days.years * 365  # convert years to days
            daysToAdd += lifetime_in_days.months * 30  # convert months to days
            if lifetime_in_days.hours >= 12:
                lifetime_in_days.days += 1
            lifetime_in_days.days += daysToAdd
            lifetime_in_days = lifetime_in_days.days
            c.loc[c.index[index], 'lifetime_in_days'] = lifetime_in_days
        c.to_csv(name, index=False)
    except Exception, err:
        print Exception, err


def create_until_state_changed_in_days(c):
    cols = ['state_changed_at', 'launched_at']
    name = c
    print 'FUNC :- create_until_state_changed_in_days CSV:', name
    try:
        c = pd.read_csv(c, error_bad_lines=False)
        c['until_state_changed_in_days'] = ''  # creating new column
        for index, row in c.iterrows():  # iterate through rows
            state_changed = datetime.datetime.fromtimestamp(row['state_changed_at'])  # grab state_changed_at timestamp
            launched_at = datetime.datetime.fromtimestamp(row['launched_at'])  # grab launched_at timestamp
            until_state_changed_in_days = dateutil.relativedelta.relativedelta(state_changed,
                                                                               launched_at)  # subtract the two timestamps. Output is in years, months, days, minutes
            # print until_state_changed_in_days
            daysToAdd = 0
            daysToAdd = until_state_changed_in_days.years * 365  # convert years to days
            daysToAdd += until_state_changed_in_days.months * 30  # convert months to days
            if until_state_changed_in_days.hours >= 12:
                until_state_changed_in_days.days += 1
            until_state_changed_in_days.days += daysToAdd
            until_state_changed_in_days = until_state_changed_in_days.days
            c.loc[c.index[index], 'until_state_changed_in_days'] = until_state_changed_in_days  # write to the cell
        c.to_csv(name, index=False)
    except Exception, err:
        print Exception, err


def main():
    # Get the list of CSV's in the current directory
    cDir_files = os.listdir(".")
    CSV_files = []
    for item in cDir_files:
        if ".csv" in item:
            # TESTING: and "test" in item and "$" not in item:
            CSV_files.append(item)
    del cDir_files

    start = time.time()
    # Remove the rubbish columns
    for CSV in CSV_files:
        remove_columns(CSV)
        create_lifetime_in_days(CSV)
        create_until_state_changed_in_days(CSV)
        remove_columns(CSV, ['state_changed_at', 'launched_at', 'deadline'])
        parse_json_category(CSV, 'category', 'slug')
        parse_json_creator(CSV)
        print "Completed ", CSV
    end = time.time()
    print "Total time: ", end - start


if __name__ == "__main__":
    main()
