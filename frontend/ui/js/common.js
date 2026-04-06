const STORE_KEY = "bookstore_access_token";
const USER_KEY = "bookstore_user_profile";

function createElement(tagName, className = "", textContent = "") {
  const node = document.createElement(tagName);
  if (className) node.className = className;
  if (textContent) node.textContent = textContent;
  return node;
}

function getToken() {
  return localStorage.getItem(STORE_KEY) || "";
}

function setToken(token) {
  if (!token) {
    localStorage.removeItem(STORE_KEY);
    localStorage.removeItem(USER_KEY);
    return;
  }
  localStorage.setItem(STORE_KEY, token);
}

function setCurrentUser(user) {
  if (!user) {
    localStorage.removeItem(USER_KEY);
    return;
  }
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

function getCurrentUser() {
  const raw = localStorage.getItem(USER_KEY);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch (_error) {
    localStorage.removeItem(USER_KEY);
    return null;
  }
}

function clearSession() {
  localStorage.removeItem(STORE_KEY);
  localStorage.removeItem(USER_KEY);
}

async function fetchCurrentUser(force = false) {
  if (!getToken()) {
    return null;
  }

  const cached = getCurrentUser();
  if (cached && !force) {
    return cached;
  }

  try {
    const response = await apiRequest("/auth/me");
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Failed to load current user");
    }
    setCurrentUser(payload);
    return payload;
  } catch (_error) {
    clearSession();
    return null;
  }
}

function applyRoleVisibility(isAdmin) {
  document.querySelectorAll(".admin-only").forEach((node) => {
    node.style.display = isAdmin ? "" : "none";
  });
  document.querySelectorAll(".customer-only").forEach((node) => {
    node.style.display = isAdmin ? "none" : "";
  });
}

function wireLogoutLinks() {
  document.querySelectorAll(".logout-link").forEach((node) => {
    if (node.dataset.logoutWired === "1") return;
    node.dataset.logoutWired = "1";
    node.addEventListener("click", (event) => {
      event.preventDefault();
      clearSession();
      toast("Logged out");
      setTimeout(() => {
        window.location.href = "/ui/login";
      }, 220);
    });
  });
}

document.addEventListener("DOMContentLoaded", wireLogoutLinks);

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  const token = getToken();
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  return fetch(path, { ...options, headers });
}

function apiRequest(path, options = {}) {
  return api(path, options);
}

function toast(message, isError = false) {
  const node = document.getElementById("toast");
  if (!node) return;
  node.textContent = message;
  node.style.borderColor = isError ? "rgba(240, 90, 116, 0.55)" : "rgba(34, 201, 192, 0.55)";
  node.classList.add("show");
  setTimeout(() => node.classList.remove("show"), 2200);
}

function showToast(message, type = "success") {
  toast(message, type === "error");
}

function ensureAuthenticated(redirectTo = "/ui/login") {
  if (!getToken()) {
    window.location.href = redirectTo;
    return false;
  }
  return true;
}

