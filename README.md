# fast_zero

## Toda vez que abrir o projeto:

```bash
   poetry env use 3.13
```
```bash
   poetry env activate
```
```bash
   source /home/jorge.machado/.cache/pypoetry/virtualenvs/fast-zero-dVL4rHQI-py3.13/bin/activate
```
```bash
   fastapi dev fast_zero/app.py
```

## Ferramentas usadas:

### Poetry
#### Ferramenta para gerenciamento de dependências
```bash
   pipx install poetry
   pipx inject poetry poetry-plugin-shell
   poetry python install 3.13
   poetry env use 3.13
   poetry install
```

### FastAPI
#### Ferramenta para criar APIs
```bash
   poetry add fastapi[standard]
```

### Ruff
#### Ferramenta para análise estática de código(Um linter e formatador bem poderoso e rápido)
```bash
   poetry add --group dev ruff
```

### Pytest
#### Ferramenta para testes automatizados
```bash
   poetry add --group dev pytest pytest-cov
```

### taskipy
#### Ferramenta para automatizar tarefas(Um MakeFile do Python)
```bash
   poetry add --group dev taskipy
```

### sqlalchemy
#### Ferramenta para gerenciamento de banco de dados
```bash
   poetry add sqlalchemy
```

### pydantic-settings
#### Ferramenta para gerenciamento de configurações usando Pydantic
```bash
   poetry add pydantic-settings
```

### alembic
#### Ferramenta para gerenciamento de migrações de dados de banco de dados
```bash
   poetry add alembic
   // Cria a estrutura de pastas de migração.
   alembic init migrations
   // cria uma versão de dados.
   alembic revision --autogenerate -m "create users table"
   // Atualiza para a ultima versão.
   alembic upgrade head
   // Volta uma versão.
   alembic downgrade -1
   // Cria uma migração versão vazia, sem autogenerate
   alembic revision -m "create seeds"
   
```

### pwdlib
#### Ferramenta para gerenciamento de senhas
```bash
   poetry add "pwdlib[argon2]"
```

### JWT
#### Ferramenta para gerar tokens JWT
```bash
   poetry add pyjwt
```

### tzdata
#### Ferramenta para gerenciamento de fuso horário
```bash
   poetry add tzdata
```

### sqlalchemy[asyncio]
#### Ferramenta para gerenciamento de banco de dados com async
```bash
   poetry add "sqlalchemy[asyncio]"
```

### aiosqlite
#### Ferramenta para gerenciamento de banco de dados sqlite com async
```bash
   poetry add aiosqlite
```

### pytest-asyncio
#### Ferramenta para testes assíncronos
```bash
   poetry add --group dev pytest-asyncio
```


### Para gerar uma secret no python, basta entrar no python:
```bash
python

import secrets

secrets.token_hex()
```

### Para executar um unico teste, pode se usar o seguinte comando:
```bash
task test -k test_create_user
```

### Comando para saber todos os testes presentes no projeto.
```bash
task test --collect-only
```