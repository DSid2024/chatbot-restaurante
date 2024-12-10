// 1) Ao carregar: pedir idioma
// 2) Usuário escolhe idioma: Setar idioma no backend e seguir para mainMenu
// 3) Em mainMenu: Usuário escolhe entre "menu", "delivery", "pickup" (retirada), "reservation" (reserva)
// 4) Para "menu": Mostrar cardápio. Depois voltar ao mainMenu
// 5) Para "reservation": Solicitar data,hora,pessoas. Depois confirmar e voltar ao mainMenu
// 6) Para "delivery" e "pickup": Solicitar itens. Confirmar pedido. Se delivery pedir endereço. Depois voltar ao mainMenu

import React, { useState, useEffect } from "react";
import Message from "./Message";
import "./ChatWidget.css";

const ChatWidget = () => {
  // Array de mensagens do chat
  const [messages, setMessages] = useState([]);
  // Armazena o texto digitado pelo usuário
  const [input, setInput] = useState("");
  // Estado do fluxo do chatbot, começando pelo idioma
  const [stage, setStage] = useState("language");
  // Idioma padrão
  const [language, setLanguage] = useState("pt");
  
  // Variáveis auxiliares para controlar pedidos e reservas
  // Por exemplo, ao escolher delivery/pickup, guardaremos itens do pedido
  const [pendingOrderType, setPendingOrderType] = useState(null);  // 'delivery' ou 'pickup'
  const [pendingItems, setPendingItems] = useState([]); // Armazenar itens temporariamente
  const [awaitingAddress, setAwaitingAddress] = useState(false); // Espera endereço no caso de delivery
  
  // Ao montar o componente, enviar a mensagem inicial pedindo idioma
  useEffect(() => {
    // Mensagem inicial
    addMessage(
      "Bem-vindo ao Chatbot Restaurante! Digite 'pt' para Português ou 'en' para English.",
      "bot"
    );
  }, []);

  // Função para adicionar mensagem no array de mensagens
  const addMessage = (content, sender) => {
    setMessages((prev) => [...prev, { content, sender }]);
  };

  // Função principal ao enviar uma mensagem pelo usuário
  const sendMessage = async () => {
    // Se o usuário não digitou nada, não faz nada
    if (!input.trim()) return;

    // Adiciona a mensagem do usuário ao chat
    addMessage(input, "user");

    // Armazena o que o usuário digitou
    const userText = input.trim().toLowerCase();

    try {
      // Dependendo do estágio atual, tratamos a lógica diferente
      let response;
      switch (stage) {
        case "language":
          // Etapa de seleção de idioma
          response = await handleLanguageSelection(userText);
          break;
        case "mainMenu":
          // Etapa de menu principal: usuário escolhe entre menu, delivery, pickup, reservation
          response = await handleMainMenu(userText);
          break;
        case "seeMenu":
          // Após exibir o menu, voltamos ao mainMenu
          response = await returnToMainMenu();
          break;
        case "reservation":
          // Usuário deve enviar data,hora,pessoas
          response = await handleReservation(input);
          break;
        case "delivery":
        case "pickup":
          // Nessas etapas, primeiro o usuário envia itens. 
          // Caso delivery e já tenha itens, pede endereço depois.
          if (awaitingAddress && stage === "delivery") {
            // Se estamos aguardando endereço do delivery:
            response = await handleDeliveryAddress(input);
          } else {
            // Caso contrário, estamos aguardando itens
            response = await handleOrderItems(input);
          }
          break;
        default:
          // Caso não entenda a etapa, mensagem genérica
          response = getLocalizedMessage(
            "Desculpe, não entendi sua mensagem.",
            "Sorry, I didn't understand your message."
          );
      }

      // Se obtivemos uma resposta do "bot", enviamos ao chat
      if (response) addMessage(response, "bot");
    } catch (error) {
      console.error(error);
      addMessage(
        getLocalizedMessage(
          "Erro ao se comunicar com a API.",
          "Error communicating with the API."
        ),
        "bot"
      );
    }

    // Limpa o campo de input
    setInput("");
  };

  // Função para obter mensagem no idioma selecionado
  const getLocalizedMessage = (ptMessage, enMessage) => {
    return language === "pt" ? ptMessage : enMessage;
  };

  // Lida com seleção de idioma
  const handleLanguageSelection = async (lang) => {
    // Verifica se idioma é válido
    if (!["pt", "en"].includes(lang)) {
      return getLocalizedMessage(
        "Idioma inválido. Digite 'pt' para Português ou 'en' para English.",
        "Invalid language. Type 'pt' for Portuguese or 'en' for English."
      );
    }

    setLanguage(lang); // Ajusta idioma localmente

    // Faz requisição ao backend para trocar o idioma do back-end
    const response = await fetch("http://127.0.0.1:5000/idioma", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ idioma: lang }),
    });

    if (!response.ok) throw new Error("Erro na API de idioma.");
    
    // Após selecionar idioma, vai para o menu principal
    setStage("mainMenu");

    return getLocalizedMessage(
      "Idioma alterado para Português. Escolha uma opção: 'menu', 'delivery', 'retirada' ou 'reserva'.",
      "Language switched to English. Choose an option: 'menu', 'delivery', 'pickup', or 'reservation'."
    );
  };

  // Exibe as opções principais
  const handleMainMenu = async (userInput) => {
    // Usuário deve escolher entre menu, delivery, retirada(pickup), reserva(reservation)
    if (userInput === "menu") {
      // Usuário quer ver o menu
      setStage("seeMenu");
      return await showMenu();
    } else if (userInput === "delivery") {
      // Usuário quer fazer um pedido delivery
      setPendingOrderType("delivery");
      setStage("delivery");
      return getLocalizedMessage(
        "Envie os códigos dos itens do pedido separados por vírgula (Ex: 1,2,3).",
        "Send the item codes separated by commas (Ex: 1,2,3)."
      );
    } else if (userInput === "retirada" || userInput === "pickup") {
      // Usuário quer fazer um pedido para retirada local
      setPendingOrderType("pickup");
      setStage("pickup");
      return getLocalizedMessage(
        "Envie os códigos dos itens do pedido separados por vírgula (Ex: 1,2,3).",
        "Send the item codes separated by commas (Ex: 1,2,3)."
      );
    } else if (userInput === "reserva" || userInput === "reservation") {
      // Usuário quer fazer uma reserva
      setStage("reservation");
      return getLocalizedMessage(
        "Envie no formato: data,hora,pessoas (Ex: 10/12/2024,20:00,4)",
        "Send in the format: date,time,people (Example: 10/12/2024,20:00,4)"
      );
    } else {
      // Opção inválida
      return getLocalizedMessage(
        "Opção inválida. Escolha: 'menu', 'delivery', 'retirada', ou 'reserva'.",
        "Invalid option. Choose: 'menu', 'delivery', 'pickup', or 'reservation'."
      );
    }
  };

  // Mostra o menu obtido do backend
  const showMenu = async () => {
    // Requisição ao backend para obter menu
    const menuData = await fetchBackend("/menu");
    // Apresenta o menu ao usuário
    return getLocalizedMessage(
      "Aqui está o cardápio:\n" + menuData + "\n\nDigite qualquer coisa para voltar ao menu principal.",
      "Here is the menu:\n" + menuData + "\n\nType anything to return to the main menu."
    );
  };

  // Ao pressionar algo após ver menu, retorna para o menu principal
  const returnToMainMenu = async () => {
    setStage("mainMenu");
    return getLocalizedMessage(
      "Escolha uma opção: 'menu', 'delivery', 'retirada', ou 'reserva'.",
      "Choose an option: 'menu', 'delivery', 'pickup', or 'reservation'."
    );
  };

  // Faz requisição ao backend
  const fetchBackend = async (endpoint) => {
    const response = await fetch(`http://127.0.0.1:5000${endpoint}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) throw new Error("Erro na API.");
    const data = await response.json();

    // Se data for um array, formatamos; caso contrário, exibimos JSON
    if (Array.isArray(data)) {
      // Retorna string formatada
      return data.map((item) => `${item.nome} - R$ ${item.preço.toFixed(2)}`).join("\n");
    }
    return JSON.stringify(data, null, 2);
  };

  // Lidar com reservas
  const handleReservation = async (message) => {
    // Espera formato: data,hora,pessoas
    const parts = message.split(",");
    if (parts.length !== 3) {
      return getLocalizedMessage(
        "Formato inválido. Exemplo: 10/12/2024,20:00,4",
        "Invalid format. Example: 10/12/2024,20:00,4"
      );
    }

    const [data, hora, pessoas] = parts.map((item) => item.trim());
    const response = await fetch("http://127.0.0.1:5000/reservas", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ data, hora, pessoas }),
    });

    if (!response.ok) throw new Error("Erro na API de reservas.");
    const result = await response.json();
    // Depois de concluir a reserva, volta ao menu principal
    setStage("mainMenu");
    return getLocalizedMessage(
      `Reserva confirmada: ${result.reserva.data}, ${result.reserva.hora}, ${result.reserva.pessoas} pessoas. Agora escolha outra opção: 'menu', 'delivery', 'retirada', ou 'reserva'.`,
      `Reservation confirmed: ${result.reserva.data}, ${result.reserva.hora}, ${result.reserva.pessoas} people. Now choose another option: 'menu', 'delivery', 'pickup', or 'reservation'.`
    );
  };

  // Lidar com pedido (itens) para delivery ou pickup
  const handleOrderItems = async (message) => {
    // O usuário envia algo tipo "1,2,3"
    const parts = message.split(",").map((p) => p.trim());
    if (!parts.length) {
      return getLocalizedMessage(
        "Envie ao menos um código de item.",
        "Send at least one item code."
      );
    }

    // Guarda itens no estado local
    setPendingItems(parts);

    // Se for delivery, após itens, perguntar endereço
    if (pendingOrderType === "delivery") {
      setAwaitingAddress(true);
      return getLocalizedMessage(
        "Agora envie o endereço para entrega.",
        "Now send the delivery address."
      );
    } else {
      // Se for pickup, já registra pedido
      return await confirmOrder(null);
    }
  };

  // Lidar com endereço no delivery
  const handleDeliveryAddress = async (address) => {
    // Agora temos itens e endereço, vamos fazer o pedido ao backend
    setAwaitingAddress(false);
    return await confirmOrder(address);
  };

  // Confirmar pedido no backend
  const confirmOrder = async (address) => {
    // Monta corpo da requisição
    const body = {
      tipo: pendingOrderType === "delivery" ? "delivery" : "local",
      itens: pendingItems.map((code) => parseInt(code, 10))
    };

    // Se delivery, precisa do endereço
    if (pendingOrderType === "delivery" && address) {
      body.endereco = address;
    }

    const response = await fetch("http://127.0.0.1:5000/pedido", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) throw new Error("Erro ao fazer pedido.");

    const result = await response.json();

    // Depois de confirmar o pedido, limpar variáveis e voltar ao mainMenu
    setPendingOrderType(null);
    setPendingItems([]);
    setStage("mainMenu");

    return getLocalizedMessage(
      `${result.message} Total: R$ ${result.total.toFixed(2)}. Escolha outra opção: 'menu', 'delivery', 'retirada', ou 'reserva'.`,
      `${result.message} Total: $${result.total.toFixed(2)}. Choose another option: 'menu', 'delivery', 'pickup', or 'reservation'.`
    );
  };

  return (
    <div className="chat-widget">
      {/* Cabeçalho do chat */}
      <div className="chat-header">Chatbot Restaurante</div>
      {/* Área das mensagens */}
      <div className="chat-messages">
        {messages.map((msg, index) => (
          // Componente Message renderiza cada mensagem
          <Message key={index} content={msg.content} sender={msg.sender} />
        ))}
      </div>
      {/* Campo de input e botão de enviar */}
      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={getLocalizedMessage("Digite sua mensagem...", "Type your message...")}
        />
        <button onClick={sendMessage}>
          {getLocalizedMessage("Enviar", "Send")}
        </button>
      </div>
    </div>
  );
};

export default ChatWidget;