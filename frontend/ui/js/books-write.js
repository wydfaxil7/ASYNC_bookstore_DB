document.addEventListener("DOMContentLoaded", () => {
  if (!ensureAuthenticated()) {
    return;
  }

  const singleBookForm = document.getElementById("singleBookForm");
  const bulkBookForm = document.getElementById("bulkBookForm");
  const createdBooksGrid = document.getElementById("createdBooksGrid");
  const createStatus = document.getElementById("createStatus");
  const bulkBooksJson = document.getElementById("bulkBooksJson");

  (async () => {
    const user = await fetchCurrentUser();
    if (!user) {
      window.location.href = "/ui/login";
      return;
    }
    applyRoleVisibility(Boolean(user.is_admin));
    if (!user.is_admin) {
      showToast("Only admins can access write operations.", "error");
      window.location.href = "/ui/dashboard";
    }
  })();

  bulkBooksJson.value = JSON.stringify(
    {
      books: [
        {
          name: "Atomic Habits",
          author: "James Clear",
          genre: "Productivity",
          published_date: "2018-10-16",
          description: "A practical system for building good habits and breaking bad ones.",
        },
      ],
    },
    null,
    2,
  );

  const renderCreated = (books) => {
    createdBooksGrid.innerHTML = "";
    if (!books.length) {
      createdBooksGrid.appendChild(createEmptyState("Created books will appear here."));
      return;
    }
    books.forEach((book) => createdBooksGrid.appendChild(createBookCard(book)));
  };

  singleBookForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    createStatus.textContent = "Creating book...";

    const payload = {
      name: document.getElementById("bookName").value.trim(),
      author: document.getElementById("bookAuthor").value.trim(),
      genre: document.getElementById("bookGenre").value.trim() || null,
      published_date: document.getElementById("bookDate").value || null,
      description: document.getElementById("bookDescription").value.trim() || null,
    };

    try {
      const response = await apiRequest("/books", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      const createdBook = await response.json();
      if (!response.ok) {
        throw new Error(createdBook.detail || "Create failed (admin only)");
      }
      renderCreated([createdBook]);
      createStatus.textContent = "Created one book";
      showToast("Book created.", "success");
      singleBookForm.reset();
    } catch (error) {
      createStatus.textContent = "Create failed";
      showToast(error.message, "error");
    }
  });

  bulkBookForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    createStatus.textContent = "Creating bulk books...";

    let payload;
    try {
      payload = JSON.parse(bulkBooksJson.value);
    } catch (error) {
      showToast("Bulk JSON is invalid.", "error");
      createStatus.textContent = "Invalid bulk payload";
      return;
    }

    try {
      const response = await apiRequest("/books/bulk", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      const createdBooks = await response.json();
      if (!response.ok) {
        throw new Error(createdBooks.detail || "Bulk create failed");
      }
      renderCreated(Array.isArray(createdBooks) ? createdBooks : []);
      createStatus.textContent = `Created ${Array.isArray(createdBooks) ? createdBooks.length : 0} books`;
      showToast("Bulk books created.", "success");
    } catch (error) {
      createStatus.textContent = "Bulk create failed";
      showToast(error.message, "error");
    }
  });
});
