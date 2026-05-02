(function () {
  if (!ensureAuthenticated()) return;

  const state = {
    allBooks: [],
    filteredBooks: [],
    selectedAuthor: "",
    selectedGenre: "",
    search: "",
  };

  const refs = {
    totalBooks: document.getElementById("totalBooks"),
    totalCartItems: document.getElementById("totalCartItems"),
    resultMeta: document.getElementById("resultMeta"),
    authorsList: document.getElementById("authorsList"),
    genresList: document.getElementById("genresList"),
    authorCount: document.getElementById("authorCount"),
    genreCount: document.getElementById("genreCount"),
    searchInput: document.getElementById("searchInput"),
    clearFiltersBtn: document.getElementById("clearFiltersBtn"),
    shopGrid: document.getElementById("shopGrid"),
  };

  const coverUrl = (book) => `https://picsum.photos/seed/book-${book.id}/560/760`;

  function normalizeKey(book) {
    return [book.name, book.author, book.genre]
      .map((value) => String(value || "").trim().toLowerCase())
      .join("|");
  }

  function dedupeBooks(list) {
    const seen = new Map();
    list.forEach((book) => {
      const key = normalizeKey(book);
      if (!seen.has(key)) {
        seen.set(key, book);
      }
    });
    return [...seen.values()];
  }

  async function loadBooks() {
    const limit = 100;
    let offset = 0;
    let total = 0;
    const all = [];

    do {
      const response = await apiRequest(`/books?limit=${limit}&offset=${offset}`);
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || "Failed to load books");
      }

      const data = Array.isArray(payload.data) ? payload.data : [];
      total = Number(payload.total || data.length);
      all.push(...data);
      offset += limit;
    } while (all.length < total);

    state.allBooks = dedupeBooks(all);
    state.filteredBooks = [...state.allBooks];
    refs.totalBooks.textContent = String(state.allBooks.length);
  }

  function buildSections() {
    const authorMap = new Map();
    const genreMap = new Map();

    state.allBooks.forEach((book) => {
      const author = (book.author || "Unknown").trim();
      const genre = (book.genre || "Uncategorized").trim();
      authorMap.set(author, (authorMap.get(author) || 0) + 1);
      genreMap.set(genre, (genreMap.get(genre) || 0) + 1);
    });

    const renderChips = (container, entries, selected, onClick) => {
      container.innerHTML = "";

      const allBtn = createElement("button", `chip ${!selected ? "active" : ""}`, "All");
      allBtn.type = "button";
      allBtn.addEventListener("click", () => onClick(""));
      container.appendChild(allBtn);

      entries
        .sort((a, b) => a[0].localeCompare(b[0]))
        .forEach(([name, count]) => {
          const btn = createElement("button", `chip ${selected === name ? "active" : ""}`, `${name} (${count})`);
          btn.type = "button";
          btn.addEventListener("click", () => onClick(name));
          container.appendChild(btn);
        });
    };

    refs.authorCount.textContent = String(authorMap.size);
    refs.genreCount.textContent = String(genreMap.size);

    renderChips(refs.authorsList, [...authorMap.entries()], state.selectedAuthor, (value) => {
      state.selectedAuthor = value;
      applyFilters();
      buildSections();
    });

    renderChips(refs.genresList, [...genreMap.entries()], state.selectedGenre, (value) => {
      state.selectedGenre = value;
      applyFilters();
      buildSections();
    });
  }

  function stockNote(book) {
    const stock = Number(book.stock ?? 10);
    if (stock <= 0) return "Out of stock";
    return stock < 5 ? `Only ${stock} pieces left` : "";
  }

  function renderBooks() {
    refs.shopGrid.innerHTML = "";

    if (!state.filteredBooks.length) {
      refs.shopGrid.appendChild(createEmptyState("No books match your filters."));
      refs.resultMeta.textContent = "0 items";
      return;
    }

    state.filteredBooks.forEach((book) => {
      const card = createElement("article", "shop-card");

      const imageWrap = createElement("a", "shop-card-image-wrap");
      imageWrap.href = `/ui/product?id=${book.id}`;
      const stock = stockNote(book);
      if (stock) {
        imageWrap.appendChild(createElement("span", "stock-corner", stock));
      }

      const image = createElement("img", "shop-card-image");
      image.src = coverUrl(book);
      image.alt = `${book.name} cover`;
      image.loading = "lazy";
      image.onerror = () => {
        image.src = "/static/ui/assets/bookstore-hero.svg";
      };
      imageWrap.appendChild(image);

      const body = createElement("div", "shop-card-body");
      const title = createElement("a", "shop-card-title", book.name);
      title.href = `/ui/product?id=${book.id}`;
      const author = createElement("p", "shop-card-author", `by ${book.author}`);
      const genre = createElement("p", "shop-card-genre", book.genre || "Uncategorized");
      const price = createElement("p", "shop-card-price", `$${Number(book.price || 0).toFixed(2)}`);

      const actions = createElement("div", "shop-card-actions");
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

      const viewBtn = createElement("a", "btn ghost", "View");
      viewBtn.href = `/ui/product?id=${book.id}`;

      actions.append(getNow, viewBtn);
      body.append(title, author, genre, price, actions);
      card.append(imageWrap, body);
      refs.shopGrid.appendChild(card);
    });

    refs.resultMeta.textContent = `${state.filteredBooks.length} items`;
  }

  function applyFilters() {
    const q = state.search.toLowerCase();
    state.filteredBooks = state.allBooks.filter((book) => {
      const author = (book.author || "").trim();
      const genre = (book.genre || "").trim();
      const textMatch = !q
        || (book.name || "").toLowerCase().includes(q)
        || author.toLowerCase().includes(q)
        || genre.toLowerCase().includes(q);
      const authorMatch = !state.selectedAuthor || author === state.selectedAuthor;
      const genreMatch = !state.selectedGenre || genre === state.selectedGenre;
      return textMatch && authorMatch && genreMatch;
    });
    renderBooks();
  }

  async function loadCartTotal() {
    const response = await apiRequest("/carts");
    const payload = await response.json();
    if (response.ok && refs.totalCartItems) {
      refs.totalCartItems.textContent = String(payload.total_items || 0);
    }
    if (window.refreshCartCount) {
      window.refreshCartCount(payload.total_items || 0);
    }
  }

  function wireEvents() {
    refs.searchInput?.addEventListener("input", (e) => {
      state.search = e.target.value || "";
      applyFilters();
    });

    refs.clearFiltersBtn?.addEventListener("click", () => {
      state.search = "";
      state.selectedAuthor = "";
      state.selectedGenre = "";
      refs.searchInput.value = "";
      applyFilters();
      buildSections();
    });
  }

  (async () => {
    try {
      const user = await fetchCurrentUser(true);
      if (!user) {
        window.location.href = "/ui/login";
        return;
      }

      await loadBooks();
      await loadCartTotal();
      buildSections();
      wireEvents();
      renderBooks();
    } catch (error) {
      refs.shopGrid.innerHTML = "";
      refs.shopGrid.appendChild(createEmptyState(error.message || "Unable to load shop"));
      showToast(error.message || "Unable to load shop", "error");
    }
  })();
})();
