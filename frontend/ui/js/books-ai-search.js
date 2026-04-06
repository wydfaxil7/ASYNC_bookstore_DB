document.addEventListener("DOMContentLoaded", () => {
  if (!ensureAuthenticated()) {
    return;
  }

  const form = document.getElementById("aiSearchForm");
  const queryInput = document.getElementById("aiQuery");
  const limitInput = document.getElementById("limit");
  const offsetInput = document.getElementById("offset");
  const aiResults = document.getElementById("aiResults");
  const aiMeta = document.getElementById("aiMeta");
  const aiStatus = document.getElementById("aiStatus");
  const aiPagination = document.getElementById("aiPagination");

  let latestQuery = "";

  (async () => {
    const user = await fetchCurrentUser();
    if (!user) {
      window.location.href = "/ui/login";
      return;
    }
    applyRoleVisibility(Boolean(user.is_admin));
  })();

  const renderResponse = (payload, limitValue, offsetValue, onPageChange) => {
    const books = payload?.books ?? payload?.data ?? payload?.results ?? [];
    const summary = payload?.summary ?? payload?.message ?? payload?.intent ?? "AI search completed.";
    const responseText = payload?.response || payload?.answer || payload?.notes || "";
    const total = Number(payload?.total ?? books.length);

    aiStatus.textContent = `Found ${total} books`;
    aiMeta.innerHTML = "";
    aiMeta.appendChild(createNoteCard("AI summary", summary, responseText || "The search results are ranked by the model response."));
    aiResults.innerHTML = "";

    if (!books.length) {
      aiResults.appendChild(createEmptyState("No matches returned by AI search."));
      return;
    }

    books.forEach((book) => aiResults.appendChild(createBookCard(book)));
    renderPagination(aiPagination, total, limitValue, offsetValue, onPageChange);
  };

  const runSearch = async (page = 1) => {
    aiStatus.textContent = "Searching...";
    const query = latestQuery;
    const limitValue = Math.max(1, Number(limitInput.value || 20));
    const offsetValue = (Math.max(1, Number(page || 1)) - 1) * limitValue;
    offsetInput.value = String(offsetValue);

    try {
      const params = new URLSearchParams({
        query,
        limit: String(limitValue),
        offset: String(offsetValue),
      });
      const response = await apiRequest(`/books/ai-search?${params.toString()}`);
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || payload.message || "AI search failed");
      }
      renderResponse(payload, limitValue, offsetValue, runSearch);
      showToast("AI search loaded.", "success");
    } catch (error) {
      aiStatus.textContent = "Search failed";
      showToast(error.message, "error");
      aiResults.innerHTML = "";
      aiPagination.innerHTML = "";
      aiResults.appendChild(createEmptyState("Unable to fetch AI search results."));
    }
  };

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const query = queryInput.value.trim();
    if (!query) {
      showToast("Enter a search query first.", "error");
      aiStatus.textContent = "Waiting for query";
      return;
    }
    latestQuery = query;
    runSearch(1);
  });
});
