import pandas as pd
import numpy as np
import math

def sigmoid(x,b,c):
   """
   This is the logistic function. b and c are the parameters to be learned in order to calculate the variables scores.

   Parameters
   ----------
   x: float 
      Feature for which the score will be calculated.
   b: float 
      Midpoint sigmoind function value.
   c: float
      Logistic growth rate. Represents the steepness of the curve.

   Return
   ------
   Scores calculated from the sigmoid function.
   """
   return 1 / (1 + math.exp(-c * (x-b)))

def calc_score(x, column, model):
   """
   Function to calculte the features score using sigmoid and the features weights (importance)

   Parameters
   ----------
   x: float
      Feature for which the score will be calculated.
   column: str
      Feature name.
   model: Dataframe
      Dataframe containing the weights and parameters of the sigmoid function.

   Return
   ------
      Return the features scores passaed as column parameter.
   """
   return sigmoid(x, 
        model.loc[column]['x0'], 
        model.loc[column]['k']) * model.loc[column]['weight'].item()

def get_score(model, input, columns):
    """
    Function to apply the calc_score function.

    Parameters
    ----------
    model: Dataframe
      Dataframe containing the weights and parameters of the sigmoid function.
    input: Dataframe
      Features to calculate the score

    Return
    ------
    response: json
      Json containing the features score and the final score.
    """
    
    for col in input.columns[1:6]:
        input[col + 'Score'] = input[col].apply(calc_score, args=(col, model))
        input.loc[input[col]==0, col + 'Score'] = 0

    input['Score'] = round(input.iloc[:,6:].sum(axis=1),2)
    input.rename(columns={'Score':'LegalScore'}, inplace=True)
    # columns = [
    #     'person_uuid',
    #     'LegalScore'
    # ]

    input = input[columns]
    response = input.to_dict(orient='records')[0]
    return response
