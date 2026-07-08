-- query 1
/*
This query was used to find the average performance of each student baesd upon their assigned 
sleep category, based upon the hours they have slept, ranging from low (5 hours or below),
medium(7 hours or below), or high(8+ hours) and also returned the number of each students in 
each category as well, as well as returning the average study hours of each category of sleep 
of students
*/

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

-- query 2
/* 
This query was used to find the stuednts that were above the average performance index score,
by using subqueries, and listed the first 20 students with the highest performance index scores
and found the relation that the top 20 highest scores had almost all studied for 9 hours
*/

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

-- query 4
/*
This query was used to find the average of each category of sleep using CTE, and found the 
average performance of each sleep category and the number of students in each category,
finding that those with the most sleep had the best average performance and more student count
*/
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