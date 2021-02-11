# Zoom-Poll-Evaluator

Zoom Poll Evaluator evaluates poll answers answered by participants and computes attendance ratios for Zoom sessions. 
The project is built within Object Oriented Software Design course in Computer Engineering Department. Also project is checked by Murat Can Ganiz in each iteartion.

## Description
This project's main idea is to evaluate poll answers asnwered by participants of participated zoom session and compute attendance ratios for multiple zoom sessions.
Poll questions considered as pop up quizzes so there are true answers for each question.

After all necessary documents are processed, a general document created for polls and their statistical information. Also for each poll statistical information are 
created on different files and given answer distrubtion is created as histograms. For each participant their accuracy percentages are created with their zoom username and related
poll's name.

### Iteration 1
We created an operable program that takes participant list that contains their necessary information. After, based on answer key files, the polls, questions and true answers 
are created. After that program takes all submission for all participants and creates student-poll relations one by one. At the end of creation relationships 
program computes attendances by looking a json file that is used for storage purposes for different runs. 

Finally program evaluates each submission's correctness for each poll and student. Given answers distribution of participants are created as histograms and a general file 
created for poll's and their statistical state.

### Iteration 2
We changed lots of simple things because of the change in input formats and their contents. A more deatiled output is created for each student and each poll. 
Question' description are added to histograms and corrected attendance logic from hourly to session based.

## Collabrators
- Talha Bayburtlu
- Can Karatepe
- Melik Çağan Oduncuoğlu
- Osman Erikci
- Abdullah Emre Aydemir
- Zekeriya Batuhan Karataş
