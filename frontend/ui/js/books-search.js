document.addEventListener("DOMContentLoaded", () => {
  if (!ensureAuthenticated()) {
    return;
  }

  const searchForm = document.getElementById("searchForm");
  const searchResults = document.getElementById("searchResults");
  const searchStatus = document.getElementById("searchStatus");
  const searchPagination = document.getElementById("searchPagination");
  const limitInput = document.getElementById("limit");
  const offsetInput = document.getElementById("offset");

  let latestQuery = "";
  let latestGenre = "";

  (async () => {
    const user = await fetchCurrentUser();
    if (!user) {
      window.location.href = "/ui/login";
      return;
    }
    applyRoleVisibility(Boolean(user.is_admin));
  })();

  const runSearch = async (page = 1) => {
    searchStatus.textContent = "Searching...";
    searchResults.innerHTML = "";

    const currentPage = Math.max(1, Number(page || 1));
    const limit = Math.max(1, Number(limitInput.value || 20));
    const offset = (currentPage - 1) * limit;
    offsetInput.value = String(offset);

    const params = new URLSearchParams();
    const query = latestQuery;
    const genre = latestGenre;

    if (query) params.set("q", query);
    if (genre) params.set("genre", genre);
    params.set("limit", String(limit));
    params.set("offset", String(offset));

    try {
      const response = await apiRequest(`/books/search?${params.toString()}`);
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || "Search failed");
      }
      const books = payload.data || [];
      renderBookGrid(searchResults, books, "No search results matched your query.");
      searchStatus.textContent = `${payload.total ?? books.length} results`;
      renderPagination(searchPagination, payload.total ?? books.length, limit, offset, runSearch);
      showToast("Search complete.", "success");
    } catch (error) {
      searchStatus.textContent = "Search failed";
      searchPagination.innerHTML = "";
      searchResults.appendChild(createEmptyState("No results could be loaded."));
      showToast(error.message, "error");
    }
  };

  searchForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    latestQuery = document.getElementById("query").value.trim();
    latestGenre = document.getElementById("genre").value.trim();
    runSearch(1);
  });
});
