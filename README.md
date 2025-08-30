# Sistema de Controle Financeiro

Um sistema completo de controle financeiro pessoal desenvolvido com Django, permitindo gerenciar receitas, despesas, contas e visualizar relatórios.

## Funcionalidades

- Cadastro e autenticação de usuários
- Gerenciamento de categorias (receitas e despesas)
- Gerenciamento de contas bancárias
- Registro de transações financeiras
- Dashboard com resumo financeiro
- Relatórios mensais com gráficos
- Interface responsiva com Bootstrap

## Requisitos

- Python 3.8+
- Django 5.2+
- Outras dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório ou baixe os arquivos

2. Crie e ative um ambiente virtual Python:

```
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Instale as dependências:

```
pip install django django-crispy-forms pillow matplotlib
```

4. Execute as migrações:

```
python manage.py makemigrations
python manage.py migrate
```

5. Crie um superusuário:

```
python manage.py createsuperuser
```

6. Inicie o servidor de desenvolvimento:

```
python manage.py runserver
```

7. Acesse o sistema em `http://127.0.0.1:8000/`

## Uso

### Primeiro acesso

1. Acesse o painel administrativo em `http://127.0.0.1:8000/admin/` e faça login com o superusuário criado
2. Crie algumas categorias de receitas e despesas
3. Crie pelo menos uma conta bancária
4. Comece a registrar suas transações

### Funcionalidades principais

- **Dashboard**: Visualize um resumo das suas finanças, incluindo saldo atual, receitas e despesas do mês
- **Categorias**: Gerencie categorias para organizar suas transações
- **Contas**: Adicione e gerencie suas contas bancárias
- **Transações**: Registre receitas e despesas
- **Relatórios**: Visualize relatórios mensais com gráficos

## Estrutura do Projeto

- `controle/`: Aplicação principal
  - `models.py`: Modelos de dados (Categoria, Conta, Transacao)
  - `views.py`: Lógica de visualização
  - `forms.py`: Formulários para entrada de dados
  - `urls.py`: Configuração de URLs
  - `templates/`: Templates HTML
  - `static/`: Arquivos estáticos (CSS, JS)

- `financeiro/`: Configurações do projeto Django

## Personalização

Você pode personalizar o sistema editando os templates em `controle/templates/controle/` e os estilos em `controle/static/controle/css/style.css`.

## Licença

Este projeto é distribuído sob a licença MIT. Sinta-se livre para usar, modificar e distribuir conforme necessário.