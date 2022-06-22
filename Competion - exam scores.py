# Importing the pandas module
import pandas as pd

# Reading in the data
df = pd.read_csv('data/exams.csv')

# Take a look at the first data-points
df.head()

# 1. What are the average reading scores for students with/without the test preparation course?

df.groupby('test_prep_course')[['reading']].mean()

# Check if test prep course was taken by enough students for results to be relevant
# test=df['test_prep_course']
# sns.countplot(x=test)
# plt.show()

# 3. Create plots to visualize findings for questions 1 and 2.

print("The average reading scores show that students who took the test preparation course did better "
      "at the year-end exam.")

import matplotlib.pyplot as plt
import seaborn as sns

sns.catplot(x='test_prep_course', y='reading', data=df, kind='bar')
plt.show()

# 2. What are the average scores for the different parental education levels?

# Unpivot df
df_tall = df.melt(id_vars=['parent_education_level', 'test_prep_course'], value_vars=['reading', 'math', 'writing'],
                  var_name=['subject'], value_name='score')
# print(df_tall.head(10))

print('AVERAGE SUBJECT SCORES BY PARENTAL EDUCATIONAL LEVEL')
df_by_ed_subj = df_tall.groupby(['parent_education_level', 'subject'])[['score']].mean()
print(df_by_ed_subj)

print('AVERAGE SCORES BY PARENTAL EDUCATIONAL LEVEL')
df_by_ed = df_tall.groupby(['parent_education_level'])[['score']].mean()

print(df_by_ed.sort_values('score', ascending=False))
print("The level of parental education influences the results, though for higher scores the distribution is wider.")
print("Average results in reading and writing are more prominent with students whose parents have MASTER'S DEGREE.")
order_ed = ["high school", "some high school", "some college", "associate's degree",
            "bachelor's degree", "master's degree"]
sns.catplot(x='parent_education_level', y='score', data=df_tall, kind='bar', hue='subject',
            hue_order=['math', 'writing', 'reading'], order=order_ed)
plt.xticks(rotation=90)
plt.show()

# 4. [Optional] Look at the effects within subgroups. Compare the average scores for students with/without
# the test preparation course for different parental education levels (e.g., faceted plots).

# print('reading')

df1 = df.pivot_table(values='reading', index='parent_education_level', columns='test_prep_course')
df1['diff'] = df1['completed'] - df1['none']

# print(df1.sort_values('diff',ascending=False))
# print('math')

df2 = df.pivot_table(values='math', index='parent_education_level', columns='test_prep_course')
df2['diff'] = df2['completed'] - df2['none']

# print(df2.sort_values('diff',ascending=False))
# print('all')

df3 = df.pivot_table(values='writing', index='parent_education_level', columns='test_prep_course')
df3['diff_writing'] = df3['completed'] - df3['none']
df3['diff_math'] = df2['diff']
df3['diff_reading'] = df1['diff']

# df3['diff_total']=df3[['diff_writing'],['diff_math'],['diff_reading']].sum()

df4 = df3.loc[:, 'diff_writing':'diff_reading']
df4['diff_total'] = df4.mean(axis='columns')

# df4.mean(axis='columns')

print(df4.sort_values('diff_total', ascending=False))

print("Students whose parents have SOME COLLEGE educational level tend to suffer most from not taking the test")
print("preparation course.")
order_ed = ["high school", "some high school", "some college", "associate's degree", "bachelor's degree",
            "master's degree"]
sns.catplot(x='score', y='parent_education_level', data=df_tall, kind='bar', hue='test_prep_course',
            order=order_ed)
plt.show()

# 5. [Optional 2] The principal wants to know if kids who perform well on one subject also
# score well on the others. Look at the correlations between scores.

print('Students who perform well on one subject also score well on the others.')
print('The correlation is more prominent in writing/reading subject pair.')
fig, ax = plt.subplots(1, 2, sharey=True)
ax[0].scatter(df['reading'], df['writing'], alpha=0.5, color='#eb8934')
ax[1].scatter(df['math'], df['writing'], alpha=0.5, color='#3458eb')
ax[0].set_xlabel('reading')
ax[1].set_xlabel('math')
ax[0].set_ylabel('writing')
plt.show()

# fig, (ax0, ax1)=plt.subplots(nrows=1, ncols=2, sharey=True)
# sns.regplot(x='reading', y='writing', data=df, ax=ax0)
# sns.regplot(x='math', y='writing', data=df, ax=ax1)
# ax0.set_xlabel('reading')
# ax1.set_xlabel('math')
# ax0.set_ylabel('writing')
# plt.show()

fig, ax = plt.subplots()
ax.scatter(df['reading'], df['math'], alpha=0.5, color='g')
ax.set_xlabel('reading')
ax.set_ylabel('math')
fig.set_size_inches([2.7, 4])
plt.show()

# Conclusions
#
# 1.Test preparation course is helpful to all students, especially those whose parents have SOME COLLEGE
# educational level.
#
# The questions to think about:
#
# Does the course give extra knowledge or student practice the exam procedure to reduce stress level
# during actual exams?
#
# 2.Parental educational level affects the results though most likely indirectly. High parental educational
# level alone cannot guarantee better year-end performance. Though information about educational background
# can be useful to the teachers to know which students are more likely to need more guidance and be extra
# motivated to take the test preparation course.
#
# 3.Students who do well on one subject tend to do well on other subjects as well. Reading and writing
# scores predictably show higher correlation.
