import pandas as pd


def remove_dups(file_name):

    df = pd.read_csv(file_name, error_bad_lines=False)
    df = df.drop_duplicates(subset='id', keep='first', inplace=False)
    df.to_csv('Deduped_Master.csv', index=False)
    print "Completed removing duplicates and trimmed on file: " + file_name


def trim(file_name):
    df = pd.read_csv(file_name, error_bad_lines=False)
    # for_pledged%

    # df = df.sort_values(by=['pledged %'])
    # df = df.iloc[1000:]
    # df = df.iloc[:-9000]

    # for_goal
    # df = df.sort_values(by=['goal'])
    # df = df.iloc[1000:]
    # df = df.iloc[:-6000]  # see screenshots of 5-number for this category

    # for_for_backers_count
    # df = df.sort_values(by=['backers_count'])
    # df = df.iloc[3000:]
    # df = df.iloc[:-5000]  # see screenshots of 5-number for this category

    # filter projects and return those with goals higher than:
    df = df[df['goal'] >= 200]
    # filter projectss and return those with goals less than:
    df = df[df['goal'] <= 750000]

    df.to_csv('Trimmed_Deduped_Master.csv', index=False)
    print "Completed trimming on file: " + file_name


def categorise_pledged(file_name, output_file):

    df = pd.read_csv(file_name, error_bad_lines=False)
    df = df.sort_values(by=['pledged %'])

    # Changed to numerical labels for plotting. Also put infinte upper bound on it to include stupid pledges.
    df['pledged %'] = pd.cut(df['pledged %'], bins=[-1, 49, 99, 149, float("inf")],
                             labels=[0, 1, 2, 3])
    df.to_csv(output_file, index=False)
    print "Completed changing pledged to categories in file: " + file_name + " to: " + output_file


def main():
    remove_dups("Master.csv")
    trim("Deduped_Master.csv")

    # This is for non-trimmed. Need to add for trimmed if we want
    categorise_pledged("Deduped_Master.csv", "Cat_Master.csv")
    # Trimmed
    categorise_pledged("Trimmed_Deduped_Master.csv", "Trimmed_Cat_Master.csv")


if __name__ == "__main__":
    main()
