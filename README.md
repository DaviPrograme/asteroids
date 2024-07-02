# Asteroids

Recrie o clássico jogo [Asteroids](https://en.wikipedia.org/wiki/Asteroids_(video_game)) usando Python para o frontend e backend e PostgreSQL para armazenar as informações. O jogo incluirá funcionalidades básicas como controle da nave espacial, movimento dos asteroides, detecção de colisões, contagem de pontos, conquistas dos jogadores e um histórico de pontuações. Os dados do jogo, como pontuações mais altas, serão armazenados em um banco de dados PostgreSQL.

![Asteroids Photo](./readme/asteroids.gif)

## Objetivo

O objetivo principal deste projeto é dividido igualmente entre aprender Python e SQL. A ideia é se familiarizar com o ecossistema de bibliotecas, documentação da linguagem e sites conhecidos, tais como a documentação oficial do Python e Pygame, assim como interagir diretamente com um banco de dados PostgreSQL usando SQL através do Python. O jogo apenas serve como uma desculpa legal e prática para alcançar esses objetivos.

## Instruções

### Frontend

- **Python**
    - Implemente a lógica do jogo usando Python com a biblioteca [Pygame](https://www.pygame.org/news). As principais funcionalidades incluem:
        - **Loop:** Crie um loop do jogo para lidar com a renderização e atualização do estado do jogo em uma taxa de quadros especificada.
        - **Colisões:** Implemente um sistema simples de detecção de colisões.
        - **Controle do jogo:** Capture o teclado para controle da nave (impulso, rotação, disparo).
        - **Menu:** Implemente um menu inicial onde os jogadores podem acessar o leaderboard antes de iniciar o jogo.

### Backend

- **Gerenciamento de Dados**
    - Use `psycopg2` para gerenciar a interação com o banco de dados PostgreSQL. Garanta que as pontuações e outras informações do jogo sejam armazenadas e recuperadas de forma eficiente.
    - Extrair os dados do PostgreSQL utilizando a ferramenta Airbyte, que gerencia a extração e carregamento de dados através de conectores.
    - Transformar os dados de um Banco na ferramenta ClickHouse onde os dados ja foram previamente carregados pelo Airbyte.
    - Analisar e apresentar dados e pesquisas utilizando a ferramenta Metabase que permite criar gráficos analíticos.

### Banco de dados

- **PostgreSQL**
    - Crie um schema de banco de dados no PostgreSQL para armazenar as informações do jogo. Tabelas necessárias:
        - **players (id, player_name):** Armazena informações sobre cada jogador.
        - **high_scores (id, player_id, score, date):** Registra as pontuações mais altas individuais, juntamente com o jogador associado e o timestamp.
        - **score_history (id, player_id, score, date):** Registra os históricos de pontuações mais altas para cada jogador.
        - **achievements (id, achievement_name, description):** Armazena diferentes conquistas que os jogadores podem ganhar.
        - **player_achievements (player_id, achievement_id, date_earned):** Registra quais conquistas cada jogador ganhou e quando.
- **ClickHouse**
    - O ClickHouse é um sistema de gerenciamento de banco de dados SQL orientado a colunas e de alto desempenho para processamento analítico online.
    - Utilizamos para receber e tratar os dados que são extraídos do PostgreSQL
    - Ao invés de tabelas criamos view para conseguir lidar com esses dados de forma mais eficaz no próximo passo.

### Ferramentas
- **Airbyte**
    - Plataforma de integração de dados
    - Esta ferramenta nos ajuda a conectar o Banco de Dados PostgreSQL ao Banco de Dados ClickHouse

- **Metabase**
    - Ferramenta de relatórios e BI que permite criar relatórios e dashboards.
    - Com esta ferramenta analisamos dados como:
        - ***Gráfico de barras***: Jogadores com as maiores pontuações em ordem decrescente.
        - ***Gráfico de dispersão***: Pontuações em diferentes datas.
        - ***Gráfico de barras***: Quantidade de conquistas por jogador.
        - ***Gráfico de barras***: Pontuação média de cada jogador em ordem decrescente.

### Expansão
#### Fizemos a implentação de um etl em nosso banco de dados
- ETL (Extract, Transform, Load) é um processo de integração de dados que envolve três etapas principais: extrair dados de várias fontes, transformá-los para atender às necessidades de negócios ou formatos específicos e carregá-los em um sistema de destino, como um data warehouse. O propósito do ETL é consolidar dados dispersos, garantir a qualidade dos dados e facilitar a análise e a tomada de decisões.


### Implementação

- **Setup**
    - Toda da estrutura de dados do projeto roda em sistemas dockerizados, para executar o projeto será necessário ter o docker e docker-compose instalados.
    - Passo 1: Clonar o repositório
    ```bash
    git clone https://github.com/DaviPrograme/asteroids.git
    ``` 
    - Passo 2: Iniciar Submodules e criar a venv python
    ```bash
    make init
    ```
    - Passo 3: Acessar a venv
    ```bash
    source ./venv/bin/activate && pip install -r requirements.txt
    ```
    - Passo 4: Inicializar todos os Contêiners
    ```bash
    make
    ```
    - Passo 5: Inicializar o PostgreSQL
    ```bash
    python backend/postgres/backend.py
    ```
    - Passo 6: Criar os conectores no Airbyte(a conexão será manual pela plataforma)
    ```bash
    python services/airbyte/create_connection.py
    ```
    - Passo 7: Criar os conectores no Airbyte(a conexão será manual pela plataforma)
    ```url
    acesse em seu navegador: localhost:8000
    user: airbyte
    password: password
    ```
    ##### Siga os passos abaixo:
    ![](/readme/airbyte_cropped)

    #### no fim, sua tela deve estar parecida com esta:
    
    ![](/readme/airbyte_finish.png)
    - Caso tenha DBeaver instalado o clickhouse tera o banco "airbyte_internal"
    ![](/readme/dbv_internal.png)

    - Passo 8: Inicializar o ClickHouse. Este script gera as views necessárias para a visualização no Metabase

    ```bash
    python backend/clickhouse/clickhouse.py
    ```
    ![](/readme/views.png)

    - Passo 9: Acessar o Metabase
    ```
    acesse: localhost:3000
    siga os passos iniciais
    em seguida garanta que esta tela tenha os mesmos dados: 
    ```
    ![](./readme/metabase.png)

    - Passo 10: Inicializar o Jogo. Isso serve para gerar dados (e se divertir um pouco)
    ```bash
    python frontend/frontend.py
    ```

    ##### Ultimo Passo
    - Montar alguns gráficos no Metabase

### Adicionais

- **Segurança:** Garanta que todos os inputs do jogador sejam sanitizados e seguros.
- **Flexibilidade:** Você pode precisar tomar decisões sobre features/detalhes adicionais, componentes da UI ou otimizações necessárias para melhorar o jogo.
- **Persistência de dados:** Garanta que as pontuações e os dados do jogo sejam armazenados de forma persistente no PostgreSQL e possam ser recuperados de maneira eficiente.
