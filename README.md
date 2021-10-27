# Quantificando a disrupção em redes de similaridade musicais
<p align="center">
  <img src="https://i.imgur.com/ypbO8JZ.png" alt="disruption" width="400" height="200"/>
</p>
Este repositório organiza os meus estudos, progressos e análises do Trabalho de Conclusão de Curso.

O meu trabalho é sobre a quantificação da disrupção em redes de similaridade musicais e também como os usuários navegam por estas redes.

# Introdução

Ao analisar a influência musical através de redes complexas é possível tirar conclusões quantitativas de como as influências modelam a forma que artistas e grupos produzem música, provendo informações valiosas das tendências e inovações músico-culturais. 

Recentemente surgiram trabalhos baseados em uma métrica de rede proposta por [Funk $\&$ Owen-Smith](http://russellfunk.org/cdindex/static/funk_ms_2016.pdf) para medir as influências desestabilizadoras e consolidadoras, chamada disrupção.

Originalmente foi utilizada para analisar as mudanças tecnológicas no domínio das patentes para demonstrar de forma geral que um objeto disruptivo é aquele que cria um novo fluxo de eventos, mudando a maneira tradicional de como um contexto geralmente funciona, mostrando assim quais eram as patentes inovadoras ao longo do tempo.

Este trabalho visa explorar o potencial musicológico da métrica em redes de múltiplos gêneros musicais para poder entender como foi a evolução da música, seus gêneros, assim como artistas e músicas disruptivas.

# Dataset

O conjunto de dados utilizado foi o [Music4All](https://sites.google.com/view/contact4music4all) que contém 16.269 artistas, 38.363 álbuns, 109.269 músicas. 

Para cada uma das músicas têm-se os metadados, tags, informações dos gêneros das músicas, clipes de áudio de 30 segundos, letras, somando ao todo 16 metadados extraídos através da API do Spotify. Além disso, é disponibilizado o histórico de músicas ouvidas por 15.602 usuários anônimos. 

# Representação de Similaridade e Extração de Atributos

Para estimar a similaridade entre músicas é necessário uma forma de comparação entre elas, logo é necessário uma representação das músicas que possibilite a sua análise.

Para este trabalho foram utilizadas e testadas duas representações:
- MFCC
- [Transfer Learning Feature](https://github.com/keunwoochoi/transfer_learning_music)

<p align="center">
  <img src="https://github.com/keunwoochoi/transfer_learning_music/raw/master/diagram.png" alt="workflow" width="400" height="390" />
</p>


Em especial depois de feitos os testes a feature do transfer learning para foi utilizada para todos os testes seguintes e na construção da rede, já que o MFCC não foi bem representativo, devido à grande quantidade de gêneros musicais.

Para a facilidade da extração das features para qualquer música foi feita uma imagem Dockerfile já configurada para gerar as features para uma pasta de músicas.

# Experimentos
<p align="center">
  <img src="https://i.imgur.com/aXNcYlL.png" alt="workflow" />
</p>

A maior parte dos experimentos se encontra na pasta code/experiments. 
Nesta se encontram os dois experimentos feitos:

1. Utilizando todas as músicas de 1923 até 2002
2. Utilizando uma amostragem de 30.000 músicas de 1928 até 2019

Os experimentos visam explorar o potencial musicológico da métrica da disrupção.

# Resultados

Os resultados finais podem ser encontrados em Relatório_Final.pdf, este mostra de forma mais concisa e estruturada os resultados obtidos nos experimentos