# Python CSV file processing
Project was last updated on: 16 Sept 2022

**This was a university project for a basic python unit.**

I did not upload the csv files used to test this project. The code I used in this project received a grade of over 80%.

## Project Overview

Face recognition (FR) is one the most widely known and used non-intrusive biometric that aids in identifying individuals and its primary objective is to recognize a specific person in various scenarios, such as when displaying different facial expressions, after their identity has been established.

The project required analyzing eight geodesic (surface) and eight 3D Euclidian distances between facial landmarks for four expressions: 'Neutral,' 'Angry,' 'Disgust,' and 'Happy.' These distances are measured on a face in the 'Neutral' expression and can be used to determine similarity with the same face in different expressions or with other faces in the dataset. Details of facial landmarks could be Ex-Outer eye corners or En- Inner eye corners, while distances could be Inner-canthal width En_L En_R or Outer-canthal width Ex_L Ex_R.

**The function takes three input arguments:**

> csvfile, the name of a CSV file containing data on individuals to be analyzed. The file contains an unspecified number of rows, with each row providing information on an individual's de-identified adult ID, displayed expression, distance number, geodesic distance, and 3D Euclidean distance. The first row of the file contains headers for these fields. The values in each row are strings for adult ID and expression, an integer for distance, and floats for the remaining values.

> adultID, the ID number of the adult to be analyzed. The ID is a case-sensitive string.

> Option, a string input that determines the type of analysis to be performed.
