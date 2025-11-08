document.addEventListener("DOMContentLoaded", () => {
  const chatbot = document.getElementById("chatbot-container");
  const openBtn = document.getElementById("open-chatbot");
  const sendBtn = document.getElementById("chatbot-send");
  const input = document.getElementById("chatbot-input");
  const body = document.getElementById("chatbot-body");

  // Abre e fecha o chat
  openBtn.addEventListener("click", () => {
    const isOpen = chatbot.style.display === "flex";
    chatbot.style.display = isOpen ? "none" : "flex";
    openBtn.style.display = isOpen ? "block" : "none";
  });

  async function enviarMensagem() {
    const mensagem = input.value.trim();
    if (!mensagem) return;

    body.innerHTML += `<div style="margin-bottom:8px;"><b>Você:</b> ${mensagem}</div>`;
    input.value = "";
    body.scrollTop = body.scrollHeight;

    try {
      const response = await fetch("/chat/chatbot/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json; charset=utf-8",
          "Accept": "application/json"
        },
        body: JSON.stringify({ mensagem }),
      });

      const data = await response.json();
      body.innerHTML += `<div style="margin-bottom:8px;"><b>Bot:</b> ${data.resposta}</div>`;
      body.scrollTop = body.scrollHeight;
    } catch (error) {
      console.error("Erro no chatbot:", error);
      body.innerHTML += `<div style="color:red;"><b>Erro:</b> Não foi possível obter resposta.</div>`;
    }
  }

  sendBtn.addEventListener("click", enviarMensagem);
  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") enviarMensagem();
  });
});
