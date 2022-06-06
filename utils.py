from geopy.distance import great_circle
import pandas as pd
import folium

class CountByWGS84:

    def __init__(self, df, lat, lon, dist=1):

        self.df = df
        self.lat = lat
        self.lon = lon
        self.dist = dist
        
    def filter(self):

        lat_min = self.lat - 0.01 * self.dist
        lat_max = self.lat + 0.01 * self.dist

        lon_min = self.lon - 0.015 * self.dist
        lon_max = self.lon + 0.015 * self.dist

        self.points = [[lat_min, lon_min], [lat_max, lon_max]]

        result = self.df.loc[
            (self.df['위도'] > lat_min) &
            (self.df['위도'] < lat_max) &
            (self.df['경도'] > lon_min) &
            (self.df['경도'] < lon_max)
        ]
        result.index = range(len(result))

        return result
    
    def filter_by_radius(self):
        tmp = self.filter()

        # 기준 좌표 포인트
        center = (self.lat, self.lon)

        result = pd.DataFrame()
        for index, row in tmp.iterrows():
            # 개별 좌표 포인트
            point = (row['위도'], row['경도'])
            d = great_circle(center, point).kilometers
            if d <= self.dist:
                result = pd.concat([result, tmp.iloc[index, :].to_frame().T])

        result.index = range(len(result))

        return result

    def plot_by_radius(self, df):


        m = folium.Map(location=[self.lat, self.lon], zoom_start=14)

        for idx, row in df.iterrows():

            lat_ = row['위도']
            lon_ = row['경도']

            folium.Marker(location=[lat_, lon_],
                          radius=15,
                          tooltip=row['상호명']).add_to(m)

        folium.Circle(radius=self.dist * 1000,
                      location=[self.lat, self.lon],
                      color="#ff7800",
                      fill_color='#ffff00',
                      fill_opacity=0.2
                      ).add_to(m)

        return m