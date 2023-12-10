from requests import post
import pandas as pd
import requests

CLIENT_ID = '5shneu6u6k9eh5a5eqaz3uokteh2cq'
CLIENT_SECRET = open("scripts/data_acquisition/secret.txt").read()
GRANT_TYPE = 'client_credentials'
ENDPOINT_TOKEN= f'https://id.twitch.tv/oauth2/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type={GRANT_TYPE}'
PATH_IMAGENES = r"data"


# Obtención del token de autenticación de Twitch Developers API

#https://api-docs.igdb.com/?python#authentication

class GamesCoverAdquisition():
    def __init__(self, write_csv = True) -> None:
        self.auth_data = self.initilize_connection()
        self.platforms_df = self.get_id_platform()
        self.genre_df = self.get_genre_games()
        self.games_df = self.get_games_data()
        self.games_df = self.get_games_cover_id(self.games_df)
        if write_csv:
            self.write_data(self.games_df, "games")
            self.write_data(self.genre_df, "genres")
    
    def initilize_connection(self) -> dict:
        """ Inicializa la conexión con la API de IGDB

        Returns:
            dict: Diccionario con el token de autenticación
        """
        response = post(ENDPOINT_TOKEN)
        bearer_token = response.json()["access_token"]
        auth_data ={'Client-ID': CLIENT_ID,
                    'Authorization': f'Bearer {bearer_token}'}
        return auth_data
    
    @staticmethod    
    def get_API_data_igdb(tipo: str, api_string: str, headers_auth:dict)-> requests.models.Response:
        """ Obtiene los datos de la API de IGDB

        Args:
            tipo (str): Tipo de datos que se quieren obtener (genres, platforms, games)
            api_string (str): String con la query de la API
            headers_auth (dict): Diccionario con el token de autenticación

        Returns:
            requests.models.Response: Respuesta de la API
        """
        url = f'https://api.igdb.com/v4/{tipo}'
        data = api_string
        response = post(url, data=data, headers=headers_auth)
        return response

    def get_id_platform(self) -> pd.DataFrame:
        """ Obtiene los id de las plataformas de la API de IGDB

        Returns:
            pd.DataFrame: _description_
        """
        platforms_filter = ["Xbox Series X|S", "PlayStation 5", "Nintendo Switch"]
        platforms_list = ["XBOX", "PLAYSTATION", "SWITCH"]
        platforms_df = pd.DataFrame()
        for platform in platforms_list:
            query_string = f'fields abbreviation,name,generation;limit 100;search "{platform}";'
            response = self.get_API_data_igdb("platforms", query_string, self.auth_data)
            platforms_df = pd.concat([platforms_df, pd.DataFrame(response.json())])
        return platforms_df.loc[platforms_df["name"].isin(platforms_filter)]

    def get_genre_games(self) -> pd.DataFrame:
        """ Obtiene los géneros de los juegos de la API de IGDB

        Returns:
            pd.DataFrame: DataFrame con los géneros de los juegos
        """
        query_string = 'fields name,slug;limit 500;'
        response = self.get_API_data_igdb("genres", query_string, self.auth_data)
        return pd.DataFrame(response.json())

    def get_games_data(self) -> pd.DataFrame:
        """ Obtiene los datos de los juegos de la API de IGDB

        Returns:
            pd.DataFrame: DataFrame con los datos de los juegos
        """
        platforms_list_id = list(self.platforms_df["id"])
        print(platforms_list_id)
        videogame_data = []
        for platform in platforms_list_id:
            print("Procesando plataforma: " + str(platform))
            id_list = (0,1)
            iterador = 0
            last_value = 0
            all_data_finished = False

            videogame_data_by_platform = []

            while not all_data_finished:

                try:
                    print("Iteracion: " + str(iterador))
                    print(len(id_list))
                    query_string = f'''fields name,cover,genres.slug;where platforms = ({platform}) & category = 0 & id != {id_list};limit 500;'''
                    response = self.get_API_data_igdb("games", query_string, self.auth_data)
                    videogame_data_by_platform = videogame_data_by_platform + response.json()
                    id_list = tuple(item['id'] for item in videogame_data_by_platform)

                    if len(id_list) == last_value:
                        all_data_finished = True
                    
                    if (len(id_list) >= 5000):
                        all_data_finished = True

                    last_value = len(id_list)
                    iterador +=1
                except:
                    all_data_finished = True
            videogame_data = videogame_data + videogame_data_by_platform
        videogame_df = pd.DataFrame(videogame_data)
        videogame_df = videogame_df.dropna().drop_duplicates(subset = "id")
        return videogame_df

    def get_games_cover_id(self, games_df: pd.DataFrame) -> pd.DataFrame:
        """ Obtiene los id de las portadas de los juegos de la API de IGDB

        Args:
            games_df (pd.DataFrame): DataFrame con los datos de los juegos

        Returns:
            pd.DataFrame: DataFrame con los id de las portadas de los juegos
        """
        id_batches = np.array_split(games_df["cover"].astype(int).to_list(), 
                        games_df.shape[0]//500+1)
        image_data = []
        for batch in id_batches:
            batch = tuple(batch)
            query_string = f'''fields image_id;where id = {batch};limit 500;'''
            response = self.get_API_data_igdb("covers", query_string, self.auth_data)
            image_data = image_data + response.json()

        image_data = pd.DataFrame(image_data)
        image_data.rename(columns = {"id":"cover"}, inplace = True)
        image_data.head()
        final_data = pd.merge(games_df, image_data, 
                        on='cover', how='left')
        return final_data

    def download_images(self, games_df: pd.DataFrame) -> None:
        """ Descarga las imágenes de las portadas de los juegos

        Args:
            games_df (pd.DataFrame): DataFrame con los datos de los juegos
        """
        os.makedirs(PATH_IMAGENES, exist_ok=True)
        for index, row in tqdm(games_df.iterrows(), total=games_df.shape[0]):
            if row["image_id"] != None:
                url = f'https://images.igdb.com/igdb/image/upload/t_cover_big/{row["image_id"]}.jpg'
                filename = f'{PATH_IMAGENES}/{row["id"]}.jpg'
                wget.download(url, filename)

    def write_data(self, games_df: pd.DataFrame, name: str) -> None:
        """ Escribe los datos de los juegos en un archivo csv

        Args:
            games_df (pd.DataFrame): DataFrame con los datos de los juegos
            name (str): Nombre del archivo csv
        """
        games_df.to_csv(f"data/{name}.csv", index=False)

if __name__ == "__main__":
    cover_adq = GamesCoverAdquisition(write_csv = True)
    cover_adq.download_images(cover_adq.games_df)
