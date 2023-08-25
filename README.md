# Project: AirCrashesFatalities
*App to analyze and visualize data of air accidents with fatalities in the world*

Um pequeno projeto para visualização de acidêntes aéreos com fatalidade que ocorreram ao longo do tempo. Alguns desafios a solucionar, o arquivo csv não possui a latitude e 
longitude dos acidêntes, somente a descrição do local, que ajuda, entretando, meu objetivo inicial era exibir os pontos exatos do acidêntes e o número de vitimas e sobreviventes,
entretando, criei um script para obter a latitude e longitude através do metódo abaixo:

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
Funcionou, apesar de aguardar mais de 5mil requisições para obter cada coordenadas (vou pensar em obter em lote), muitas coordenadas não incorretas, muito se deve a 
descrição do localização do acidênte (Terei de tratar esse campo no csv). Assim sendo, para criar meu primeiro MVP (Produto minimamente viável), apenas adicionei widgets para
filtrar a tabela e o gráfico. Isto posto, o gráfico ilustra a curva de acidêntes ao longo do tempo e uma média suavizada.

Ainda vou implementar os locais dos acidêntes e gerar um gráfico com a rotas de cada aeronave, mas preciso melhorar a obtenção das coordenadas. Abaixo as imagens do app:

![image](https://github.com/gbaere/AirCrashesFatalities/assets/397533/fe0b520b-b3c1-4768-a11e-533af4c32dde)

![image](https://github.com/gbaere/AirCrashesFatalities/assets/397533/c120243b-befb-47fb-b45e-f21741e49ef5)


