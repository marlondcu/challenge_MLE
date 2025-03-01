import pandas as pd
import numpy as np
from datetime import datetime
from typing import Tuple, Union, List
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix, classification_report
import xgboost as xgb


class DelayModel:
    def __init__(self):
        self._model = None  # Model will be saved in this attribute

    def get_min_diff(self, data: pd.Series) -> float:
        """
        Calculate the time difference in minutes between 'Fecha-O' and 'Fecha-I'.
        
        Args:
            data (pd.Series): A row of the DataFrame containing 'Fecha-O' and 'Fecha-I'.

        Returns:
            float: The difference in minutes.
        """
        fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
        fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
        min_diff = ((fecha_o - fecha_i).total_seconds()) / 60  # Convert to minutes
        return min_diff

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or prediction.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        #Define get_min_diff to set a delay'
        data['min_diff'] = data.apply(self.get_min_diff, axis=1)

        #Create delay column based on min_diff threshold (15 minutes)
        threshold_in_minutes = 15
        data['delay'] = np.where(data['min_diff'] > threshold_in_minutes, 1, 0)

        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix='OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix='TIPOVUELO'),
            pd.get_dummies(data['MES'], prefix='MES')
        ], axis=1)

        
        top_10_features = [
           "OPERA_Latin American Wings", 
           "MES_7",
           "MES_10",
           "OPERA_Grupo LATAM",
           "MES_12",
           "TIPOVUELO_I",
           "MES_4",
           "MES_11",
           "OPERA_Sky Airline",
           "OPERA_Copa Air" ]

        features = features[top_10_features]

        if target_column:
           target = data[target_column]
           return features, target

        return features

    def fit(self, features: pd.DataFrame, target: pd.DataFrame) -> None:
        """
        Fit the model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        scale_pos_weight = target.value_counts()[0] / target.value_counts()[1]
        
        self._model = xgb.XGBClassifier(
            random_state=1,
            learning_rate=0.01,
            scale_pos_weight=scale_pos_weight  # balance
        )
        self._model.fit(features, target)

    def predict(self, features: pd.DataFrame) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.

        Returns:
            (List[int]): predicted targets.
        """

        predictions = self._model.predict(features)
        predictions = [1 if y_pred > 0.5 else 0 for y_pred in predictions]
        return predictions

   