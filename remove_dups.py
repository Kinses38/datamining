import pandas as pd



def main():
    df = pd.read_csv('Master.csv', error_bad_lines=False)
    df = df.drop_duplicates(subset='id', keep='first', inplace=False)
    df = df.sort_values(by=['pledged %'])
    df = df.iloc[:-3000]
    df.to_csv('Deduped_Master.csv', index=False)
if __name__ == "__main__":
    main()

