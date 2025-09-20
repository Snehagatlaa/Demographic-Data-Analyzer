import pandas as pd

def calculate_demographic_data(print_data=True):
    # Define column names since adult.data.csv has no headers
    column_names = [
        'age', 'workclass', 'fnlwgt', 'education', 'education-num',
        'marital-status', 'occupation', 'relationship', 'race', 'sex',
        'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'salary'
    ]

    # Read dataset with column names
    df = pd.read_csv("adult.data.csv", header=None, names=column_names)

    # Strip whitespace from string columns (important for comparisons like '>50K')
    for col in df.select_dtypes(include='object'):
        df[col] = df[col].str.strip()


    # 1. How many people of each race are represented in this dataset?
    race_count = df['race'].value_counts()

    # 2. What is the average age of men?
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # 3. Percentage of people who have a Bachelor's degree
    percentage_bachelors = round((df['education'].value_counts(normalize=True)['Bachelors'] * 100), 1)

    # 4. Percentage with advanced education making >50K
    advanced_education = ['Bachelors', 'Masters', 'Doctorate']
    higher_education = df[df['education'].isin(advanced_education)]
    lower_education = df[~df['education'].isin(advanced_education)]

    higher_education_rich = round((higher_education[higher_education['salary'] == '>50K'].shape[0] /
                                   higher_education.shape[0]) * 100, 1)
    lower_education_rich = round((lower_education[lower_education['salary'] == '>50K'].shape[0] /
                                  lower_education.shape[0]) * 100, 1)

    # 5. Minimum number of hours a person works per week
    min_work_hours = df['hours-per-week'].min()

    # 6. Percentage of people who work min hours and earn >50K
    min_workers = df[df['hours-per-week'] == min_work_hours]
    rich_percentage = round((min_workers[min_workers['salary'] == '>50K'].shape[0] /
                             min_workers.shape[0]) * 100, 1)

    # 7. Country with highest percentage of >50K earners
    country_earnings = df[df['salary'] == '>50K']['native-country'].value_counts()
    country_total = df['native-country'].value_counts()
    country_percentages = (country_earnings / country_total * 100).dropna()
    highest_earning_country = country_percentages.idxmax()
    highest_earning_country_percentage = round(country_percentages.max(), 1)

    # 8. Most popular occupation for >50K in India
    india_occupation = df[(df['native-country'] == 'India') & (df['salary'] == '>50K')]
    top_IN_occupation = india_occupation['occupation'].value_counts().idxmax()

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print("Highest percentage of rich people in country:", highest_earning_country_percentage)
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
