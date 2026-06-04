# 🌿 SafeSpace — Controle de Humor


###
Aplicação TUI (Terminal User Interface) de controle e acompanhamento de humor,
construída com **Python + Textual + SQLite**. 
###
---

## 📁 Estrutura do Projeto

~~~
safespace/
├── main.py                 # Ponto de entrada da aplicação
├── requirements.txt        # Dependências Python
├── generate_whitenoise.py  # Gerador do arquivo de ruído branco (rodar uma vez)
├── white_noise.wav         # Áudio de ruído branco para a tela de calma
├── database.py             # Conexão e inicialização do SQLite
├── user_model.py           # CRUD de usuários
├── mood_model.py           # CRUD de registros de humor
├── home_screen.py          # Tela inicial
├── login_screen.py         # Tela de autenticação
├── register_screen.py      # Tela de cadastro
├── menu_screen.py          # Menu principal pós-login
├── tracking_screen.py      # Registro de humor com emojis
├── reports_screen.py       # Relatórios semanais/mensais
├── emergency_screen.py     # Tela de contato de emergência
├── meltdown_screen.py      # Tela de momento de calma (técnica 5-4-3-2-1)
├── validators.py           # Validação de email, senha e telefone
├── mood_utils.py           # Emojis, médias e gráficos de humor
└── journal_utils.py        # Funções auxiliares para anotações
~~~~
---

## ⚙️ Requisitos

- Python 3.10+
- pip

> O SQLite já vem incluído no Python. Não é necessário instalar nenhum servidor de banco de dados.

---

## 🚀 Instalação e Execução

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Gere o arquivo de ruído branco (apenas na primeira vez)

```bash
python generate_whitenoise.py
```

### 3. Execute a aplicação

```bash
python main.py
```

> Na primeira execução o arquivo `safespace.db` é criado automaticamente. Nenhuma configuração adicional é necessária.

---

## Controles e Navegação

| Tecla     | Ação                        |
|-----------|-----------------------------|
| `ESC`     | Voltar para a tela anterior |
| `Q`       | Sair da aplicação           |
| `←` / `→` | Navegar entre relatórios    |
| `Enter`   | Submeter formulários        |
| `Tab`     | Navegar entre campos        |

---

##  Funcionalidades

### Tela Inicial
- Paleta visual suave em roxo, rosa e azul
- Opções de Login e Cadastro

### Cadastro
- Campo de nome de usuário
- Validação de email
- Validação de senha: mín. 8 chars, 1 maiúscula, 2 números, 1 caractere especial
- Confirmação de senha
- Contato de emergência opcional — aceita qualquer formato numérico e normaliza automaticamente para (XX) XXXXX-XXXX

### Login
- Opção "Lembrar de mim" — mantém a sessão entre usos do app
- Login automático ao reabrir o app quando sessão está salva

### Menu Principal
- Saudação personalizada com o nome do usuário
- Acesso a todas as funcionalidades

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
- Navegação para períodos anteriores
- Gráfico de barras ASCII com flutuação de humor
- Média diária e média geral do período com emoji

###  Momento de Calma
- Tela de baixo estímulo com paleta escura em tons de roxo
- Ruído branco real tocando em background durante toda a sessão
- Mensagens rotativas baseadas na técnica de grounding **5-4-3-2-1**:
  - 5 coisas que podem ser vistas
  - 4 coisas que podem ser tocadas
  - 3 coisas que podem ser ouvidas
  - 2 coisas que podem ser cheiradas
  - 1 coisa que pode ser saboreada
- Timer silencioso (sem contagem visível para não causar ansiedade)
- Duração configurável: 3, 5 ou 10 minutos (padrão: 3 min)
- Ao fim da sessão, três opções:
  - ✅ "Sim, estou melhor" → volta ao menu
  - 🔄 "Preciso de mais tempo" → reinicia a sessão
  - 🆘 "Ligar para emergência" → vai para a tela de emergência

### Emergência
- Exibe o contato de emergência cadastrado
- Retorno automático ao menu após 3 segundos
- Botão de cancelar disponível a qualquer momento

---

##  Banco de Dados

Arquivo **`safespace.db`** criado automaticamente na raiz do projeto.

### Tabela `users`
| Campo              | Tipo       | Descrição                           |
|--------------------|------------|-------------------------------------|
| id                 | INTEGER PK | Identificador único                 |
| name               | TEXT       | Nome do usuário                     |
| email              | TEXT       | Email único                         |
| password_hash      | TEXT       | Hash SHA-256 com salt               |
| emergency_contact  | TEXT       | Telefone de emergência (opcional)   |
| calm_timer         | INTEGER    | Duração da sessão de calma (min)    |
| created_at         | TEXT       | Data de cadastro                    |

### Tabela `mood_entries`
| Campo       | Tipo       | Descrição                        |
|-------------|------------|----------------------------------|
| id          | INTEGER PK | Identificador único              |
| user_id     | INTEGER FK | Referência ao usuário            |
| mood_level  | INTEGER    | Nível de humor (1–6)             |
| description | TEXT       | Descrição opcional               |
| recorded_at | TEXT       | Data e hora do registro          |

---

## Próximas Funcionalidades

- **Tela de Configurações** — ajuste do timer da sessão de calma (3, 5 ou 10 min) e outras preferências do usuário
- **Minijogo de Calma** — jogo simples e de baixo estímulo integrado ao app, usando pygame, voltado para regulação sensorial
- **Gamificação** — sistema de conquistas e recompensas para incentivar o uso consistente do app
- **Perfil do Usuário** — tela para editar nome, email e contato de emergência
