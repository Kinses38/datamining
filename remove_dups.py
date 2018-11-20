import pandas as pd


def remove_dups_and_trim(file_name):

    df = pd.read_csv(file_name, error_bad_lines=False)
    df = df.drop_duplicates(subset='id', keep='first', inplace=False)

    # for_pledged%
    df = df.sort_values(by=['pledged %'])

    #df = df.iloc[1000:]
    #df = df.iloc[:-9000]

    # for_goal
    # df = df.sort_values(by=['goal'])
    # df = df.iloc[1000:]
    # df = df.iloc[:-6000]  # see screenshots of 5-number for this category

    # for_for_backers_count
    # df = df.sort_values(by=['backers_count'])
    # df = df.iloc[3000:]
    # df = df.iloc[:-5000]  # see screenshots of 5-number for this category

    df.to_csv('Deduped_Master.csv', index=False)
    print "Completed removing duplicates and trimmed"


def categorise_pledged(file_name):

    df = pd.read_csv(file_name, error_bad_lines=False)
    df = df.sort_values(by=['pledged %'])
    df['pledged %'] = pd.cut(df['pledged %'], bins=[-1, 50, 100, 150, 99999], labels=['flop', 'fail', 'success', 'unicorn'])
    df.to_csv('Cat_Master.csv', index=False)
    print "Completed changing pledged to categories in file " + file_name

def main():
    remove_dups_and_trim("Master.csv")
    categorise_pledged("Deduped_Master.csv")


if __name__ == "__main__":
    main()
