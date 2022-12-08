from collections import namedtuple
from math import radians, cos, sin, asin, sqrt

import folium
import numpy as np
import pandas as pd
from folium import FeatureGroup, LayerControl
from folium.plugins import MarkerCluster

from Algoritms.Graph import Graph
from Algoritms.Node import Node
from Core.ConfigReader import ConfigReader
from Core.Preprocess import Preprocess


class BuildingGraph:
    def __init__(self, color, type_of_map, priority):
        """
        :param color: color of markers
        :param type_of_map: type of map
        :param priority: saving priority
        """
        self.config_reader = ConfigReader()
        airports_from = self.config_reader.read_config("date_base.airports_from")
        airports_to = self.config_reader.read_config("date_base.airports_to")
        routes = self.config_reader.read_config("date_base.routes")

        self.df_from = pd.read_csv(airports_from)
        self.df_to = pd.read_csv(airports_to)
        self.routes = pd.read_csv(routes)

        preprocess = Preprocess(self.df_from, self.df_to, self.routes)
        self.df, self.unique_airports = preprocess.preprocess()

        self.color = color.lower()
        self.type_of_map = type_of_map.lower()
        self.priority = priority

        if self.color == "":
            self.color = "blue"

        if self.type_of_map == "":
            self.type_of_map = "Stamen Terrain"

        # Создаем вершины графа
        self.nodes_int = [i for i in range(max(self.unique_airports) + 1)]
        self.nodes = [Node(str(self.nodes_int[i])) for i in range(len(self.nodes_int))]

        self.list_dist = self.list_distance()

        # Создаем граф со списками сежности
        self.g_money = Graph(self.nodes)

        self.g_time = Graph(self.nodes)

        for i in self.list_dist:
            self.g_time.connect(self.nodes[i[0]], self.nodes[i[1]], i[2])
            self.g_money.connect(self.nodes[i[0]], self.nodes[i[1]], i[3])

    def list_distance(self):

        # Расстояние через широты

        def haversine(lat1, lon1, lat2, lon2):
            # Вычисляет расстояние в километрах между двумя точками, учитывая окружность Земли.
            # https://en.wikipedia.org/wiki/Haversine_formula

            # convert decimal degrees to radians
            lon1, lat1, lon2, lat2 = map(radians, (lon1, lat1, lon2, lat2))

            # haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * asin(sqrt(a))
            km = 6367 * c
            return km

        list_dist = []

        for index, row in self.df.iterrows():
            dist = int(haversine(row['LAT_from'], row['LON_from'], row['LAT_to'], row['LON_to']))
            if dist != 0:
                cost = int(np.random.random() * dist)
            else:
                cost = 0
            list_dist.append((row['Airport_from_ID'], row['Airport_to_ID'], dist, cost))

        un_country_city = np.unique(self.df[['City_to']])

        for city in un_country_city:
            df_city = self.df_to[self.df_to['City_to'] == city]
            un_country = np.unique(df_city['Country_to'])
            for country in un_country:
                df_cc = df_city[df_city['Country_to'] == country]
                df_id = np.array(df_cc['Airport_to_ID'])
                for i in df_id:
                    for j in df_id:
                        if i < j:
                            list_dist.append([i, j, 0, 0])
                            list_dist.append([j, i, 0, 0])
        return list_dist

    #################################################
    ## dijkstra ##
    #################################################

    def dijkstra(self, city_from, city_to):
        ############################

        def get_bearing(p1, p2):

            '''
            Returns compass bearing from p1 to p2

            Parameters
            p1 : namedtuple with lat lon
            p2 : namedtuple with lat lon

            Return
            compass bearing of type float

            Notes
            Based on https://gist.github.com/jeromer/2005586
            '''

            long_diff = np.radians(p2.lon - p1.lon)

            lat1 = np.radians(p1.lat)
            lat2 = np.radians(p2.lat)

            x = np.sin(long_diff) * np.cos(lat2)
            y = (np.cos(lat1) * np.sin(lat2)
                 - (np.sin(lat1) * np.cos(lat2)
                    * np.cos(long_diff)))
            bearing = np.degrees(np.arctan2(x, y))

            # adjusting for compass bearing
            if bearing < 0:
                return bearing + 360
            return bearing

        def get_arrows(locations, color='blue', size=5, n_arrows=3):

            '''
            Get a list of correctly placed and rotated
            arrows/markers to be plotted

            Parameters
            locations : list of lists of lat lons that represent the
                        start and end of the line.
                        eg [[41.1132, -96.1993],[41.3810, -95.8021]]
            arrow_color : default is 'blue'
            size : default is 6
            n_arrows : number of arrows to create.  default is 3
            Return
            list of arrows/markers
            '''

            Point = namedtuple('Point', field_names=['lat', 'lon'])

            # creating point from our Point named tuple
            p1 = Point(locations[0][0], locations[0][1])
            p2 = Point(locations[1][0], locations[1][1])

            # getting the rotation needed for our marker.
            # Subtracting 90 to account for the marker's orientation
            # of due East(get_bearing returns North)
            rotation = get_bearing(p1, p2) - 90

            # get an evenly space list of lats and lons for our arrows
            # note that I'm discarding the first and last for aesthetics
            # as I'm using markers to denote the start and end
            arrow_lats = np.linspace(p1.lat, p2.lat, n_arrows + 2)[1:n_arrows + 1]
            arrow_lons = np.linspace(p1.lon, p2.lon, n_arrows + 2)[1:n_arrows + 1]

            arrows = []

            # creating each "arrow" and appending them to our arrows list
            for points in zip(arrow_lats, arrow_lons):
                arrows.append(folium.RegularPolygonMarker(location=points,
                                                     fill_color=color, number_of_sides=3,
                                                     radius=size + 2, rotation=rotation - 15))
            return arrows

        ##########################################################

        def amount_arrows(p1, p2):
            def haversine(lat1, lon1, lat2, lon2):
                # Вычисляет расстояние в километрах между двумя точками, учитывая окружность Земли.
                # https://en.wikipedia.org/wiki/Haversine_formula

                # convert decimal degrees to radians
                lon1, lat1, lon2, lat2 = map(radians, (lon1, lat1, lon2, lat2))

                # haversine formula
                dlon = lon2 - lon1
                dlat = lat2 - lat1
                a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
                c = 2 * asin(sqrt(a))
                km = 6367 * c
                return km

            n = int(haversine(p1[0], p1[1], p2[0], p2[1]) / 1000)
            if n == 0:
                n = int(haversine(p1[0], p1[1], p2[0], p2[1]) / 500)
                if n == 0:
                    n = 1
            return n

        def total_cost_dist(path_int):
            cost = 0
            dist = 0
            for i in range(len(path_int) - 1):
                ld = pd.DataFrame(self.list_dist)
                l = ld[ld[0] == path_int[i]]
                l = l[l[1] == path_int[i + 1]]
                cost += l[3].min()
                dist += l[2].min()
            return cost, dist

        priority = self.priority
        bd_f = self.df_from[self.df_from['Country_from'] == city_from[0]]
        int_from = bd_f[bd_f['City_from'] == city_from[1]]['Airport_from_ID'].iloc[0]
        bd_t = self.df_from[self.df_from['Country_from'] == city_to[0]]
        int_to = bd_t[bd_t['City_from'] == city_to[1]]['Airport_from_ID'].iloc[0]

        ans1 = self.g_time.path_from_to(self.nodes[int_from], str(int_to))  # nodes[]- исходная вершина, str - конечная
        ans2 = self.g_money.path_from_to(self.nodes[int_from], str(int_to))

        if priority == 'time':
            path = ans1[1]
        else:
            path_int1 = [int(p) for p in ans1[1]]
            path_int2 = [int(p) for p in ans2[1]]
            if total_cost_dist(path_int1)[0] < total_cost_dist(path_int2)[0]:
                path = ans1[1]
            else:
                path = ans2[1]
        path_int = [int(p) for p in path]

        if len(path) > 0:

            df_airports_path = self.df_from[self.df_from['Airport_from_ID'].isin(path_int)]

            # Собираем точки в нужном порядке
            data = []
            path_city_str = []
            path_country_str = []
            for i in range(len(path)):
                data.append(
                    [float(df_airports_path[df_airports_path['Airport_from_ID'] == int(path[i])]['LAT_from'].iloc[0]),
                     float(df_airports_path[df_airports_path['Airport_from_ID'] == int(path[i])]['LON_from'].iloc[0])]
                )
                path_city_str.append(
                    df_airports_path[df_airports_path['Airport_from_ID'] == int(path[i])]['City_from'].iloc[0])
                path_country_str.append(
                    df_airports_path[df_airports_path['Airport_from_ID'] == int(path[i])]['Country_from'].iloc[0])
                subset = pd.DataFrame(data)

            ####################################################
            ## вывод пути ##
            ####################################################

            for i in range(len(path_city_str)):
                print(path_city_str[i], ',', path_country_str[i], end=' -------> ')
                if i == len(path_city_str) - 1:
                    print(path_city_str[i], ',', path_country_str[i])

            cost = total_cost_dist(path_int)
            distance = cost[1]
            cost = cost[0]
            filename = self.config_reader.read_config("tmp.lines2")
            file = open(filename, "w")
            file.write(str(cost))

            filename = self.config_reader.read_config("tmp.lines3")
            file = open(filename, "w")
            file.write(str(distance))

            print(*path_int)
            ################################################
            ## MAP ##
            ################################################

            feature_group = FeatureGroup(name='All airports')
            feature_group2 = FeatureGroup(name='My path')

            m1 = folium.Map(location=[50.296933, -101.9574983], zoom_start=5, tiles=self.type_of_map)
            feature_group.add_to(m1)
            feature_group2.add_to(m1)
            LayerControl().add_to(m1)
            marker_cluster = MarkerCluster().add_to(feature_group)

            for at, on, city, country in zip(self.df_from["LAT_from"],
                                             self.df_from["LON_from"],
                                             self.df_from["City_from"],
                                             self.df_from["Country_from"]):
                folium.CircleMarker(location=[at, on], radius=9, popup=str(city) + ", " + str(country),

                               color="gray", fill_opacity=0.9).add_to(marker_cluster)

            for at, on, city in zip(df_airports_path['LAT_from'], df_airports_path['LON_from'],
                                    df_airports_path['City_from']):
                folium.Marker(location=[at, on],
                         popup=city,
                         icon=folium.Icon(self.color), draggable=False).add_to(feature_group2)

            for i in range(len(subset) - 1):
                p1 = [float(subset.iloc[i][0]), float(subset.iloc[i][1])]
                p2 = [float(subset.iloc[i + 1][0]), float(subset.iloc[i + 1][1])]
                arrows = get_arrows(locations=[p1, p2], n_arrows=amount_arrows(p1, p2))
                for arrow in arrows:
                    arrow.add_to(feature_group2)

        m1.save(self.config_reader.read_config("tmp.FeatureGroup"))
        if len(path) == 0:
            print('Вы не сможете добраться до этого города')
        return m1

    ######################################################################
    ##tsp##
    ########################################################################

    def tsp(self, countries):

        def haversine(lat1, lon1, lat2, lon2):
            # Вычисляет расстояние в километрах между двумя точками, учитывая окружность Земли.
            # https://en.wikipedia.org/wiki/Haversine_formula

            # convert decimal degrees to radians
            lon1, lat1, lon2, lat2 = map(radians, (lon1, lat1, lon2, lat2))

            # haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * asin(sqrt(a))
            km1 = 6367 * c
            return km1

        def find_cycle(matrix, n):
            # Функция нахождения минимального элемента, исключая текущий элемент
            def Min(lst, myindex):
                return min(x for idx, x in enumerate(lst) if idx != myindex)

            # функция удаления нужной строки и столбцах
            def Delete(matrix, index1, index2):
                del matrix[index1]
                for i in matrix:
                    del i[index2]
                return matrix

            H = 0
            Str = []
            Stb = []
            res = []
            result = []
            StartMatrix = []

            for i in range(n):
                Str.append(i)
                Stb.append(i)

            # Сохраняем изначальную матрицу
            for i in range(n): StartMatrix.append(matrix[i].copy())

            # Присваеваем главной диагонали float(inf)
            for i in range(n): matrix[i][i] = float('inf')

            while True:
                # Редуцируем
                # --------------------------------------
                # Вычитаем минимальный элемент в строках
                for i in range(len(matrix)):
                    temp = min(matrix[i])
                    H += temp
                    for j in range(len(matrix)):
                        matrix[i][j] -= temp

                # Вычитаем минимальный элемент в столбцах
                for i in range(len(matrix)):
                    temp = min(row[i] for row in matrix)
                    H += temp
                    for j in range(len(matrix)):
                        matrix[j][i] -= temp
                # --------------------------------------

                # Оцениваем нулевые клетки и ищем нулевую клетку с максимальной оценкой
                # --------------------------------------
                NullMax = 0
                index1 = 0
                index2 = 0
                tmp = 0
                for i in range(len(matrix)):
                    for j in range(len(matrix)):
                        if matrix[i][j] == 0:
                            tmp = Min(matrix[i], j) + Min((row[j] for row in matrix), i)
                            if tmp >= NullMax:
                                NullMax = tmp
                                index1 = i
                                index2 = j
                # --------------------------------------

                # Находим нужный нам путь, записываем его в res и удаляем все ненужное
                res.append(Str[index1])
                res.append(Stb[index2])

                oldIndex1 = Str[index1]
                oldIndex2 = Stb[index2]
                if oldIndex2 in Str and oldIndex1 in Stb:
                    NewIndex1 = Str.index(oldIndex2)
                    NewIndex2 = Stb.index(oldIndex1)
                    matrix[NewIndex1][NewIndex2] = float('inf')
                del Str[index1]
                del Stb[index2]
                matrix = Delete(matrix, index1, index2)
                if len(matrix) == 1:
                    break

            # Формируем порядок пути
            for i in range(0, len(res) - 1, 2):
                if res.count(res[i]) < 2:
                    result.append(res[i])
                    result.append(res[i + 1])
            for i in range(0, len(res) - 1, 2):
                for j in range(0, len(res) - 1, 2):
                    if result[len(result) - 1] == res[j]:
                        result.append(res[j + 1])
            result.append(result[0])

            result = np.array(result)

            return result

        ##################################
        # Осталось вывести их на карту()
        def print_cycle(path_id):
            lons = []
            lats = []
            city = []
            for i in range(len(path_id)):
                df_airports_path = self.df_from[self.df_from['Airport_from_ID'] == path_id[i]]
                df_airports_path = df_airports_path[df_airports_path['Country_from'] == country_path[i]]
                lons.append(df_airports_path['LON_from'].iloc[0])
                lats.append(df_airports_path['LAT_from'].iloc[0])
                city.append(df_airports_path['City_from'].iloc[0])

            feature_group2 = FeatureGroup(name='My path')

            m1 = folium.Map(location=[lons[1], lats[1]], zoom_start=3, tiles=self.type_of_map)

            feature_group2.add_to(m1)
            LayerControl().add_to(m1)

            for at, on, c, country in zip(lats, lons, city, country_path):
                folium.Marker(location=[at, on],
                         popup=c + ", " + country,
                         icon=folium.Icon(self.color)).add_to(feature_group2)

            subset = []
            for i in range(len(lats)):
                subset.append((lats[i], lons[i]))
            for at, on in zip(lats, lons):
                folium.PolyLine(locations=subset, opacity=0.1,
                           color='cadetblue',
                           dash_array='10').add_to(m1)
            return m1

        ############################################

        city_int = []
        n = len(countries)

        for i in range(n):

            db = self.df_from[self.df_from['City_from'] == countries[i][1]]
            db = db[db['Country_from'] == countries[i][0]]
            city_int.append(db['Airport_from_ID'].iloc[0])
        matrix_id = []
        for i in range(n):
            db = self.df_from[self.df_from['City_from'] == countries[i][1]]
            db = db[db['Country_from'] == countries[i][0]]
            id_ports = np.array(db['Airport_from_ID'])
            matrix_id.append(id_ports)

        id_airports = []
        for i in range(0, n):
            db = self.df[self.df['Airport_from_ID'].isin(matrix_id[i])]
            for j in range(n):
                if i == j:
                    continue
                db1 = db[db['Airport_to_ID'].isin(matrix_id[j])]
            if (db1.empty):
                pass

            id_airports.append(db1['Airport_from_ID'].iloc[0])

        matrix_dist = []

        for i in range(n):
            row = []
            for j in range(n):
                if i == j:
                    d = 0
                if i != j:
                    db = self.df[self.df['Airport_from_ID'].isin(matrix_id[i])]
                    db1 = db[db['Airport_to_ID'].isin(matrix_id[j])]
                    if db1.empty:
                        d = 100000000000000 #float("inf")
                    else:
                        d = int(haversine(db1['LAT_from'].iloc[0], db1['LON_from'].iloc[0],
                                          db1['LAT_to'].iloc[0], db1['LON_to'].iloc[0]))

                row.append(d)
            matrix_dist.append(row)

        path = find_cycle(matrix_dist, n)
        country_path = []
        path_id = []
        for i in path:
            path_id.append(city_int[i])
            country_path.append(countries[i][0])
        m1 = print_cycle(path_id)
        m1.save(self.config_reader.read_config("tmp.FeatureGroup"))
        return m1