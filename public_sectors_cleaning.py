# Gabriel Chang
import pandas as pd

public_sector_file = "Public_Sector_Emergency_Calls.csv"

# funcion para recibir un data frame, y crear un nuevo csv con la data transformada
def crear_csv_data_frame(df):
    df.to_csv('cleaned_public_sector_emergency_calls.csv', index = False)

# funcion principal
def  cleaning_Public_Sector_Emergency_Calls_Data():
    data_frame = pd.read_csv(public_sector_file)

    # 1 - Seccion de "Look into your Data"
    print("\nRow Count: ", data_frame.shape[0])
    print("Column Count: " , data_frame.shape[1], '\n')

    print("Imprimir un par de registros: ")
    print(data_frame[['Country', 'Incident #', 'Incident City', 'Incident Date', 'Incident Description', 'Time to Arrival (s)' , 'Time to Dispatch (s)']].sample(5))

    # 2 - Seccion de "Look at the proportion of missing data" (con redondeo a los primeros 2 decimales)
    # Igualmente, eliminaré la columnas columnas "Country" y "State", ya que son redundantes,
    # siendo todos los registros basados en Georgia, Estados Unidos
    print("\nPorcentaje de datos faltantes por columnas: ")
    print(data_frame.isnull().mean() * 100, 2)
    
    # drop de columna country
    data_frame = data_frame.drop('Country', axis = 1)
    data_frame = data_frame.drop('State', axis = 1)

    # 3 - Seccion de "Check the data type of each column"
    print("\nColumn data types: ")
    print(data_frame.dtypes)

    # 4 - Seccion de "Check for trailing whitespaces"
    # haré strip de las columnas "Incident Description" e "Incident Type", siendo estas las que contienen
    # cadenas mas largas.
    data_frame['Incident Description'].str.strip()
    data_frame['Incident Type'].str.strip()

    print('\n' , data_frame['Incident Description'].sample(3))
    print('\n' , data_frame['Incident Type'].sample(3))

    # 5 - Seccion de Dealing with Missing Values - ya que no se encuentran valores vacíos, reemplazamos
    # ciertos valores por otras frases indicativas de que hace falta un valor
    # igualmente, para las dos columans "Incident Position" y "Station Position", las rellenaré con
    # "(position not specified)", ya que todas bienen con el valor "Point", pero son relevantes como 
    # para borrarlas completamente
    data_frame['Incident Date'] = data_frame['Incident Date'].fillna("(NO DATE REGISTERED)")
    data_frame['Incident Description'] = data_frame['Incident Description'].fillna("(NO DESCRIPTION)")
    data_frame['Incident Type'] = data_frame['Incident Type'].fillna("(NO TYPE SPECIFIED)")
    data_frame['Incident Type Code'] = data_frame['Incident Type Code'].fillna("---")
    data_frame['Distance'] = data_frame['Distance'].fillna("---")
    data_frame['Time to Arrival (s)'] = data_frame['Time to Arrival (s)'].fillna("-")
    data_frame['Time to Dispatch (s)'] = data_frame['Time to Dispatch (s)'].fillna("-")
    data_frame['Time to Dispatch Target (s)'] = data_frame['Time to Dispatch Target (s)'].fillna("-")
    data_frame['Time to En Route (s)'] = data_frame['Time to En Route (s)'].fillna("-")
    data_frame['Time to En Route Target (s)'] = data_frame['Time to En Route Target (s)'].fillna("-")

    data_frame['Incident Position'] = '(INCIDENT POSITION NOT SPECIFIED)'
    data_frame['Station Position'] = '(STATION POSITION NOT SPECIFIED)'

    # 6 - Extracting more information from your dataset to get more variables
    # principalmente, me gustaría crear cuatro columnas agregadas basadas en el "Incident Date",
    # correspondientes a Day, Month, Year, y Time

    # antes de calcular dichas columnas agregadas, nos aseguramos que el formato de los valores en la columna
    # "Incident Date" se convierta a formato formal datetime, para poder trabajar con el atributo 'dt'
    data_frame['Incident Date'] = pd.to_datetime(data_frame['Incident Date'], format='%m/%d/%Y %I:%M:%S %p')

    data_frame['Day'] = data_frame['Incident Date'].dt.day
    data_frame['Month'] = data_frame['Incident Date'].dt.month
    data_frame['Year'] = data_frame['Incident Date'].dt.year
    data_frame['Time'] = data_frame['Incident Date'].dt.time

    print('\n', data_frame[['Day', 'Month', 'Year', 'Time']].sample(5))

    #   También me gustaría realizar un cálculo de proporción entre los Targets de 
    #   "Time to Dispatch" y "Time to En Route", para ver el cumplimiento de lo registrado con los Targets
    #   sera basado en un porcentaje
    #   dispatch time:
    data_frame['Dispatch Time/Target Ratio'] = (data_frame['Time to Dispatch (s)'] / data_frame['Time to Dispatch Target (s)']) * 100
    data_frame['Dispatch Time/Target Ratio'] = data_frame['Dispatch Time/Target Ratio'].astype(str) + '%'

    #   en route time:
    data_frame['En Route Time/Target Ratio'] = (data_frame['Time to En Route (s)'] / data_frame['Time to En Route Target (s)']) * 100
    data_frame['En Route Time/Target Ratio'] = data_frame['En Route Time/Target Ratio'].astype(str) + '%'


    print('\n', data_frame[['Time to Dispatch (s)', 'Time to Dispatch Target (s)', 'Dispatch Time/Target Ratio']].sample(2))
    print('\n', data_frame[['Time to En Route (s)', 'Time to En Route Target (s)', 'En Route Time/Target Ratio']].sample(2))

    # 7 - Check the unique values of columns
    # mediante este print, descubrí muchas similitudes en valores únicos de Incident Type,
    # como lo son todo lo relacionado a Fuego, Gas, Electriidad, y Vehículos
    # utilizaré expresiones regulares por cuestión de evitar lo case-sensitive o diferencias como 
    # "electric" con "electrical"
    uq_incident_type = data_frame['Incident Type'].unique()

    print('\n', uq_incident_type)

    # Generalizar tipos de incidentes:
    # fire regex:
    data_frame['Incident Type'] = data_frame['Incident Type'].str.replace(r'(?i).*fire.*', 'Fire Related', regex=True)

    # gas regex:
    data_frame['Incident Type'] = data_frame['Incident Type'].str.replace(r'(?i).*gas.*', 'Gas Related', regex=True)

    # vehicle regex:
    data_frame['Incident Type'] = data_frame['Incident Type'].str.replace(r'(?i).*vehicle.*', 'Vehicle(s) Involved', regex=True)

    # electric regex:
    data_frame['Incident Type'] = data_frame['Incident Type'].str.replace(r'(?i).*electric.*', 'Electric Incident', regex=True)

    print('\n', data_frame['Incident Type'].sample(10), '\n')

    # creo un nuevo csv con el data set transformado/limpiado desde el data frame:
    crear_csv_data_frame(data_frame)

cleaning_Public_Sector_Emergency_Calls_Data()