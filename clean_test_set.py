import pandas as pd


def remove_training_from_test_duplicates(train_file_name, test_file_name):
    df_train_set = pd.read_csv(train_file_name, error_bad_lines= False)
    df_test_set = pd.read_csv(test_file_name, error_bad_lines=False)
    df_test_set = df_test_set[~df_test_set['id'].isin(df_train_set['id'])]
    df_test_set.to_csv('Final_Testing_Set.csv', index=False)


def main():

    remove_training_from_test_duplicates('Final_Training_Set.csv', 'Testing_Set.csv')


if __name__ == "__main__":
    main()
