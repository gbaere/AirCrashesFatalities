# Project: AirCrashesFatalities
*App to analyze and visualize data of air accidents with fatalities in the world*

Um pequeno projeto para visualização de acidentes aéreos com fatalidade que ocorreram ao longo do tempo. Alguns desafios a solucionar, o arquivo csv não possui a latitude e 
longitude dos acidentes, somente a descrição do local, entretanto, meu objetivo inicial era exibir os pontos exatos dos acidentes e o número de vítimas e sobreviventes. 

Portanto, criei um script para obter a latitude e longitude para preencher as novas colunas (Latitude, Longitude) do meu dataframe, após o término criei um arquivo csv em que o nome adicionei o sufixo "clean. Abaixo está método para obter as coordenadas: (Existem vários API geolocation, pode alterar a sua preferência)


```python
def get_coordinates(location):
    if isinstance(location, str):
        url = f"https://nominatim.openstreetmap.org/search?q={format_location(location)}&format=json"
        st.write(url)
        response = requests.get(url)
        data = response.json()

        if data:
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            return latitude, longitude
        else:
            return None, None
    else:
        return None, None
  return None, None
```
Funcionou, apesar de aguardar mais de 5mil requisições para obter cada coordenadas (vou pensar em obter em lote), muitas coordenadas são incorretas, muito se deve a 
descrição da localização do acidênte (Terei de tratar esse campo no csv). Assim sendo, para criar meu primeiro MVP (Produto minimamente viável), apenas adicionei widgets para
filtrar a tabela e o gráfico. Isto posto, o gráfico ilustra a curva de acidentes ao longo do tempo e uma média suavizada.

Ainda vou implementar os locais dos acidentes e gerar um gráfico com a rotas de cada aeronave, mas preciso melhorar a obtenção das coordenadas. Abaixo as imagens do app:


![image](https://github.com/gbaere/AirCrashesFatalities/assets/397533/ebfbdd8d-f295-4c04-a153-79680c3c924b)


![image](https://github.com/gbaere/AirCrashesFatalities/assets/397533/0f2c392a-b5a0-4db4-ba97-f1e9eab8c8dd)

![image](https://github.com/gbaere/AirCrashesFatalities/assets/397533/24eb282d-7561-4fbe-9e2d-3bcfca2aba8d)

![image](https://github.com/gbaere/AirCrashesFatalities/assets/397533/e50200a2-1cc9-48b5-91b3-d3348560aa59)


![image](https://github.com/gbaere/AirCrashesFatalities/assets/397533/5d6c4cac-c25a-4e22-8556-2f59143d7d39)

![image](https://github.com/gbaere/AirCrashesFatalities/assets/397533/422d4529-b810-443e-aca4-504b3de4dc81)







