(function () {
  const ids = {
    filterForm: "filterForm",
    q: "q",
    genre: "genre",
    author: "author",
    loadBooksBtn: "loadBooksBtn",
    clearBooksBtn: "clearBooksBtn",
    aiSearchForm: "aiSearchForm",
    aiQuery: "aiQuery",
    createBookForm: "createBookForm",
    bookName: "bookName",
    bookAuthor: "bookAuthor",
    bookGenre: "bookGenre",
    bookDate: "bookDate",
    bookDescription: "bookDescription",
    summaryForm: "summaryForm",
    summaryId: "summaryId",
    summaryName: "summaryName",
    summaryOutput: "summaryOutput",
    bookGrid: "bookGrid",
    bookCount: "bookCount",
  };

  const el = Object.fromEntries(Object.entries(ids).map(([k, v]) => [k, document.getElementById(v)]));

  function bookCard(book) {
    const wrapper = document.createElement("article");
    wrapper.className = "book-card";
    wrapper.innerHTML = `
      <h3>${book.name}</h3>
      <p><strong>Author:</strong> ${book.author}</p>
      <p><strong>Genre:</strong> ${book.genre || "-"}</p>
      <p><strong>Published:</strong> ${book.published_date || "-"}</p>
      <p>${book.description || "No description"}</p>
      <button class="btn ghost danger" data-delete-id="${book.id}">Delete</button>
    `;

    wrapper.querySelector("[data-delete-id]").addEventListener("click", async () => {
      try {
        const res = await api(`/books/${book.id}`, { method: "DELETE" });
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || "Delete failed");
        }
        toast("Deleted");
        loadBooks();
      } catch (error) {
        toast(error.message, true);
      }
    });

    return wrapper;
  }

  function renderBooks(books) {
    el.bookGrid.innerHTML = "";
    el.bookCount.textContent = `${books.length} result${books.length === 1 ? "" : "s"}`;
    if (!books.length) {
      el.bookGrid.innerHTML = "<p class='muted'>No books found.</p>";
      return;
    }

    books.forEach((book) => el.bookGrid.appendChild(bookCard(book)));
  }

  async function loadBooks(params = new URLSearchParams({ limit: "18", offset: "0" })) {
    try {
      const res = await fetch(`/books?${params.toString()}`);
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Failed to fetch books");
      }
      renderBooks(data.data || []);
    } catch (error) {
      toast(error.message, true);
    }
  }

  el.filterForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const q = el.q.value.trim();
    const genre = el.genre.value.trim();
    const author = el.author.value.trim();

    if (q || genre) {
      const params = new URLSearchParams({ q, genre, limit: "20", offset: "0" });
      try {
        const res = await fetch(`/books/search?${params.toString()}`);
        const data = await res.json();
        if (!res.ok) {
          throw new Error(data.detail || "Search failed");
        }
        renderBooks(Array.isArray(data) ? data : []);
      } catch (error) {
        toast(error.message, true);
      }
      return;
    }

    const listParams = new URLSearchParams({ limit: "20", offset: "0" });
    if (author) listParams.set("author", author);
    if (genre) listParams.set("genre", genre);
    loadBooks(listParams);
  });

  el.loadBooksBtn.addEventListener("click", () => loadBooks());

  el.clearBooksBtn.addEventListener("click", () => {
    el.q.value = "";
    el.genre.value = "";
    el.author.value = "";
    loadBooks();
  });

  el.aiSearchForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const query = el.aiQuery.value.trim();
    if (!query) {
      toast("Enter a query for AI search", true);
      return;
    }

    try {
      const res = await fetch(`/books/ai-search?query=${encodeURIComponent(query)}&limit=20&offset=0`);
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || data.message || "AI search failed");
      }
      renderBooks(data.data || []);
    } catch (error) {
      toast(error.message, true);
    }
  });

  el.createBookForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const payload = {
        name: el.bookName.value.trim(),
        author: el.bookAuthor.value.trim(),
        genre: el.bookGenre.value.trim() || null,
        published_date: el.bookDate.value || null,
        description: el.bookDescription.value.trim() || null,
      };

      const res = await api("/books", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Create failed (admin only)");
      }

      toast("Book created");
      el.createBookForm.reset();
      loadBooks();
    } catch (error) {
      toast(error.message, true);
    }
  });

  el.summaryForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const id = el.summaryId.value.trim();
    const name = el.summaryName.value.trim();

    if (!id && !name) {
      toast("Provide id or name", true);
      return;
    }

    const params = new URLSearchParams();
    if (id) params.set("id", id);
    if (!id && name) params.set("name", name);

    try {
      const res = await fetch(`/books/summary/search?${params.toString()}`);
      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Summary request failed");
      }
      el.summaryOutput.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
      toast(error.message, true);
    }
  });

  loadBooks();
})();
