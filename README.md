# Projeto SD Motos

Bem-vindo ao repositório do projeto SD Motos, uma aplicação web completa para uma concessionária de motocicletas. O projeto foi desenvolvido como parte de um aprendizado prático em desenvolvimento web full-stack, utilizando o framework Python Flask.

A aplicação inclui um site público para a visualização das motos e um painel de administração seguro para o gerenciamento do inventário.

## Funcionalidades

- **Site Público de Página Única:** Uma homepage interativa com rolagem suave entre as seções: Início, Localização, Contato e Sobre Nós.
- **Funcionalidade de Busca:** Filtre as motos por marca, modelo e ano para encontrar exatamente o que o cliente procura.
- **Painel de Administração Seguro:** Acesso restrito por login para o gerente da loja.
- **Gestão Completa (CRUD):**
    - **C**riar novas motos com fotos e detalhes.
    - **L**er e visualizar o inventário completo.
    - **A**tualizar informações de motos existentes.
    - **D**eletar motos e seus arquivos de imagem do servidor, evitando sobrecarga.
- **Integração com WhatsApp:** Links diretos nos cards das motos com uma mensagem pré-preenchida para facilitar o contato.

## Tecnologias Utilizadas

- **Backend:**
    - Python
    - Flask
    - Flask-SQLAlchemy (para o banco de dados SQLite)
    - Flask-Login (para autenticação)
- **Frontend:**
    - HTML5
    - CSS3 (com Grid e Flexbox para layouts responsivos)
    - JavaScript (para interatividade e rolagem suave)
- **Ferramentas:**
    - Git & GitHub (para controle de versão)
