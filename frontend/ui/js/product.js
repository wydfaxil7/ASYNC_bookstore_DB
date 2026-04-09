(function () {
  if (!ensureAuthenticated()) return;

  const wrap = document.getElementById("productWrap");
  const bookId = Number(new URLSearchParams(window.location.search).get("id"));

  const coverUrl = (id) => `https://picsum.photos/seed/book-${id}/760/1000`;

  function stockNote(book) {
    const stock = Number(book.stock ?? 10);
    if (stock <= 0) return "Out of stock";
    return stock < 5 ? `Only ${stock} pieces left` : `Stock available: ${stock}`;
  }

  function renderBook(book, totalItems = 0) {
    wrap.innerHTML = "";

    const grid = createElement("div", "product-grid");

    const media = createElement("div", "product-media");
    const img = createElement("img", "product-image");
    img.src = coverUrl(book.id);
    img.alt = `${book.name} cover`;
    img.onerror = () => {
      img.src = "/static/ui/assets/bookstore-hero.svg";
    };
    media.appendChild(img);

    const detail = createElement("div", "product-detail");
    const kicker = createElement("p", "kicker", "BOOK DETAIL");
    const title = createElement("h1", "dash-title", book.name);
    const by = createElement("p", "muted", `by ${book.author}`);
    const meta = createElement("p", "product-meta", `Genre: ${book.genre || "Uncategorized"} · Published: ${formatDate(book.published_date)}`);
    const desc = createElement("p", "product-description", book.description || "No description available.");
    const price = createElement("p", "product-price", `$${Number(book.price || 0).toFixed(2)}`);

    const infoRow = createElement("div", "product-info-row");
    infoRow.appendChild(createElement("span", "badge", `Cart Items: ${totalItems}`));
    infoRow.appendChild(createElement("span", "badge", stockNote(book)));

    const actions = createElement("div", "product-actions");
    const getNow = createElement("button", "btn", "Get Now");
    getNow.type = "button";
    if (Number(book.stock ?? 10) <= 0) {
      getNow.disabled = true;
      getNow.textContent = "Out of stock";
    }
    getNow.addEventListener("click", async () => {
      if (window.openQuickAddModal) {
        await window.openQuickAddModal(book);
      }
    });

    const back = createElement("a", "btn ghost", "Back to Shop");
    back.href = "/ui/shop";

    actions.append(getNow, back);
    detail.append(kicker, title, by, meta, desc, price, infoRow, actions);
    grid.append(media, detail);
    wrap.appendChild(grid);
  }

  async function loadCartTotal() {
    const response = await apiRequest("/carts");
    const payload = await response.json();
    if (response.ok && window.refreshCartCount) {
      window.refreshCartCount(payload.total_items || 0);
    }
    return response.ok ? Number(payload.total_items || 0) : 0;
  }

  (async () => {
    if (!Number.isFinite(bookId) || bookId <= 0) {
      wrap.innerHTML = "";
      wrap.appendChild(createEmptyState("Invalid product id."));
      return;
    }

    try {
      const user = await fetchCurrentUser(true);
      if (!user) {
        window.location.href = "/ui/login";
        return;
      }

      const [bookRes, cartTotal] = await Promise.all([
        apiRequest(`/books/${bookId}`),
        loadCartTotal(),
      ]);
      const bookPayload = await bookRes.json();

      if (!bookRes.ok) {
        throw new Error(bookPayload.detail || "Book not found");
      }

      renderBook(bookPayload, cartTotal);
    } catch (error) {
      wrap.innerHTML = "";
      wrap.appendChild(createEmptyState(error.message || "Unable to load product"));
      showToast(error.message || "Unable to load product", "error");
    }
  })();
})();
