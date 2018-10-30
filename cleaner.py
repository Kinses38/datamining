# -*- coding: utf-8 -*-
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
            creator = pre_creator.split("\",\"")[0].replace("\"", "").replace(" ", "_").replace("'", "")

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


def classify_created_at(c):
    cols = ['created_at']
    name = c
    print 'FUNC :- classify_created_at CSV:', name
    try:
        c = pd.read_csv(c, error_bad_lines=False)
        c['quarter_created_at'] = ''
        c['year_created_at'] = ''
        for index, row in c.iterrows():
            created_at = datetime.datetime.fromtimestamp(row['created_at'])
            created_at = str(created_at).split("-")

            # Creating season quartile
            if int(created_at[1]) < 4:
                c.loc[c.index[index], 'quarter_created_at'] = 1
            elif int(created_at[1]) < 7:
                c.loc[c.index[index], 'quarter_created_at'] = 2
            elif int(created_at[1]) < 10:
                c.loc[c.index[index], 'quarter_created_at'] = 3
            elif int(created_at[1]) < 13:
                c.loc[c.index[index], 'quarter_created_at'] = 4
            else:
                c.loc[c.index[index], 'quarter_created_at'] = "ERROR!"

            # fill year_created_at
            c.loc[c.index[index], 'year_created_at'] = created_at[0]

        c.to_csv(name, index=False)
    except Exception, err:
        print Exception, err

def get_target_goal_percent(c):
    name = c
    print 'FUNC :- Converting Pledged to P/G at CSV:', name
    try:
        c = pd.read_csv(c, error_bad_lines=False)
        for index, row in c.iterrows():
            goal =  row['goal']
            pledged = row['pledged']
            p_over_g = pledged / goal
            #to two sign decimal places
            formatted_p_over_g = "{:.2f}".format(p_over_g * 100)
            c.loc[c.index[index], 'pledged'] = formatted_p_over_g
        c.rename(columns={'pledged':'pledged %'}, inplace=True  )
        c.to_csv(name, index=False)
    except Exception, err:
        print Exception,

def calculate_var_mean_std(c, column_name):
    #This should be calculating a master csv file of all our training data.
    name = c
    print 'FUNC :- Calculating Variance: '
    try:
        c = pd.read_csv(c, error_bad_lines=False)
        stats = pd.DataFrame([c[column_name].var(), c[column_name].mean(), c[column_name].std()], index=['Variance', 'Mean', 'Standard Dev'])
        pd.set_option('display.float_format', lambda x: '%.3f' % x)
        print (stats.to_string())
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
        classify_created_at(CSV)
        remove_columns(CSV, ['created_at', 'state_changed_at', 'launched_at', 'deadline'])
        parse_json_category(CSV, 'category', 'slug')
        parse_json_creator(CSV)
        get_target_goal_percent(CSV)
        print calculate_var_mean_std(CSV, 'pledged %')
        print "Completed ", CSV
    end = time.time()
    print "Total time: ", end - start


if __name__ == "__main__":
    main()
