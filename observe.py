import sys
import pandas as pd
import time
import matplotlib.pyplot as plt

COLUMNS_TO_OBSERVE = ["pledged %", "lifetime_in_days", "backers_count", "goal"]


def observe():
    df = pd.read_csv("Deduped_Master.csv", error_bad_lines=False) #capture data frame
    master_length = len(df.index)
    print "FUNC := observe \nDeduped_Master.csv row count: ", master_length
    results = {}
    for col in COLUMNS_TO_OBSERVE:
        print "Attribute: ", col
        results[col] = {
            "min": df[col].min(),
            "max": df[col].max(),
            "mean": df[col].mean(),
            "median": df[col].median(),
            "Q1": df[col].quantile(0.25),
            "Q2": df[col].quantile(0.50),
            "Q3": df[col].quantile(0.75),
            "Q4": df[col].quantile(1),
            "std": df[col].std(),
            "var": df[col].var()
        }
    return results

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
                f.write("\nRange of attr")
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
    df = pd.read_csv("Deduped_Master.csv", error_bad_lines=False) #capture data frame
    # df.plot.box(vert=False, column=["pledged %", "state"])
    # df.boxplot(by='state', column = 'pledged %', grid=True)
    # df.boxplot(by='category', column='pledged %', grid=True)
    # df.boxplot(by='category', column='lifetime_in_days', grid=True)
    # df.boxplot(by='state', column='lifetime_in_days', grid=True)
    # df.boxplot(by='category', column='backers_count', grid=True)
    # df.boxplot(by='category', column='goal', grid=True)
    df.boxplot(by='state', column='goal', grid=True)
    #df.boxplot(by='category', column='state', grid=True)

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

    if dispersal:
        print "Running in disperal mode"
        output_to_file(observe(), "dispersal")
    elif display:
        print "Displaying boxplot" 
        display_boxplot()
    elif remove_dups:
        df = pd.read_csv("Master.csv", error_bad_lines=False)
        df = df.drop_duplicates(subset='id', keep='first', inplace=False)
        df.to_csv('Deduped_Master.csv', index=False)

if __name__ == "__main__":
    main()
