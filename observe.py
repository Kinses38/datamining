import sys
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns

COLUMNS_TO_OBSERVE = ["pledged %", "lifetime_in_days", "backers_count", "goal"]


def observe():
    df = pd.read_csv("Deduped_Master.csv", error_bad_lines=False)  # capture data frame
    master_length = len(df.index)
    print "FUNC := observe \nDeduped_Master.csv row count: ", master_length
    results = {}
    for col in COLUMNS_TO_OBSERVE:
        stats = pd.DataFrame([df[col].min(), df[col].max(), (df[col].max() - df[col].min()), df[col].mean(),
                              df[col].median(), df[col].quantile(0.25), df[col].quantile(0.5), df[col].quantile(0.75),
                              df[col].quantile(1), (df[col].quantile(0.75) - df[col].quantile(0.25)), df[col].std(),
                              df[col].var()],
                             index=["Min: ", "Max: ", "Range: ", "Mean: ", "Median: ", "Q1: ", "Q2: ", "Q3: ",
                                    "Q4: ", "IQR: ", "STD: ", "Variance: "])
        pd.options.display.float_format = '{0:,.2f}'.format
        print ("Atrribute: " + col)
        print (stats.to_string())
        print "\n"


def output_to_file(data_dict, flag):
    print "FUNC := output_to_file"
    if flag == "dispersal":
        filename = str(time.time()) + "_dispersal_results.txt"
        with open(filename, 'w') as f:
            for key, values in data_dict.iteritems():
                f.write("\n\n--!!Attribute: ")
                f.write(str(key))
                f.write("!!--\n")
                f.write("\nMin value: ")
                f.write(str(values["min"]))
                f.write("\nMax value: ")
                f.write(str(values["max"]))
                f.write("\nRange of attr: ")
                f.write(str(values["max"] - values["min"]))
                f.write("\nMedian value: ")
                f.write(str(values["median"]))
                f.write("\nStandard Deviation: ")
                f.write(str(values["std"]))
                f.write("\nVariance: ")
                f.write(str(values["var"]))
                f.write("\nQ1: ")
                f.write(str(values["Q1"]))
                f.write("\nQ2: ")
                f.write(str(values["Q2"]))
                f.write("\nQ3: ")
                f.write(str(values["Q3"]))
                f.write("\nQ4: ")
                f.write(str(values["Q4"]))
                f.write("\nIQR")
                f.write(str(values["Q3"] - values["Q1"]))
    return


def display_boxplot():
    # df = pd.read_csv("Deduped_Master.csv", error_bad_lines=False)  # capture data frame
    df = pd.read_csv("Cat_Master.csv", error_bad_lines=False)
    # df.plot.box(vert=False, column=["pledged %", "state"])
    # df.boxplot(by='state', column = 'pledged %', grid=True)
    # df.boxplot(by='category', column='pledged %', grid=True)
    # df.boxplot(by='category', column='lifetime_in_days', grid=True)
    # df.boxplot(by='state', column='lifetime_in_days', grid=True)
    # df.boxplot(by='category', column='backers_count', grid=True)
    # df.boxplot(by='category', column='goal', grid=True)
    # df.boxplot(by='state', column='goal', grid=True)
    # df.boxplot(by='category', column='state', grid=True)
    sns.boxplot(x="category", y="pledged %", data=df)
    plt.show()


def display_heatmap(file_name):
    df = pd.read_csv(file_name, error_bad_lines=False)
    df = df.pivot_table("pledged %", "category", "country")
    hm = sns.heatmap(df)
    plt.show()

def main():
    dispersal = True
    display = False
    central_tendancy = False
    graphics = False
    remove_dups = False

    if len(sys.argv) > 1:
        if sys.argv[1] == "dispersal":
            dispersal = True
        elif sys.argv[1] == "display":
            display = True
            dispersal = False
        elif sys.argv[1] == "dups":
            remove_dups = True
            dispersal = False
        elif sys.argv[1] == "heatmap":
            display_heatmap(sys.argv[2])


    if dispersal:
        print "Running in disperal mode"
        observe()
    elif display:
        print "Displaying boxplot"
        display_boxplot()
    elif remove_dups:
        df = pd.read_csv("Master.csv", error_bad_lines=False)
        df = df.drop_duplicates(subset='id', keep='first', inplace=False)
        df.to_csv('Deduped_Master.csv', index=False)


if __name__ == "__main__":
    main()
