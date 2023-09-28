import subprocess
import pandas as pd
import warnings 
warnings.filterwarnings('ignore')
command = 'pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org gdown --ignore-installed'
output = subprocess.check_output(command, shell=True)
output_str = output.decode('utf-8')
print(output_str)

output_file = 'data/datasetproject.zip'
# Define the folder ID and destination directory
file_id = '1AHV_Thi1xFp792l8dOHFCWvHpISx8bn9'

command = "gdown --id {} -O {}".format(file_id, output_file)
output = subprocess.check_output(command, shell=True)
output_str = output.decode('utf-8')
print(output_str)

command = 'unzip data/datasetproject.zip -d data/'
output = subprocess.check_output(command, shell=True)
output_str = output.decode('utf-8')
print(output_str)


comments_df = pd.read_csv('data/Comments.csv', delimiter = ',', encoding = 'utf-8', nrows=10000)
course_df = pd.read_csv('data/Course_info.csv', delimiter = ',', encoding = 'utf-8', nrows=10000)
N = 10
# Select first N columns
course_df  = course_df.iloc[: , :N]
comments_df = comments_df.iloc[: , :3]
course_df['id'] = course_df['id'].astype(int)
# Create a set of valid course IDs from course_df
course_ids = course_df['id']

# Filter comments that have a valid course ID
comments_df = comments_df[comments_df['course_id'].isin(course_ids)]

# Save comments_df with tab delimiter
comments_df.to_csv('data/comments_df.csv', index=False, sep='\t', encoding='utf-8')

# Save course_df with tab delimiter
course_df = course_df.drop('headline', axis=1)
course_df.to_csv('data/course_df.csv', index=False, sep='\t', encoding='utf-8')
print("Stage 1 Done")

