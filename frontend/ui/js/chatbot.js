(function () {
  if (!ensureAuthenticated()) {
    return;
  }

  const form = document.getElementById("chatForm");
  const input = document.getElementById("chatInput");
  const sendBtn = document.getElementById("sendBtn");
  const chatFeed = document.getElementById("chatFeed");
  const clearBtn = document.getElementById("clearChatBtn");
  const historyLimit = document.getElementById("historyLimit");
  const quickRow = document.getElementById("quickRow");

  const state = {
    sending: false,
  };

  const createBubble = (type, text, meta = "") => {
    const wrap = document.createElement("article");
    wrap.className = `chat-bubble ${type}`;

    const role = document.createElement("p");
    role.className = "chat-role";
    role.textContent = type === "user" ? "You" : "BookGPT";

    const body = document.createElement("p");
    body.className = "chat-text";
    body.textContent = text;

    wrap.append(role, body);

    if (meta) {
      const note = document.createElement("p");
      note.className = "chat-meta";
      note.textContent = meta;
      wrap.appendChild(note);
    }

    return wrap;
  };

  const scrollBottom = () => {
    chatFeed.scrollTop = chatFeed.scrollHeight;
  };

  const setSending = (value) => {
    state.sending = value;
    sendBtn.disabled = value;
    sendBtn.textContent = value ? "Sending..." : "Send";
  };

  const addTyping = () => {
    const typing = document.createElement("article");
    typing.className = "chat-bubble bot typing";
    typing.id = "typingBubble";
    typing.innerHTML = '<p class="chat-role">BookGPT</p><p class="chat-text">Thinking...</p>';
    chatFeed.appendChild(typing);
    scrollBottom();
  };

  const removeTyping = () => {
    const typing = document.getElementById("typingBubble");
    if (typing) typing.remove();
  };

  const clearFeed = () => {
    chatFeed.innerHTML = "";
    chatFeed.appendChild(
      createBubble(
        "bot",
        "Hi, I am BookGPT. Ask me about books, recommendations, genres, and authors.",
        "Authenticated chat. Replies use your current session context."
      )
    );
  };

  const sendMessage = async (message) => {
    const text = (message || "").trim();
    if (!text || state.sending) {
      return;
    }

    chatFeed.appendChild(createBubble("user", text));
    scrollBottom();
    setSending(true);
    addTyping();

    try {
      const response = await apiRequest("/chat", {
        method: "POST",
        body: JSON.stringify({
          message: text,
          history_limit: Number(historyLimit.value || 10),
        }),
      });

      const payload = await response.json();
      removeTyping();

      if (!response.ok) {
        if (response.status === 401 || response.status === 403) {
          clearSession();
          showToast("Session expired. Login again.", "error");
          setTimeout(() => {
            window.location.href = "/ui/login";
          }, 260);
          return;
        }
        throw new Error(payload.detail || "BookGPT request failed.");
      }

      const meta = Array.isArray(payload.context_used)
        ? `Used ${payload.context_used.length} context messages`
        : "No context metadata";

      chatFeed.appendChild(createBubble("bot", payload.reply || "No response generated.", meta));
      scrollBottom();
    } catch (error) {
      removeTyping();
      chatFeed.appendChild(createBubble("bot", "I could not process that request right now."));
      showToast(error.message || "Request failed", "error");
      scrollBottom();
    } finally {
      setSending(false);
    }
  };

  form?.addEventListener("submit", async (event) => {
    event.preventDefault();
    const value = input.value;
    input.value = "";
    await sendMessage(value);
    input.focus();
  });

  clearBtn?.addEventListener("click", () => {
    clearFeed();
    showToast("Chat screen cleared.");
  });

  quickRow?.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLButtonElement)) {
      return;
    }
    const prompt = target.dataset.prompt || "";
    input.value = prompt;
    input.focus();
  });

  (async () => {
    const user = await fetchCurrentUser(true);
    if (!user) {
      window.location.href = "/ui/login";
      return;
    }
    applyRoleVisibility(Boolean(user.is_admin));
    clearFeed();
  })();
})();
