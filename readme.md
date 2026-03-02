# Gerenciamento de Redes (estrutura inicial)

Projeto inicial para gerenciamento de dispositivos de rede com Python e MySQL.

## Objetivo

Disponibilizar uma base organizada para evolucao do software com:

- configuracao por variaveis de ambiente;
- conexao com banco MySQL;
- camada de dominio, repositorio e servico;
- CLI para operacoes basicas;
- testes unitarios iniciais.

## Estrutura

```text
.
├── docker-compose.yml
├── pyproject.toml
├── sql/
│   └── schema.sql
├── src/
│   └── gerenciamento_redes/
│       ├── cli.py
│       ├── config.py
│       ├── db.py
│       ├── main.py
│       ├── models.py
│       ├── repositories/
│       │   └── device_repository.py
│       └── services/
│           └── network_service.py
└── tests/
    ├── test_config.py
    └── test_network_service.py
```

## Requisitos

- Python 3.10+
- Docker e Docker Compose (opcional, recomendado para MySQL local)

## Configuracao rapida

1. Crie um ambiente virtual:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Instale dependencias:

   ```bash
   pip install -e .
   ```

3. Copie o arquivo de ambiente:

   ```bash
   cp .env.example .env
   ```

4. Suba o MySQL com Docker:

   ```bash
   docker compose up -d
   ```

O arquivo `sql/schema.sql` sera executado automaticamente na primeira inicializacao do container.

## Uso da CLI

Cadastrar dispositivo:

```bash
python -m gerenciamento_redes.main cadastrar --nome Switch-01 --ip 10.0.0.10 --tipo switch
```

Listar dispositivos:

```bash
python -m gerenciamento_redes.main listar
```

Atualizar status:

```bash
python -m gerenciamento_redes.main status --id 1 --status manutencao
```

Status permitidos: `ativo`, `manutencao`, `inativo`.

## Rodando testes

```bash
python -m unittest discover -s tests -v
```

## Proximos passos sugeridos

- adicionar autenticacao e perfis de acesso;
- criar API HTTP (ex.: FastAPI) sobre os servicos;
- expandir modelo para links, VLANs, incidentes e alertas;
- incluir migracoes versionadas de banco (Alembic/Flyway).
