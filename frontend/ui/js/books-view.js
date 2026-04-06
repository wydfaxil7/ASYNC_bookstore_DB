document.addEventListener("DOMContentLoaded", () => {
  if (!ensureAuthenticated()) {
    return;
  }

  const listForm = document.getElementById("listForm");
  const detailForm = document.getElementById("detailForm");
  const bookList = document.getElementById("bookList");
  const bookDetail = document.getElementById("bookDetail");
  const listStatus = document.getElementById("listStatus");
  const listCount = document.getElementById("listCount");
  const listPagination = document.getElementById("listPagination");
  const limitInput = document.getElementById("limit");
  const offsetInput = document.getElementById("offset");

  let activePage = 1;

  (async () => {
    const user = await fetchCurrentUser();
    if (!user) {
      window.location.href = "/ui/login";
      return;
    }
    applyRoleVisibility(Boolean(user.is_admin));
  })();

  const loadBooks = async (page = activePage) => {
    listStatus.textContent = "Loading books...";
    activePage = Math.max(1, Number(page || 1));
    const limitValue = Math.max(1, Number(limitInput.value || 20));
    const offsetValue = (activePage - 1) * limitValue;
    offsetInput.value = String(offsetValue);

    const params = new URLSearchParams();
    params.set("limit", String(limitValue));
    params.set("offset", String(offsetValue));

    const author = document.getElementById("authorFilter").value.trim();
    const genre = document.getElementById("genreFilter").value.trim();
    const startDate = document.getElementById("startDate").value.trim();
    const endDate = document.getElementById("endDate").value.trim();
    const sortBy = document.getElementById("sortBy").value.trim();
    const order = document.getElementById("orderBy").value.trim();

    if (author) params.set("author", author);
    if (genre) params.set("genre", genre);
    if (startDate) params.set("start_date", startDate);
    if (endDate) params.set("end_date", endDate);
    if (sortBy) params.set("sort_by", sortBy);
    if (order) params.set("order", order);

    try {
      const response = await apiRequest(`/books?${params.toString()}`);
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || "Unable to load books");
      }
      const books = payload.data || [];
      renderBookGrid(bookList, books, "No books matched the current filters.");
      listCount.textContent = `${payload.total ?? books.length} books`;
      listStatus.textContent = payload.message || "Book list loaded";
      renderPagination(listPagination, payload.total ?? books.length, limitValue, offsetValue, loadBooks);
      showToast("Books loaded.", "success");
    } catch (error) {
      listStatus.textContent = "Load failed";
      listPagination.innerHTML = "";
      showToast(error.message, "error");
    }
  };

  listForm.addEventListener("submit", (event) => {
    event.preventDefault();
    loadBooks(1);
  });

  detailForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const bookId = document.getElementById("bookId").value.trim();
    if (!bookId) {
      showToast("Enter a book ID.", "error");
      renderBookDetail(bookDetail, null);
      return;
    }

    try {
      const response = await apiRequest(`/books/${bookId}`);
      const book = await response.json();
      if (!response.ok) {
        throw new Error(book.detail || "Unable to load the book");
      }
      renderBookDetail(bookDetail, book, "Selected Book");
      showToast("Book loaded.", "success");
    } catch (error) {
      showToast(error.message, "error");
      renderBookDetail(bookDetail, null);
    }
  });

  loadBooks(1);
});
