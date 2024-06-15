<h1 align="center">
    <img alt="RVM" src="https://github.com/sbcwebmedia2024/recsys-depolarize-fair/blob/main/assets/logo.jpg" />
</h1>

<h3 align="center">
  RecSys-Depolarize-Fair
</h3>

<p align="center">: Elaboração de uma Estratégia de Despolarização e Justiça Individual em Sistemas de Recomendação. </p>

<p align="center">
  <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/sbcwebmedia2024/recsys-depolarize-fair?color=%2304D361">

  <img alt="License" src="https://img.shields.io/badge/license-MIT-%2304D361">

  <a href="https://github.com/sbcwebmedia2024/recsys-depolarize-fair/stargazers">
    <img alt="Stargazers" src="https://img.shields.io/github/stars/sbcwebmedia2024/recsys-depolarize-fair?style=social">
  </a>
</p>

<p align="center">
  <a href="#-sobre">Sobre o projeto</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
</p>

## :page_with_curl: Sobre o projeto <a name="-sobre"/></a>

Sistemas de recomendação são essenciais para ajudar os usuários a encontrar conteúdo relevante, mas enfrentam desafios como bolhas de filtro e justiça individual de itens. Bolhas de filtro limitam a exposição a informações diversas, e a injustiça impede a recomendação equitativa de itens menos populares. Este artigo apresenta o RecSys-Depolarize-Fair, uma estrutura para reduzir a polarização e promover recomendações justas, utilizando métricas de polarização e justiça para os itens. Experimentos mostram que o algoritmo reduz efetivamente a polarização e equilibra as recomendações sem afetar significativamente a precisão. 

### :balance_scale: Medidas de Justiça <a name="-medidas"/></a>

* **Polarization (Polarização)**: Para capturar a polarização, buscamos medir a extensão na qual as avaliações dos usuários discordam. Assim, para medir a polarização dos usuários, consideramos as avaliações estimadas `$\hat{X}$`, e definimos a métrica de polarização como a soma normalizada das distâncias euclidianas entre pares de avaliações estimadas de usuários, isto é, entre linhas de `$\hat{X}$`.

* **Individual fairness (Justiça Individual)**: Para cada item `$j$`, definimos `$\ell_j$`, a perda do item `$j$`, como o erro quadrático médio da estimativa sobre as avaliações conhecidas do item `$j$`.


### :chart_with_upwards_trend: Resultados(s) <a name="-resultados"/></a>

[Link para o arquivo Excel](https://github.com/sbcwebmedia2024/recsys-depolarize-fair/blob/main/_results-article.xlsx)


### Arquivos

| Arquivo                               | Descrição                                                                                                                                                                                                                                   |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AlgorithmDepolarizeFair                | Classe para implementar justiça e despolarização das recomendações de algoritmos de sistemas de recomendação.                                                                                               |
| AlgorithmUserFairness                | Classes para medir a justiça (polarização, justiça individual e justiça do grupo) das recomendações de algoritmos de sistemas de recomendação.                                                                                               |
| RecSys                               | Classe no padrão fábrica para instanciar um sistema de recomendação com base em parâmetros string.                                                                                                                                           |
| RecSysALS                            | Alternating Least Squares (ALS) para Filtragem Colaborativa é um algoritmo que otimiza iterativamente duas matrizes para melhor prever avaliações de usuários em itens, baseando-se na ideia de fatoração de matrizes.                       |
| RecSysKNN                            | K-Nearest Neighbors para Sistemas de Recomendação é um método que recomenda itens ou usuários baseando-se na proximidade ou similaridade entre eles, utilizando a técnica dos K vizinhos mais próximos.                                      |
| RecSysNMF                            | Non-Negative Matrix Factorization para Sistemas de Recomendação utiliza a decomposição de uma matriz de avaliações em duas matrizes de fatores não-negativos, revelando padrões latentes que podem ser usados para prever avaliações faltantes. |
| RecSysSGD                            | Stochastic Gradient Descent para Sistemas de Recomendação é uma técnica de otimização que ajusta iterativamente os parâmetros do modelo para minimizar o erro nas previsões de avaliações, através de atualizações baseadas em gradientes calculados de forma estocástica. |
| RecSysSVD                            | Singular Value Decomposition para Sistemas de Recomendação é um método que fatora a matriz de avaliações em três matrizes menores, capturando informações essenciais sobre usuários e itens, o que facilita a recomendação através da reconstrução da matriz original com dados faltantes preenchidos. |
| RecSysNCF                            | Neural Collaborative Filtering é uma abordagem moderna para filtragem colaborativa que utiliza redes neurais para modelar interações complexas e não-lineares entre usuários e itens, visando aprimorar a qualidade das recomendações.          |
| TestAlgorithmDepolarizeFair        | Script de teste do algoritmo de despolarização e justiça (AlgorithmDepolarizeFair) |

---
