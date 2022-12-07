# DSS-x-TWB-Devi-S

There are 2 .py files available - the Performance Dashboard and the Demographics Dashboard python files.

## The performance dashboard
- Provides visualizations of:
  - Distribution of raw scores obtained for different activities
  - Distribution of durations obtained for different activities
  - Success Rate per Activity
  - Mean Duration in Seconds per Activity
  - Mean Score by Activity
- Used datasets: mdl_h5pactivity_attempts.csv
- Used columns: 'duration in seconds', 'maxscore', 'success if all question are answered correctly then its 1 otherwise 0', 'userid', 'h5pactivityid', 'duration in seconds', 'scaled % = scaled * 100'

## The demographics dashboard 
- Provides visualizations of:
  - Student Gender Bar Charts
  - Learner Gender Bar Charts
  - Student Gender Distribution by Campus
  - Learner Gender Distribution by Campus
  - Learner Gender Distribution by Age
  - Learner Age Histogram
  - Student Class Histogram
  - Student Section Histogram
- Used datasets: mdl_h5pactivity_attempts.csv, mdl_student.csv, mdl_learner.csv, learnerRequestData.csv
- Used columns: 'duration in seconds', 'maxscore', 'campus_id', 'age', 'gender', 'Class', 'Section'

## HOW TO USE
Look at our instructions manual PDF in this same github master branch for steps on how to generate the dashboards on your own device (Mac & Windows). 

To use the files, change the paths to the data files as indicated at the top of the files. 
- In demographicsDashboard.py, you will need to change the file paths h5p_activity_path, student_data_path, learner_data_path, request_data_path to the file paths of the respective data sets. Below the file paths, you can specify which browser you would like to open the dashboard in, such as "safari" or "chrome." 
- In performanceDashboard.py, you will need to change the file paths h5p_activity_path to the file path of the h5p activity dataset. Below the file paths, you can specify which browser you would like to open the dashboard in, such as "safari" or "chrome." 

You might need to open the chrome independently if the server does not launch itself. The link http://127.0.0.1:8000 should appear in your terminal, which you can paste into any web browser.