function formatDate(value) {
  if (!value) return "—";
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return value;
  return parsed.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

function renderBookCard(book, actions = []) {
  const card = createElement("article", "book-card");

  const main = createElement("div", "book-list-main");
  const header = createElement("div", "book-card-head");
  const titleWrap = createElement("div", "book-title-wrap");
  titleWrap.appendChild(createElement("h3", "book-title", book.name));
  titleWrap.appendChild(createElement("p", "book-subtitle", `by ${book.author}`));

  const idPill = createElement("span", "book-id-pill", `#${book.id}`);
  header.append(titleWrap, idPill);

  const meta = createElement("div", "book-meta-grid");
  const fields = [
    ["Genre", book.genre || "—"],
    ["Published", formatDate(book.published_date)],
  ];
  fields.forEach(([label, value]) => {
    const item = createElement("div", "book-meta-item");
    item.appendChild(createElement("span", "book-meta-label", label));
    item.appendChild(createElement("strong", "book-meta-value", value));
    meta.appendChild(item);
  });

  const description = createElement("p", "book-description", book.description || "No description available.");
  const actionsRow = createElement("div", "card-actions");

  actions.forEach((action) => {
    const button = createElement("button", `btn ${action.className || "ghost"}`, action.label);
    button.type = "button";
    button.addEventListener("click", () => action.onClick?.(book, card));
    actionsRow.appendChild(button);
  });

  main.append(header, meta, description);
  card.appendChild(main);
  if (actions.length) {
    const side = createElement("div", "book-list-side");
    side.appendChild(actionsRow);
    card.appendChild(side);
  }
  return card;
}

function createBookCard(book, actions = []) {
  return renderBookCard(book, actions);
}

function renderBookGrid(container, books, emptyMessage = "No books found.", actions = []) {
  container.innerHTML = "";
  if (!books || !books.length) {
    const empty = createElement("div", "empty-state", emptyMessage);
    container.appendChild(empty);
    return;
  }

  books.forEach((book) => container.appendChild(renderBookCard(book, actions)));
}

function renderPagination(container, total, limit, offset, onPageChange) {
  if (!container) return;
  container.innerHTML = "";

  const safeLimit = Math.max(1, Number(limit || 20));
  const safeTotal = Math.max(0, Number(total || 0));
  const totalPages = Math.max(1, Math.ceil(safeTotal / safeLimit));

  if (safeTotal <= safeLimit) {
    return;
  }

  const currentPage = Math.floor(Number(offset || 0) / safeLimit) + 1;
  const wrap = createElement("div", "pagination");

  const addButton = (label, page, disabled = false, active = false) => {
    const btn = createElement("button", `page-btn${active ? " active" : ""}`, String(label));
    btn.type = "button";
    btn.disabled = disabled;
    if (!disabled) {
      btn.addEventListener("click", () => onPageChange(page));
    }
    wrap.appendChild(btn);
  };

  addButton("Prev", Math.max(1, currentPage - 1), currentPage === 1);

  let start = Math.max(1, currentPage - 3);
  let end = Math.min(totalPages, start + 6);
  if (end - start < 6) {
    start = Math.max(1, end - 6);
  }

  if (start > 1) {
    addButton(1, 1, false, currentPage === 1);
    if (start > 2) {
      wrap.appendChild(createElement("span", "page-gap", "..."));
    }
  }

  for (let page = start; page <= end; page += 1) {
    addButton(page, page, false, page === currentPage);
  }

  if (end < totalPages) {
    if (end < totalPages - 1) {
      wrap.appendChild(createElement("span", "page-gap", "..."));
    }
    addButton(totalPages, totalPages, false, currentPage === totalPages);
  }

  addButton("Next", Math.min(totalPages, currentPage + 1), currentPage === totalPages);
  container.appendChild(wrap);
}

function createEmptyState(message) {
  return createElement("div", "empty-state", message);
}

function renderBookDetail(container, book, heading = "Book Details") {
  container.innerHTML = "";
  if (!book) {
    container.appendChild(createElement("div", "empty-state", "Search for a book ID to see full details."));
    return;
  }

  const wrap = createElement("article", "detail-card");
  const top = createElement("div", "detail-card-top");
  const title = createElement("div");
  title.appendChild(createElement("p", "kicker", heading.toUpperCase()));
  title.appendChild(createElement("h3", "detail-title", book.name));
  title.appendChild(createElement("p", "detail-author", `by ${book.author}`));

  const cover = createElement("div", "detail-cover");
  cover.textContent = book.genre ? book.genre.slice(0, 2).toUpperCase() : "BK";

  top.append(title, cover);

  const info = createElement("div", "detail-info-grid");
  [
    ["Book ID", `#${book.id}`],
    ["Genre", book.genre || "—"],
    ["Published", formatDate(book.published_date)],
  ].forEach(([label, value]) => {
    const item = createElement("div", "detail-info-item");
    item.appendChild(createElement("span", "book-meta-label", label));
    item.appendChild(createElement("strong", "book-meta-value", value));
    info.appendChild(item);
  });

  wrap.append(top, info, createElement("p", "detail-description", book.description || "No description available."));
  container.appendChild(wrap);
}

function renderResponseNote(container, title, description) {
  container.innerHTML = "";
  container.appendChild(createNoteCard(title, description));
}

function createNoteCard(title, description, subtitle = "") {
  const box = createElement("article", "note-card");
  box.appendChild(createElement("p", "kicker", title.toUpperCase()));
  box.appendChild(createElement("h3", "note-title", description));
  if (subtitle) {
    box.appendChild(createElement("p", "muted", subtitle));
  }
  return box;
}

function renderSummaryPanel(container, payload) {
  container.innerHTML = "";
  const panel = createElement("article", "detail-card");
  const title = createElement("p", "kicker", "AI SUMMARY");
  const heading = createElement("h3", "detail-title", payload.name || "Summary");
  const meta = createElement("div", "detail-info-grid");

  [
    ["Book ID", `#${payload.book_id ?? payload.id ?? "—"}`],
    ["Author", payload.author || "—"],
  ].forEach(([label, value]) => {
    const item = createElement("div", "detail-info-item");
    item.appendChild(createElement("span", "book-meta-label", label));
    item.appendChild(createElement("strong", "book-meta-value", value));
    meta.appendChild(item);
  });

  const summary = createElement("p", "detail-description", payload.summary || payload.message || "No summary returned.");
  panel.append(title, heading, meta, summary);
  container.appendChild(panel);
}

function createSummaryPanel(payload) {
  const container = createElement("div");
  renderSummaryPanel(container, payload);
  return container.firstElementChild;
}
