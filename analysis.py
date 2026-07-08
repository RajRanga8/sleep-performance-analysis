# %%
import pandas as pd 
df = pd.read_csv('Student_Performance.csv')


#print(df.head())
# 5 rows and 6 columns shown 

#print(df.info())
# total of 10000 rows and 6 columns

#print(df.describe())
# range of sleep hours is 5, max of 9 and min of 4
# range of performance index is 90, max of 100 and min of 10

#print(df.shape)
#10000 by 6

#print(df.columns)
# different columns: hours studied, previs scores, extracurricular activities, sleep hours, sample question papers practiced, performance index

#null check
#print(df.isnull().sum())
#df = df.dropna()
# no nulls in the file 

#duplicate check
#print(df.duplicated().sum())
#df = df.drop_duplicates()
# didn't drop duplicates because some students cna have same asnwers resulting in same rows being created, allowing for duplicates in the dataset
# %%
df.columns = df.columns.str.lower().str.replace(' ', '_')
print(df.info)
#adjusts column names to be presentable and clean and have no spaces
# %%
df['sleep_category'] = df['sleep_hours'].apply(lambda x: 
    'Low (4-5 hours)' if x <= 5 else
    'Moderate (6-7 hours)' if x <= 7 else 
    'high (8-9 hours) ')
print (df['sleep_category'].value_counts())
#sleep_category
#high (8-9 hours)        3426
#Moderate (6-7 hours)    3349
#Low (4-5 hours)         3225
# %%
df.to_csv('Student_Performance_clean.csv', index = False)
print(f'Cleaned data: {df.shape[0]} rows, {df.shape[1]} columns')
#created clean data file
# %%
import matplotlib.pyplot as plt
import seaborn as sns 
# %%
sns.heatmap(df.corr(numeric_only = True), annot = True, cmap = 'coolwarm')
plt.title('Correlation of all variables')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')
plt.show()
# created the chart which shows the correlation of all variables, highest correlation between performance index and previous scores
# %%
plt.scatter(df['sleep_hours'], df['performance_index'], alpha=0.4, color = 'blue')
plt.xlabel('Sleep hours')
plt.ylabel('Performance Index')
plt.title('Sleep hours vs performance index')
plt.savefig('sleep_vs_performance.png')
plt.show()
# chart for sleep hours vs performance index, lower range of scores for those who slept 6 or 8 hours compared to others
# %%
df.groupby('sleep_category')['performance_index'].mean().plot(kind = 'bar', color='red')
plt.title('Average performance based on sleep category')
plt.ylabel('Average Performance')
plt.xlabel('Sleep Category')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('avg_performance_vs_category.png')
plt.show()
# chart for the average performance index vs the category of sleep, higher average performance for higher level of sleep of 8-9 hours
# %%
plt.scatter(df['hours_studied'], df['performance_index'], alpha=0.4, color = 'orange')
plt.xlabel('Hours Studied')
plt.ylabel('Performance Index')
plt.title('Hours studied vs Performance Index')
plt.savefig('Hours_studied_vs_Performance.png')
plt.show()
#chart for hours studied vs performance index, showing higher scores achieved for those who studied longer, and greater mins and maxs
# %%
print(df.groupby('sleep_category').agg(
    avg_performance=('performance_index', 'mean'),
    avg_study_hours=('hours_studied', 'mean'),
    count=('performance_index', 'count')
).round(2))
#
# %%
from scipy import stats

print('Sleep vs performance: ', df['sleep_hours'].corr(df['performance_index']).round(3))
#corr for sleep vs performance: 0.048
print('Hours studied vs performance: ', df['hours_studied'].corr(df['performance_index']).round(3))
#corr for hours studied vs performance: 0.374
print('Previous scores vs performance: ',df['previous_scores'].corr(df['performance_index']).round(3))
#corr for previous scores vs performance: 0.915
# %%
slope, intercept, r, p, se = stats.linregress(
    df['sleep_hours'], df['performance_index']
)
print(f'r = {r:.3f}') # r = 0.048
print(f'p-value = {p:.4f}') # p-value = 0
print(f'Significant: {p < 0.05}')# signifigance: true
# %%
avg_sleep = df['sleep_hours'].mean()
above = df[df['sleep_hours'] > avg_sleep]['performance_index'].mean()
below = df[df['sleep_hours'] <= avg_sleep]['performance_index'].mean()
print(f'Above avg sleep performance: {above:.2f}')
#above avg sleep performance: 56.00
print(f'Below avg sleep performance: {below:.2f}')
#below avg sleep performance: 54.42
print(f'Difference:  {above - below:.2f} points')
#dfference: 1.58
# students sleeping above average score 1.58 poitns higher on average
# %%
import sqlite3

conn = sqlite3.connect('student_performance_clean.db')
df.to_sql('students', conn, if_exists='replace', index=False)
print('Database created successfully')
# %%
#average performance by sleep category
query1 = '''
Select sleep_category, AVG(performance_index) as avg_performance, avg(hours_studied) as avg_studyhours, COUNT(*) as num_students
From students
group by sleep_category
order by avg_performance desc
'''
print(pd.read_sql_query(query1, conn))
#sleep category: high > avg_performance: 56.35 > num_students: 3426, avg_studyhours = 4.98
#sleep category: medium > avg_performance: 54.97 > num_students: 3349, avg_studyhours = 5.01
#sleep category: low > avg_performance: 54.30 > num_students: 3225, avg_studyhours = 4.99
# %%
#students above average performance 
query2 = '''
Select sleep_hours, performance_index, hours_studied
From students
Where performance_index > (
    Select avg(performance_index) from students
)
order by performance_index desc
LIMIT 20
'''
print(pd.read_sql_query(query2, conn))
#students with the highest above average performance, the top 20 highest scores, have almost all studied for 9 hours, while the amount of sleep is randomized
# %%
#average of each category by using CTE
query4 = '''
WITH sleep_summary as (
    Select sleep_category, AVG(performance_index) AS avg_performance, COUNT(*) AS total
    From students
    Group by sleep_category
)
Select * from sleep_summary
Order by avg_performance desc
'''
print(pd.read_sql_query(query4, conn))
#sleep category: high > avg_performance: 56.35 > num_students: 3426
#sleep category: medium > avg_performance: 54.97 > num_students: 3349
#sleep category: low > avg_performance: 54.30 > num_students: 3225
# %%
conn.close()
# %%
