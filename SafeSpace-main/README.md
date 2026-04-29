# 🌿 SafeSpace — Controle de Humor

Aplicação TUI (Terminal User Interface) de controle e acompanhamento de humor,
construída com **Python + Textual + SQLite**.

---

## 📁 Estrutura do Projeto

```
safespace/
├── main.py                    # Ponto de entrada da aplicação
├── requirements.txt           # Dependências Python
├── config/
│   └── database.py            # Conexão e inicialização do SQLite
├── models/
│   ├── user_model.py          # CRUD de usuários (registro, login)
│   └── mood_model.py          # CRUD de registros de humor
├── screens/
│   ├── home_screen.py         # Tela inicial (login / cadastro)
│   ├── login_screen.py        # Tela de autenticação
│   ├── register_screen.py     # Tela de cadastro com validações
│   ├── menu_screen.py         # Menu principal pós-login
│   ├── tracking_screen.py     # Registro de humor com emojis
│   ├── reports_screen.py      # Relatórios semanais/mensais em gráfico ASCII
│   └── emergency_screen.py    # Simulação de chamada de emergência
└── utils/
    ├── validators.py          # Validação de email, senha e telefone
    └── mood_utils.py          # Emojis, cálculo de médias, geração de gráficos
```

---

## ⚙️ Requisitos

- Python 3.10+
- pip

> O SQLite já vem incluído no Python, não é necessário instalar nenhum servidor de banco de dados.

---

## 🚀 Instalação e Execução

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Execute a aplicação

```bash
python main.py
```

> Na primeira execução o arquivo `safespace.db` é criado automaticamente na pasta do projeto. Nenhuma configuração adicional é necessária.

---

## 🎮 Controles e Navegação

| Tecla     | Ação                            |
|-----------|---------------------------------|
| `ESC`     | Voltar para a tela anterior     |
| `Q`       | Sair da aplicação               |
| `←` / `→` | Navegar entre períodos (relatórios) |
| `Enter`   | Submeter formulários            |
| `Tab`     | Navegar entre campos            |

---

## 🌟 Funcionalidades

### Tela Inicial
- Opções de Login e Cadastro

### Cadastro
- Validação de email (domínios aceitos: Gmail, Hotmail, Outlook, UFRPE, etc.)
- Validação de senha: mín. 8 chars, 1 maiúscula, 2 números, 1 caractere especial
- Confirmação de senha
- Contato de emergência opcional (formato telefone brasileiro)

### Tracking de Humor
- 6 níveis de humor representados por emojis:
  - 😭 Muito Triste (1)
  - 😢 Triste (2)
  - 😐 Neutro (3)
  - 🙂 Bem (4)
  - 😊 Feliz (5)
  - 😁 Muito Feliz (6)
- Campo de descrição opcional
- Múltiplos registros por dia com timestamp

### Relatórios
- Visualização por **semana** ou **mês**
- Navegação para períodos anteriores com dados
- Gráfico de barras ASCII com flutuação de humor
- Média diária (quando há múltiplos registros no dia)
- Média geral do período com emoji

### Emergência
- Simulação de ligação para o contato cadastrado
- Retorno automático ao menu após 3 segundos

---

## 🗄️ Banco de Dados

O banco de dados é um arquivo **`safespace.db`** criado automaticamente na raiz do projeto ao iniciar a aplicação pela primeira vez. Por usar SQLite, não requer nenhum servidor ou configuração externa.

### Tabela `users`
| Campo              | Tipo     | Descrição                         |
|--------------------|----------|-----------------------------------|
| id                 | INTEGER PK | Identificador único (autoincrement) |
| email              | TEXT     | Email único do usuário            |
| password_hash      | TEXT     | Hash SHA-256 com salt             |
| emergency_contact  | TEXT     | Telefone de emergência (opcional) |
| created_at         | TEXT     | Data de cadastro                  |

### Tabela `mood_entries`
| Campo       | Tipo    | Descrição                             |
|-------------|---------|---------------------------------------|
| id          | INTEGER PK | Identificador único (autoincrement) |
| user_id     | INTEGER FK | Referência ao usuário              |
| mood_level  | INTEGER | Nível de humor (1–6)                  |
| description | TEXT    | Descrição opcional do estado          |
| recorded_at | TEXT    | Data e hora exatas do registro        |
