# **CSI606-2024-02 - Trabalho Final - Resultados**

## *Discente: Laura Valamiel Andrade*

<!-- Este documento tem como objetivo apresentar o projeto desenvolvido, considerando o que foi definido na proposta e o produto final. -->

### Resumo

O sistema MoneyWise consiste em um site simples para controle de finanças pessoais, com o propósito de auxiliar os usuários no gerenciamento de suas finanças, registrando, categorizando e analisando as despesas. 
A aplicação, permite uma melhor organização financeira, ajudando os usuários a entender seus gastos com recursos essenciais para o controle financeiro e analisar as despesas. As principais funcionalidades incluem sistema de login, cadastro de receitas e despesas, exibição de um resumo financeiro, orçamento mensal e geração de relatórios.

### 1. Funcionalidades implementadas
- Login.
- Cadastrar usuário.
- Cadastro de receitas e despesas.
- Exibição do saldo atual, receita e despesas.
- Visualizar resumo do mês.
- Visualizar despesas por categoria e evolução das despesas.
- Visualizar resumo financeiro detalhado.
- Visualizar orçamento mensal e relatório.
  
### 2. Outras funcionalidades implementadas
-Editar dados do usuário (nome, email e número do celular).

### 3. Arquitetura do Projeto
### 3.1 Backend
-Framework: Flask.
-Banco de dados: PostgreSQL.
-APIs REST para as rotas ficarem mais organizadas e padronizadas.

### 3.2 Frontend
-Framework: React e Vite
-Estilização: uso de CSS.
-Interatividade: botões para ações.
-Integração: APIs REST para a comunicação entre o frontend e o backend.


### 4. Instruções para instalação e execução
### 4.1 Clonar o repositório
git clone https://github.com/usuario/repositorio.gt
cd repositorio
### 4.2 Instalar dependências
```bash
cd backend
pip install flask
pip install flask-cors
pip install requests
pip install pandas
pip install matplotlib
pip install psycopg2
pip install python-dateutil
```

Ou:
```bash
cd backend
pip install flask flask-cors requests pandas matplotlib psycopg2 python-dateutil
```
### 4.3 Executar o Backend
```bash
cd backend
python server.py
```
Disponível em: http://localhost:5000

### 4.4 Executar o Frontend
```bash
cd frontend/MoneyWise
npm run dev
```
Disponível em: http://localhost:5173
### 4.5 Testar o Sistema
1. Acessar o http://localhost:5173.
2. Realizar o cadastro no sistema.
3. Testar as funcionalidades do sistema, primeiro adicionar despesas e receitas para poder analisá-las.


