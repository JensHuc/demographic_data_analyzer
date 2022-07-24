import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # Number of entries
    num_of_entries = len(df)
  
    # How many of each race are represented in the dataset
    race_count = df.groupby('race')['race'].count().sort_values(ascending=False)

    # What is the average age of men?
    avg_age = df.groupby('sex')['age'].mean()
    average_age_men = avg_age.loc['Male'].round(1)

    # What is the percentage of people who have a Bachelor's degree?
    education = df.groupby('education')['education'].count()
    bachelors = education.loc['Bachelors']
    percentage_bachelors = ((bachelors / num_of_entries)*100).round(1)

    # Percentage of people make > 50k
    ### More than 50 k
    salary_50plus = df.loc[df['salary'] == ">50K"]
  
    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_edu = education.loc['Bachelors'] + education.loc['Masters'] + education.loc['Doctorate']

    edu_50plus = salary_50plus.groupby('education')['education'].count()

    higher_edu_50plus = edu_50plus.loc['Bachelors'] + edu_50plus.loc['Masters'] + edu_50plus.loc['Doctorate']

    higher_education_rich = ((higher_edu_50plus / higher_edu)*100).round(1)
   
    ### without higher Education more than 50k
    lower_edu = num_of_entries - higher_edu
    lower_edu_50plus = edu_50plus.sum() - higher_edu_50plus
    lower_education_rich = ((lower_edu_50plus / lower_edu)*100).round(1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_hours_per_week = df['hours-per-week'].min()
    min_work_hours = min_hours_per_week

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    hours_per_week = df.groupby('hours-per-week')['hours-per-week'].count()
    num_min_workers = hours_per_week.loc[min_hours_per_week]

    minhours_50plus = salary_50plus.loc[df['hours-per-week'] == min_hours_per_week]
    minhours_50plus_pcnt = (len(minhours_50plus) / num_min_workers)*100
    rich_percentage = minhours_50plus_pcnt

    # What country has the highest percentage of people that earn >50K?
    countries_50plus = salary_50plus.groupby('native-country')['native-country'].count()
    people_count_country = df.groupby('native-country')['native-country'].count()

    countries_50plus_df = countries_50plus.to_frame(name='count-50plus')
    countries_df = countries_50plus.index.to_frame(name='Countries')
    people_count_country_df = people_count_country.to_frame(name='total_people')
    countries_salary = pd.concat([countries_df, countries_50plus_df, people_count_country_df], axis=1)
    countries_salary['pcnt_50plus'] = (countries_salary['count-50plus'] / countries_salary['total_people'])*100

    countries_max_salary = countries_salary['pcnt_50plus'].max()
    country_max_salary = countries_salary.loc[countries_salary['pcnt_50plus'] == countries_max_salary]
    country_max_salary_str = country_max_salary.index.tolist()
    country_max_salary_str = country_max_salary_str[0]
  
    highest_earning_country = country_max_salary_str
    highest_earning_country_percentage = round(countries_max_salary, 1)

    # Identify the most popular occupation for those who earn >50K in India.
    india_50plus = salary_50plus.loc[salary_50plus['native-country'] == "India"]
    india_50plus_occ = india_50plus.groupby('occupation')['occupation'].count()
    india_50plus_occ_max = india_50plus_occ.max()

    india_50plus_occ_popular = india_50plus_occ.loc[india_50plus_occ == india_50plus_occ_max]
    india_50plus_occ_popular_str = india_50plus_occ_popular.index.tolist()
    india_50plus_occ_popular_str = india_50plus_occ_popular_str[0]
    top_IN_occupation = india_50plus_occ_popular_str

    # Result

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
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
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
