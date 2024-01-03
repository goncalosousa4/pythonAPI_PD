import requests
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn


# Minha API key para o site OpenWeatherMap
api_key = 'a1d5318e63d38b59c63e7eb0e0691e14'   # dentro das ' '

# Lista de distritos de Portugal // Pode ser alterada para cidades inclusive de outros países
places = ['Aveiro', 'Beja', 'Braga', 'Bragança', 'Castelo Branco', 'Coimbra', 'Évora', 'Faro',
                      'Guarda', 'Leiria', 'Lisbon', 'Portalegre', 'Porto', 'Santarém', 'Setúbal', 'Viana do Castelo',
                      'Vila Real', 'Viseu', 'São João da Madeira', 'London']

# Lista para armazenar os dados de cada distrito
weather_data_list = []

for place in places:
    url = f'http://api.openweathermap.org/data/2.5/weather?q={place},&appid={api_key}'
    response = requests.get(url)


    if response.status_code == 200:
        data = response.json()

       
        weather_data = {
            'City': data['name'],
            'Temperature': round(data['main']['temp'] - 273.15),
            'Description': data['weather'][0]['description'],
            'Humidity': data['main']['humidity'],
            'Pressure': data['main']['pressure'],
            'Wind Speed': data['wind']['speed'],
            'Wind Direction': data['wind']['deg'],
            'Country': data['sys']['country'],
            'Sunrise': pd.to_datetime(data['sys']['sunrise'], unit='s'),
            'Sunset': pd.to_datetime(data['sys']['sunset'], unit='s')
        }

        
        weather_data_list.append(weather_data)
    else:
        print(f'Error {response.status_code}: Unable to retrieve data for {place}')

# DataFrame a partir da lista de dados
df = pd.DataFrame(weather_data_list)

print(df) # Print de um resumo do DataFrame 


# Montagem do DataFrame com pandas

mediaTemp = round(df['Temperature'].mean())
medianaSunset = df['Sunset'].median().strftime('%H:%M')
modaCeu = df['Description'].mode()[0].capitalize()

variancia = round(df['Temperature'].var(), 1)
desvioPadrao= round(df['Temperature'].std(), 1)
amplitude = df['Temperature'].max() - df['Temperature'].min()
quartis = df['Temperature'].quantile([0.25, 0.5, 0.75])



print(f"A Média da temperatura em Portugal é de {mediaTemp}ªC.")
print(f"A Mediana do pôr do sol em Portugal é às {medianaSunset}.")
print(f"A Moda do estado do céu em Portugal é {modaCeu}.")
print ("\n")
print(f"A Variância de temperatura é de: {variancia}ºC ")
print(f"O Desvio Padrão de temperatura é de: {desvioPadrao}ºC")
print(f"A Amplitude de temperatura é: {amplitude}ºC")
print(f"Os Quartis de temperatura são:\n{quartis}")

# Montagem dos gráficos

plt.figure(figsize=(10, 6))
plt.hist(df['Temperature'], bins=15, color='skyblue', edgecolor='black', alpha=0.7)
plt.title('Distribuição da Temperatura em Distritos de Portugal')
plt.xlabel('Temperatura (°C)')
plt.ylabel('Frequência')
plt.show()


plt.figure(figsize=(10, 6))
df['Description'].value_counts().plot(kind='barh', color='red')
plt.title('Estado do Céu em Distritos de Portugal')
plt.xlabel('Frequência')
plt.ylabel('Estado do Céu')
plt.show()

df.to_csv("dados_clima.csv", index=False)

#conda create -n my-env -c conda-forge spyder-kernels seaborn

