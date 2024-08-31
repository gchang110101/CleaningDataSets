# Gabriel Chang
import pandas as pd

netflix_file_name = "netflix_titles.csv"

# una pequeña funcion para retornar si o no, basado en un contador
def determinar_presencia_tv(contador):
    if contador > 1:
        return 'yes'
    else:
        return 'no'

# funcion para recibir un data frame, y crear un nuevo csv con la data transformada
def crear_csv_data_frame(df):
    df.to_csv('cleaned_netflix_titles.csv', index = False)

# funcion principal
def  cleaningNetflixData():
    data_frame = pd.read_csv(netflix_file_name)
    #pd.set_option('display.max_colwidth', None)

    # 1 - Seccion de "Look into your Data"
    print("\nRow Count: ", data_frame.shape[0])
    print("Column Count: " , data_frame.shape[1], '\n')
    print("Imprimir un par de registros: ")
    print(data_frame[['title', 'director', 'cast', 'country', 'release_year', 'rating', 'duration']].sample(5), '\n')

    # 2 - Seccion de "Look at the proportion of missing data" (con redondeo a los primeros 2 decimales)
    # de momento, no eliminaré ninguna columna, ya que las que tienen mayor porcentaje de data faltante,
    # director, cast, y country, son bastantes relevantes
    print("\nPorcentaje de datos faltantes por columnas: ")
    print(data_frame.isnull().mean() * 100, 2)

    # 3 - Seccion de "Check the data type of each column"
    print("\nColumn data types: ")
    print(data_frame.dtypes)

    # 4 - Seccion de "Check for trailing whitespaces"
    # haré strip de las columnas "title" y "description", siendo estas las que contienen
    # cadenas mas largas.
    data_frame['title'].str.strip()
    data_frame['description'].str.strip()

    print('\n' , data_frame['title'].sample(3))
    print('\n' , data_frame['description'].sample(3))
    
    # 5 - Seccion de Dealing with Missing Values - segun formato de valores existentes
    # para director -> "NO DIRECTOR FOUND"
    # para cast -> "CAST INFO N/A"
    # para country -> "COUNTRY NOT SPECIFIED"
    # para date added -> "----"
    # para rating -> "N/A"
    # para duration -> "--- min"
    data_frame['director'] = data_frame['director'].fillna("NO DIRECTOR FOUND")
    data_frame['cast'] = data_frame['cast'].fillna("CAST INFO N/A")
    data_frame['country'] = data_frame['country'].fillna("COUNTRY NOT SPECIFIED")
    data_frame['date_added'] = data_frame['date_added'].fillna("----")
    data_frame['rating'] = data_frame['rating'].fillna("N/A")
    data_frame['duration'] = data_frame['duration'].fillna("--- min")

    # 6 - Extracting more information from your dataset to get more variables
    # haré dos nuevas columnas ("seasons" y "duration_in_minutes") basadas en los valores de "duration"
    # si una fila trae "X Seasons", guardaremos el valor X en "seasons" (y "---" en "duration_in_minutes")
    # si una fial trae "XYZ min", guardaremos el valor XYZ en "duration_in_minutes" (y "-" en "seasons")
    # utilizaré expresiones regulares, primero para encontrar los casos que son minutos, y luego para seasons
    data_frame['duration_in_minutes'] = data_frame['duration'].str.extract(r'(\d+)\smin', expand = False)
    data_frame['duration_in_minutes'] = data_frame['duration_in_minutes'].fillna('---')

    data_frame['seasons'] = data_frame['duration'].str.extract(r'(\d+)\s[Ss]eason', expand=False)
    data_frame['seasons'] = data_frame['seasons'].fillna('-')
    
    print('\n' , data_frame[['duration', 'duration_in_minutes', 'seasons']].head(20))

    # 7 - Check the unique values of columns
    # usaré la columna "listed_in", porque varios valores únicos realmente se pueden generalizar 
    # el mismo valor o cadena, si es que no afecta nuestro análisis. En este caso, varias filas
    # tienen muchas variaciones de "TV" entonces crearé una columna "high_tv_presence" para
    # llenar "yes" o "no" en filas que repitan dicha palabra mas de una vez
    uq_listed_in = data_frame['listed_in'].unique()

    print('\n', uq_listed_in)

    data_frame['high_tv_presence'] = data_frame['listed_in'].str.count('TV')

    data_frame['high_tv_presence'] = data_frame['high_tv_presence'].apply(determinar_presencia_tv)

    print('\n', data_frame[['listed_in', 'high_tv_presence']].sample(10), '\n')

    # creamos un nuevo archivo csv basado en los datos limpiados/transformados
    crear_csv_data_frame(data_frame)


cleaningNetflixData()