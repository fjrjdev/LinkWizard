# LinkWizard

Essa aplicação de gerenciamento de links permite criar, ler, atualizar e excluir links com uma URL e um título/label. Com esta API, os usuários podem gerenciar facilmente sua lista de links favoritos ou importantes, bem como compartilhar links com outras pessoas. Os usuários podem criar novos links, visualizar links existentes, editar o título/label ou a URL dos links e excluir links indesejados.

## APIs

O projeto possui as seguintes APIs RESTful:

- `POST /api/create`: Cadastra um novo usuário no sistema.
- `POST /api/login`: Loga o usuário no sistema.
- `GET /api/links`: Retorna a lista de links criados pelo usuario.
- `POST /api/links`: Cria um novo link.
- `GET /api/webcrawler/start`: Inicia um webcrawler para extrair as urls do site [Devgo](https://devgo.com.br/).

Veja a documentação completa das APIs em [Docs](https://djangowebcrawler.onrender.com/api/docs/).

## Banco de Dados

O projeto usa um banco de dados relacional PostgreSQL. A estrutura do banco de dados inclui as seguintes tabelas:

- `users`: Armazena informações dos usuários cadastrados no sistema.
- `links`: Armazena informações dos links feitos pelos usuários.

## Iniciando o projeto backend com Docker

<br>

- **Etapa 1: clonar o repositório**

```
git@github.com:fjrjdev/API_Manage_Links.git
```

Nota: Caso já tenha clonado pule essa etapa

- **Etapa 2: Abra o diretório do repositório clonado**

```
cd API_Manage_Links
```

- **Etapa 3: Criar o arquivo .env**

Para preencher o arquivo .env com as informações necessárias, siga os passos a seguir:

```
crie um novo arquivo com o nome .env. É importante que o nome do arquivo comece com um ponto para que ele seja oculto.

Copie o conteúdo do arquivo .env.example (se existir) para o arquivo .env recém-criado.

Para preencher as informações do banco de dados PostgreSQL, adicione o nome do banco de dados na variável POSTGRES_DB, o nome de usuário do PostgreSQL na variável POSTGRES_USER e a senha do usuário na variável POSTGRES_PASSWORD.

Para preencher a chave secreta, adicione uma string aleatória na variável SECRET_KEY.

Por fim, para configurar o host do banco de dados, substitua o valor da variável DB_HOST por 127.0.0.1 se quiser rodar o projeto sem o Docker ou db se quiser usar o Docker.

Salve o arquivo .env e certifique-se de que ele está na raiz do projeto.


Pronto! Agora, as informações do banco de dados e a chave secreta estão configuradas no arquivo .env.
```

- **Etapa 3: Criar o aplicativo**

```
docker compose up --build
```

Esse comando criará as imagens e os contêineres necessários para o aplicativo.

- **Step 4: Start the application**

```
docker compose up
```

- **Etapa 5: Acessar o aplicativo**
- Visite no seu navegador da Web.

```
http://localhost:8000/
```

Nota: Certifique-se de ter o docker em seu sistema antes de executar os comandos acima.

## Web Crawler

Depedencias:

- Django Rest Framework
- scrapy
- multiprocessing

O módulo multiprocessing é usado nesse caso para executar o webcrawler em paralelo, utilizando múltiplos processos. A função run_spider é executada em um processo separado com o auxílio do ProcessPoolExecutor, que gerencia a criação e execução de múltiplos processos, nesse caso até quatro processos.

Cada processo possui sua própria instância do interpretador Python e pode executar o mesmo código de maneira independente, o que é especialmente útil em operações intensivas em CPU, como é o caso do web crawler. Isso ajuda a acelerar a execução do código, reduzindo o tempo total de execução.

Como fucinona o processo de execução do web crawler:

- O usuário envia uma solicitação GET para o servidor.
- O servidor valida o token e a permissão do usuário autenticado.
- O servidor inicia um webcrawler para extrair dados usando a biblioteca CrawlerRunner.
- A View retorna um status 202 Accepted e uma mensagem indicando que a solicitação foi recebida e está sendo processada
- Quando o rastreamento estiver concluído, a view salva os dados extraídos no banco de dados.
