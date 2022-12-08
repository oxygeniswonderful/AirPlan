import pandas as pd
import numpy as np

class Preprocess:

    def __init__(self, df_airports_from, df_airports_to, df_routes):
        """
        :param df_airports_from: db of airports from countries we want to move
        :param df_airports_to: db of airports to countries we want to move
        :param df_routes: db of routes
        """
        self.df_airports_from = df_airports_from
        self.df_airports_to = df_airports_to
        self.df_routes = df_routes

    def preprocess(self):
        del self.df_airports_from['Source_from']
        del self.df_airports_from['Type_from']
        del self.df_airports_from['DB_timezone_from']
        del self.df_airports_from['DST_from']
        del self.df_airports_from['ICAO_from']

        del self.df_airports_to['Source_to']
        del self.df_airports_to['Type_to']
        del self.df_airports_to['DB_timezone_to']
        del self.df_airports_to['DST_to']
        del self.df_airports_to['ICAO_to']

        del self.df_routes['Codeshare']
        del self.df_routes['Stops']
        del self.df_routes['Equipment']

        df = pd.merge(self.df_routes, self.df_airports_from[['LAT_from', 'LON_from', 'Airport_from_ID', 'City_from', 'Country_from']],
                           how='inner', on='Airport_from_ID')
        df = pd.merge(df, self.df_airports_to[['LAT_to', 'LON_to', 'Airport_to_ID', 'City_to', 'Country_to']],
                           how='inner', on='Airport_to_ID')

        unique_airports = np.unique(self.df_airports_to[["Airport_to_ID"]])

        return df, unique_airports