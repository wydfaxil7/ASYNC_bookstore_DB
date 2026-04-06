const STORE_KEY = "bookstore_access_token";

function getToken() {
  return localStorage.getItem(STORE_KEY) || "";
}

function setToken(token) {
  if (!token) {
    localStorage.removeItem(STORE_KEY);
    return;
  }
  localStorage.setItem(STORE_KEY, token);
}

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  const token = getToken();
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  return fetch(path, { ...options, headers });
}

function toast(message, isError = false) {
  const node = document.getElementById("toast");
  if (!node) return;
  node.textContent = message;
  node.style.borderColor = isError ? "rgba(240, 90, 116, 0.55)" : "rgba(34, 201, 192, 0.55)";
  node.classList.add("show");
  setTimeout(() => node.classList.remove("show"), 2200);
}

function ensureAuthenticated(redirectTo = "/ui/login") {
  if (!getToken()) {
    window.location.href = redirectTo;
    return false;
  }
  return true;
}
