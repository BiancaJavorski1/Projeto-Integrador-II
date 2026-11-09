from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = 'edusinal.db'

def init_db():
    """Inicializa o banco de dados com as tabelas necessárias."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            tipo TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS glossario_libras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            termo_tecnico TEXT NOT NULL,
            categoria TEXT NOT NULL,
            descricao TEXT NOT NULL,
            sinal_url TEXT NOT NULL
        )
    ''')
    # Inserir dados padrão caso a tabela esteja vazia
    cursor.execute('SELECT COUNT(*) FROM glossario_libras')
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO glossario_libras (termo_tecnico, categoria, descricao, sinal_url) VALUES ('Hardware', 'Arquitetura', 'Componentes físicos do computador.', 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=400')")
        cursor.execute("INSERT INTO glossario_libras (termo_tecnico, categoria, descricao, sinal_url) VALUES ('Classe', 'POO', 'Estrutura que define atributos e métodos de objetos.', 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=400')")
        conn.commit()
    conn.close()

# Template HTML incorporado (Design moderno, limpo e acessível)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>EduSinal+ : Plataforma Inclusiva</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f7f6; color: #333; }
        header { background: #2c3e50; color: white; padding: 20px; text-align: center; }
        nav { display: flex; justify-content: center; background: #34495e; padding: 10px; }
        nav a { color: white; margin: 0 15px; text-decoration: none; font-weight: bold; }
        nav a:hover { text-decoration: underline; }
        .container { max-width: 900px; margin: 30px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        h2 { color: #2c3e50; border-bottom: 2px solid #ecf0f1; padding-bottom: 5px; }
        .card { background: #f9f9f9; border-left: 5px solid #3498db; padding: 15px; margin-bottom: 15px; border-radius: 4px; }
        .btn { background: #3498db; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; text-decoration: none; display: inline-block; }
        .btn:hover { background: #2980b9; }
        input, select { width: 100%; padding: 10px; margin: 8px 0 15px 0; display: inline-block; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    </style>
</head>
<body>
    <header>
        <h1>EduSinal+</h1>
        <p>Inclusão, Empreendedorismo e Computação Acessível em LIBRAS</p>
    </header>
    <nav>
        <a href="/">Início & Glossário</a>
        <a href="/matematica">Módulo Matemático</a>
        <a href="/cadastro">Cadastrar Usuário</a>
    </nav>
    <div class="container">
        {% if page == 'home' %}
            <h2>Glossário Técnico & Acessibilidade em LIBRAS</h2>
            <p>Conceitos fundamentais de arquitetura, banco de dados e POO traduzidos para LIBRAS.</p>
            {% for termo in termos %}
                <div class="card">
                    <h3>{{ termo[1] }} <span style="font-size: 0.8em; color: #7f8c8d;">({{ termo[2] }})</span></h3>
                    <p>{{ termo[3] }}</p>
                    <p><strong>Demonstração em LIBRAS:</strong></p>
                    <img src="{{ termo[4] }}" alt="Sinal em LIBRAS para {{ termo[1] }}" style="max-width: 100%; height: 150px; object-fit: cover; border-radius: 4px;">
                </div>
            {% endfor %}

        {% elif page == 'matematica' %}
            <h2>Módulo Matemático & Arquitetura de Computadores</h2>
            <p>Aplicação prática de algoritmo de conversão de bases numéricas (Decimal para Binário).</p>
            <form method="POST" action="/matematica">
                <label for="decimal">Digite um número decimal:</label>
                <input type="number" id="decimal" name="decimal" required min="0" value="{{ decimal_val if decimal_val is not none else '' }}">
                <button type="submit" class="btn">Converter para Binário</button>
            </form>
            {% if resultado is not none %}
                <div class="card" style="margin-top: 20px; border-color: #27ae60;">
                    <h3>Resultado da Conversão:</h3>
                    <p>O número decimal <strong>{{ decimal_val }}</strong> em binário (base da Arquitetura de Computadores) é: <strong>{{ resultado }}</strong></p>
                </div>
            {% endif %}

        {% elif page == 'cadastro' %}
            <h2>Cadastro de Novo Aluno / Membro da Comunidade</h2>
            <form method="POST" action="/cadastro">
                <label for="nome">Nome Completo:</label>
                <input type="text" id="nome" name="nome" required>
                
                <label for="email">E-mail:</label>
                <input type="email" id="email" name="email" required>
                
                <label for="tipo">Perfil:</label>
                <select id="tipo" name="tipo">
                    <option value="ALUNO">Aluno / Aprendiz</option>
                    <option value="PROFESSOR">Professor / Instrutor</option>
                </select>
                
                <button type="submit" class="btn">Cadastrar na Plataforma</button>
            </form>
            {% if mensagem %}
                <p style="color: green; font-weight: bold; margin-top: 15px;">{{ mensagem }}</p>
            {% endif %}
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, termo_tecnico, categoria, descricao, sinal_url FROM glossario_libras')
    termos = cursor.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, page='home', termos=termos)

@app.route('/matematica', methods=['GET', 'POST'])
def matematica():
    resultado = None
    decimal_val = None
    if request.method == 'POST':
        try:
            decimal_val = int(request.form['decimal'])
            # Algoritmo matemático básico aplicado à arquitetura/computação
            resultado = bin(decimal_val)[2:]
        except ValueError:
            resultado = "Valor inválido"
    return render_template_string(HTML_TEMPLATE, page='matematica', resultado=resultado, decimal_val=decimal_val)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    mensagem = None
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        tipo = request.form['tipo']
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO usuario (nome, email, tipo) VALUES (?, ?, ?)', (nome, email, tipo))
            conn.commit()
            conn.close()
            mensagem = "Usuário cadastrado com sucesso!"
        except sqlite3.IntegrityError:
            mensagem = "Erro: Este e-mail já está cadastrado."
    return render_template_string(HTML_TEMPLATE, page='cadastro', mensagem=mensagem)

if __name__ == '__main__':
    init_db()
    print("Iniciando servidor web EduSinal+ em http://127.0.0.1:5000")
    app.run(debug=True)