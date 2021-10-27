# Quantificando a disrupção em redes de similaridade musicais
![disruption](https://i.imgur.com/ypbO8JZ.png)

Este repositório organiza os meus estudos, progressos e análises do Trabalho de Conclusão de Curso.

O meu trabalho é sobre a quantificação da disrupção em redes de similaridade musicais e também como os usuários navegam por estas redes.


# Introdução
Ao analisar a influência musical através de redes complexas é possível tirar conclusões quantitativas de como as influências modelam a forma que artistas e grupos produzem música, provendo informações valiosas das tendências e inovações músico-culturais. 

Recentemente surgiram trabalhos baseados em uma métrica de rede proposta por [Funk $\&$ Owen-Smith](http://russellfunk.org/cdindex/static/funk_ms_2016.pdf) para medir as influências desestabilizadoras e consolidadoras, chamada disrupção.

Originalmente foi utilizada para analisar as mudanças tecnológicas no domínio das patentes para demonstrar de forma geral que um objeto disruptivo é aquele que cria um novo fluxo de eventos, mudando a maneira tradicional de como um contexto geralmente funciona, mostrando assim quais eram as patentes inovadoras ao longo do tempo.

Este trabalho visa explorar o potencial musicológico da métrica em redes de múltiplos gêneros musicais para poder entender como foi a evolução da música, seus gêneros, assim como artistas e músicas disruptivas.

# Representação de Similaridade e Extração de Atributos

Para estimar a similaridade entre músicas é necessário uma forma de comparação entre elas, logo é necessário uma representação das músicas que possibilite a sua análise.

Para este trabalho foram utilizadas e testadas duas representações:
- MFCC
- Transfer Learning Feature

Em especial foi escolhida a feature do transfer learning para os testes seguintes, já que o MFCC não foi bem representativo, devido ao conjunto de dados massivo.

# Experimentos

A maior parte dos experimentos se encontra na pasta code/experiments. 
Nesta se encontram os dois experimentos feitos:

1. Utilizando todas as músicas de 1923 até 2002
2. Utilizando uma amostragem de 30.000 músicas de 1928 até 2019

Os experimentos visam explorar o potencial musicológico da métrica da disrupção.

# Resultados

Os resultados finais podem ser encontrados em Relatório_Final.pdf, este mostra de forma mais concisa e estruturada os resultados obtidos nos experimentos