

Este projeto consiste em um chatbot para um restaurante, possuindo uma interface front-end (em React com Vite) e um back-end (em Python com Flask). O usuário pode selecionar o idioma, consultar o menu, realizar pedidos (delivery ou retirada no local) e efetuar reservas, tudo via uma interface de chat simples. Além disso, há a integração de lógica de negócio coerente com o fluxo esperado de um restaurante, bem como a possibilidade de integrar com serviços de mensagens (como o Twilio) para receber e enviar mensagens por SMS ou WhatsApp, que é a principal demanda do restaurante, além do chat widget para integrar no site, que já existe



## Estrutura do Projeto


- `backend/`: Contém o código do servidor Flask.
  - `chatbot_restaurante_api.py`: Arquivo principal do Flask, contendo rotas para menu, horários, reservas, pedidos, troca de idioma, etc.
- `frontend/`: Contém o código do aplicativo React (Vite).
  - `src/`: Código fonte do front-end.
    - `ChatWidget.jsx`: Componente principal do chat.
    - `Message.jsx`: Componente para exibir mensagens.
  - Outros arquivos de configuração do React/Vite e css.

## Pré-requisitos

- **Back-end:**
  - Python 3.11+ 
  - Pip (gerenciador de pacotes Python)
  - Flask e Flask-CORS instalados (`pip install flask flask-cors`)

- **Front-end:**
  - Node.js (recomendado Node.js 18)
  - NPM ou Yarn instalado


## Instalação do Back-end


1. Navegue até a pasta do projeto:

   cd backend


Crie e ative um ambiente virtual (opcional, mas recomendado):


python -m venv venv
Linux/Mac
source venv/bin/activate  

ou no Windows:
venv\Scripts\activate

Aqui criamos e ativamos um ambiente virtual.)

Instale as dependências:

pip install flask flask-cors 

Execute o servidor Flask:


python chatbot_restaurante_api.py`.py


O back-end agora estará acessível em: http://127.0.0.1:5000


## Instalação do Front-end

Navegue até a pasta do front-end:


cd front


Instale as dependências do projeto React (Vite):

npm install

Inicie o servidor de desenvolvimento do Vite:

npm run dev

O front-end agora estará acessível em: http://127.0.0.1:5173


## Uso

Abra o front-end no navegador (por padrão em http://127.0.0.1:5173).

O chatbot solicitará primeiro o idioma: digite pt para Português ou en para English.

Após definir o idioma, você poderá escolher opções:

menu: Exibe o cardápio.
delivery: Permite fazer um pedido para entrega, solicitando itens e endereço.
retirada (ou pickup): Permite fazer um pedido para retirada, solicitando itens.
reserva (ou reservation): Permite fazer uma reserva enviando data,hora,pessoas.
Interaja conforme o chatbot indicar, e observe as respostas retornadas.

