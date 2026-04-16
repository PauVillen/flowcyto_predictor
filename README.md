# Flowcyto cell predictor
### flowcyto_predictor

Blood cell type predictor created for the Databases and Web development course, 2025-26, Bioinformatics for Health Sciences master (UPF)

* Creators:<b> Nahia Urra, Pau Villén, Diego Vicente and Itxaso Alonso. </b>

## DESCRIPTION
FlowCyto Predictor is a web application that predicts the most likely blood cell type based on a list of input genes.
The application compares the input gene list with a database of known cell type markers and calculates a prediction score for each cell type. Results are ranked according to their scores.
The application has been developed using Flask (Python) and MySQL.

## HOW TO RUN APP FROM YOUR OWN COMPUTER

1. Clone repository
2. Install requirements

```
pip install -r requirements.txt
```
3. Configure the database

Make sure you have a MySQL database running and import the provided SQL schema.
Then update the database connection string in the application configuration.
In the __init__ file user credentials must provided:

```
mysql+pymysql://username:password@localhost/flowcyto_db
```
4. Run app


## TUTORIAL AND DETAILS
The app has an easy and intuitive interface, user must provide query input in the search bar as indicated by the app itself.
Input must be provided in GENE SYMBOL format. Results from query will appear in the screen, featuring the predicted cell type, a short description, the prediction score and the probability of the prediction.
Scores are calculated using the support scores provided by original databases (source available for each marker). 

1. The user enters a list of genes in the search bar.

2. The input genes must be provided in GENE SYMBOL format.

3. The application compares these genes against a curated database of cell type markers. A score is calculated for each cell type based on the marker support weights.

4. Results are displayed showing:
  * predicted cell type
  * description
  * prediction score
  * prediction probability

## TECHNOLOGIES

- Python
- Flask
- MySQL
- SQLAlchemy
- HTML / CSS


## AUTHORS

This App was developed as an educational project for the Master's course, by Itxaso Alonso, Nahia Urra, Diego Vicente and Pau Villén. :)
