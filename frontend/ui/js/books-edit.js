document.addEventListener("DOMContentLoaded", () => {
  if (!ensureAuthenticated()) {
    return;
  }

  const loadBookForm = document.getElementById("loadBookForm");
  const updateBookForm = document.getElementById("updateBookForm");
  const deleteBookBtn = document.getElementById("deleteBookBtn");

  const targetBookId = document.getElementById("targetBookId");
  const editName = document.getElementById("editName");
  const editAuthor = document.getElementById("editAuthor");
  const editGenre = document.getElementById("editGenre");
  const editPublishedDate = document.getElementById("editPublishedDate");
  const editDescription = document.getElementById("editDescription");
  const selectedBookPreview = document.getElementById("selectedBookPreview");

  let loadedBook = null;

  const handleAuthFailure = (status) => {
    if (status === 401 || status === 403) {
      clearSession();
      showToast("Session expired. Please login again.", "error");
      setTimeout(() => {
        window.location.href = "/ui/login";
      }, 250);
      return true;
    }
    return false;
  };

  const fillForm = (book) => {
    targetBookId.value = book.id || "";
    editName.value = book.name || "";
    editAuthor.value = book.author || "";
    editGenre.value = book.genre || "";
    editPublishedDate.value = book.published_date || "";
    editDescription.value = book.description || "";
  };

  const showPreview = (book) => {
    selectedBookPreview.innerHTML = "";
    if (!book) {
      selectedBookPreview.appendChild(createEmptyState("No book loaded yet."));
      return;
    }
    selectedBookPreview.appendChild(createBookCard(book));
  };

  (async () => {
    const user = await fetchCurrentUser(true);
    if (!user) {
      window.location.href = "/ui/login";
      return;
    }
    if (!user.is_admin) {
      showToast("Only admins can access Edit Books.", "error");
      window.location.href = "/ui/dashboard";
      return;
    }
    applyRoleVisibility(true);
    showPreview(null);
  })();

  loadBookForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const id = targetBookId.value.trim();
    if (!id) {
      showToast("Enter a book ID.", "error");
      return;
    }

    try {
      const response = await apiRequest(`/books/${id}`);
      const book = await response.json();
      if (handleAuthFailure(response.status)) {
        return;
      }
      if (!response.ok) {
        throw new Error(book.detail || "Unable to load book");
      }
      loadedBook = book;
      fillForm(book);
      showPreview(book);
      showToast("Book loaded.", "success");
    } catch (error) {
      showToast(error.message, "error");
      showPreview(null);
      loadedBook = null;
    }
  });

  updateBookForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const id = targetBookId.value.trim();
    if (!id) {
      showToast("Load a book first.", "error");
      return;
    }

    const payload = {
      name: editName.value.trim(),
      author: editAuthor.value.trim(),
      genre: editGenre.value.trim() || null,
      published_date: editPublishedDate.value || null,
      description: editDescription.value.trim() || null,
    };

    try {
      const response = await apiRequest(`/books/${id}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });
      const updatedBook = await response.json();
      if (handleAuthFailure(response.status)) {
        return;
      }
      if (!response.ok) {
        throw new Error(updatedBook.detail || "Update failed");
      }
      loadedBook = updatedBook;
      fillForm(updatedBook);
      showPreview(updatedBook);
      showToast("Book updated.", "success");
    } catch (error) {
      showToast(error.message, "error");
    }
  });

  deleteBookBtn.addEventListener("click", async () => {
    const id = targetBookId.value.trim();
    if (!id) {
      showToast("Load a book first.", "error");
      return;
    }

    try {
      const response = await apiRequest(`/books/${id}`, { method: "DELETE" });
      const payload = await response.json();
      if (handleAuthFailure(response.status)) {
        return;
      }
      if (!response.ok) {
        throw new Error(payload.detail || "Delete failed");
      }
      loadedBook = null;
      updateBookForm.reset();
      targetBookId.value = "";
      showPreview(null);
      showToast("Book deleted.", "success");
    } catch (error) {
      showToast(error.message, "error");
    }
  });
});
