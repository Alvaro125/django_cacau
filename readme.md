# Gerador de Currículos - Backend

Backend da aplicação Gerador de Currículos, desenvolvido com Django REST Framework.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🚀 Instalação e Execução

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/django_cacau.git
cd django_cacau
```
### 2. Configure o ambiente virtual
```bash
python -m venv venv
venv\Scripts\activate
 ```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
 ```

### 4. Configure as variáveis de ambiente
Crie um arquivo .env na raiz do projeto com as seguintes variáveis:

```plaintext

 ```

### 5. Execute as migrações
```bash
python manage.py migrate
 ```

### 6. Crie um superusuário (opcional)
```bash
python manage.py createsuperuser
 ```

### 7. Inicie o servidor
```bash
python manage.py runserver
 ```

O servidor estará rodando em http://localhost:8000