(function () {
  const state = {
    quickBook: null,
    quickQuantity: 1,
    quickMaxQuantity: 1,
    cart: [],
    totalItems: 0,
    totalPrice: 0,
  };

  const ids = {
    backdrop: "cartBackdrop",
    drawer: "cartDrawer",
    drawerBody: "cartDrawerBody",
    drawerCount: "cartDrawerCount",
    drawerPrice: "cartDrawerPrice",
    quickModal: "quickAddModal",
    quickImage: "quickAddImage",
    quickTitle: "quickAddTitle",
    quickAuthor: "quickAddAuthor",
    quickGenre: "quickAddGenre",
    quickPrice: "quickAddPrice",
    quickStock: "quickAddStock",
    quickQty: "quickAddQty",
    quickSummary: "quickAddSummary",
    promptModal: "checkoutPromptModal",
    promptMessage: "checkoutPromptMessage",
  };

  function ensureCartUi() {
    if (document.getElementById(ids.backdrop)) return;

    const shell = document.createElement("div");
    shell.innerHTML = `
      <div id="${ids.backdrop}" class="cart-backdrop hidden"></div>

      <aside id="${ids.drawer}" class="cart-drawer hidden" aria-hidden="true">
        <div class="cart-drawer-head">
          <div>
            <p class="kicker">YOUR CART</p>
            <h2>Checkout Cart</h2>
          </div>
          <button type="button" class="icon-btn" data-cart-close aria-label="Close cart">×</button>
        </div>
        <div id="${ids.drawerBody}" class="cart-drawer-body"></div>
        <div class="cart-drawer-footer">
          <div>
            <p class="muted">Total Items</p>
            <strong id="${ids.drawerCount}">0</strong>
          </div>
          <div>
            <p class="muted">Total Price</p>
            <strong id="${ids.drawerPrice}">$0.00</strong>
          </div>
          <button type="button" class="btn" data-cart-checkout>Checkout Cart</button>
        </div>
      </aside>

      <section id="${ids.quickModal}" class="cart-modal hidden" aria-hidden="true">
        <div class="cart-modal-card">
          <button type="button" class="icon-btn cart-modal-close" data-quick-close aria-label="Close">×</button>
          <div class="quick-modal-grid">
            <div class="quick-modal-media">
              <img id="${ids.quickImage}" alt="Book cover" />
            </div>
            <div class="quick-modal-body">
              <p class="kicker">BOOK PREVIEW</p>
              <h2 id="${ids.quickTitle}"></h2>
              <p id="${ids.quickAuthor}" class="muted"></p>
              <p id="${ids.quickGenre}" class="muted"></p>
              <p id="${ids.quickPrice}" class="quick-price"></p>
              <p id="${ids.quickStock}" class="stock-badge"></p>
              <p id="${ids.quickSummary}" class="muted"></p>
              <div class="qty-stepper">
                <button type="button" class="qty-btn" data-qty-minus>-</button>
                <input id="${ids.quickQty}" type="number" value="1" min="1" readonly />
                <button type="button" class="qty-btn" data-qty-plus>+</button>
              </div>
              <div class="cart-modal-actions">
                <button type="button" class="btn" data-quick-add>Add to Cart</button>
                <button type="button" class="btn ghost" data-quick-close>Cancel</button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="${ids.promptModal}" class="cart-modal hidden" aria-hidden="true">
        <div class="cart-modal-card checkout-prompt">
          <p class="kicker">CHECKOUT CART</p>
          <h2>Item added to cart</h2>
          <p id="${ids.promptMessage}" class="muted">Ready to checkout cart?</p>
          <div class="cart-modal-actions">
            <button type="button" class="btn" data-open-cart>Checkout Cart</button>
            <button type="button" class="btn ghost" data-prompt-close>Keep Shopping</button>
          </div>
        </div>
      </section>
    `;

    document.body.appendChild(shell);

    document.getElementById(ids.backdrop)?.addEventListener("click", closeCartDrawer);
    document.querySelectorAll("[data-cart-close]").forEach((btn) => btn.addEventListener("click", closeCartDrawer));
    document.querySelectorAll("[data-quick-close]").forEach((btn) => btn.addEventListener("click", closeQuickAddModal));
    document.querySelectorAll("[data-prompt-close]").forEach((btn) => btn.addEventListener("click", closeCheckoutPrompt));
    document.querySelectorAll("[data-open-cart]").forEach((btn) => btn.addEventListener("click", async () => {
      closeCheckoutPrompt();
      await openCartDrawer();
    }));
    document.querySelectorAll("[data-cart-checkout]").forEach((btn) => btn.addEventListener("click", async () => {
      closeCartDrawer();
      await openCheckoutPrompt("Checkout your cart now.");
    }));
    document.querySelectorAll("[data-quick-add]").forEach((btn) => btn.addEventListener("click", handleQuickAdd));
    document.querySelectorAll("[data-qty-minus]").forEach((btn) => btn.addEventListener("click", () => setQuickQuantity(state.quickQuantity - 1)));
    document.querySelectorAll("[data-qty-plus]").forEach((btn) => btn.addEventListener("click", () => setQuickQuantity(state.quickQuantity + 1)));
    document.querySelectorAll("[data-cart-open]").forEach((btn) => btn.addEventListener("click", async (event) => {
      event.preventDefault();
      await openCartDrawer();
    }));
  }

  function setQuickQuantity(value) {
    const next = Math.max(1, Number(value || 1));
    state.quickQuantity = Math.min(next, state.quickMaxQuantity || 1);
    const input = document.getElementById(ids.quickQty);
    if (input) input.value = String(state.quickQuantity);

    const minus = document.querySelector("[data-qty-minus]");
    const plus = document.querySelector("[data-qty-plus]");
    if (minus) minus.disabled = state.quickQuantity <= 1;
    if (plus) plus.disabled = state.quickQuantity >= state.quickMaxQuantity;
  }

  function imageForBook(book) {
    return `https://picsum.photos/seed/book-${book.id}/560/760`;
  }

  async function handleQuickAdd() {
    if (!state.quickBook) return;
    if (state.quickMaxQuantity <= 0) {
      showToast("This book is out of stock.", "error");
      return;
    }
    const response = await apiRequest("/carts/add", {
      method: "POST",
      body: JSON.stringify({ book_id: state.quickBook.id, quantity: state.quickQuantity }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Failed to add item");
    }

    refreshCartCount(payload.total_items || 0);
    closeQuickAddModal();
    await openCheckoutPrompt("Checkout Cart is ready. Review your items now.");
    showToast("Added to cart");
  }

  async function openQuickAddModal(book) {
    ensureCartUi();
    state.quickBook = book;
    state.quickMaxQuantity = Math.max(0, Number(book.stock ?? 10));
    state.quickQuantity = state.quickMaxQuantity > 0 ? 1 : 0;
    setQuickQuantity(state.quickQuantity || 1);

    document.getElementById(ids.quickImage).src = imageForBook(book);
    document.getElementById(ids.quickTitle).textContent = book.name || "Untitled";
    document.getElementById(ids.quickAuthor).textContent = `by ${book.author || "Unknown"}`;
    document.getElementById(ids.quickGenre).textContent = `Genre: ${book.genre || "Uncategorized"}`;
    document.getElementById(ids.quickPrice).textContent = `$${Number(book.price || 0).toFixed(2)}`;
    const stock = state.quickMaxQuantity;
    const stockLabel = stock <= 0 ? "Out of stock" : stock < 5 ? `Only ${stock} pieces left` : `Stock available: ${stock}`;
    document.getElementById(ids.quickStock).textContent = stockLabel;
    document.getElementById(ids.quickSummary).textContent = book.description || "No description available.";

    const addBtn = document.querySelector("[data-quick-add]");
    const minus = document.querySelector("[data-qty-minus]");
    const plus = document.querySelector("[data-qty-plus]");
    if (addBtn) {
      addBtn.disabled = stock <= 0;
      addBtn.textContent = stock <= 0 ? "Out of stock" : "Add to Cart";
    }
    if (minus) minus.disabled = stock <= 0 || state.quickQuantity <= 1;
    if (plus) plus.disabled = stock <= 0 || state.quickQuantity >= stock;

    const modal = document.getElementById(ids.quickModal);
    const backdrop = document.getElementById(ids.backdrop);
    modal?.classList.remove("hidden");
    backdrop?.classList.remove("hidden");
  }

  function closeQuickAddModal() {
    state.quickBook = null;
    document.getElementById(ids.quickModal)?.classList.add("hidden");
    document.getElementById(ids.backdrop)?.classList.add("hidden");
  }

  async function openCheckoutPrompt(message) {
    ensureCartUi();
    const modal = document.getElementById(ids.promptModal);
    document.getElementById(ids.promptMessage).textContent = message || "Ready to checkout cart?";
    modal?.classList.remove("hidden");
    document.getElementById(ids.backdrop)?.classList.remove("hidden");
  }

  function closeCheckoutPrompt() {
    document.getElementById(ids.promptModal)?.classList.add("hidden");
    document.getElementById(ids.backdrop)?.classList.add("hidden");
  }

  async function loadCart() {
    const response = await apiRequest("/carts");
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Failed to load cart");
    }
    state.cart = Array.isArray(payload.data) ? payload.data : [];
    state.totalItems = Number(payload.total_items || 0);
    state.totalPrice = Number(payload.total_price || 0);
    refreshCartCount(state.totalItems);
    return state;
  }

  function refreshCartCount(value) {
    const total = Number(value || 0);
    document.querySelectorAll("[data-cart-count]").forEach((node) => {
      node.textContent = String(total);
    });
    const drawerCount = document.getElementById(ids.drawerCount);
    if (drawerCount) drawerCount.textContent = String(total);
  }

  function renderCartItems() {
    const body = document.getElementById(ids.drawerBody);
    const count = document.getElementById(ids.drawerCount);
    const price = document.getElementById(ids.drawerPrice);
    if (!body) return;

    body.innerHTML = "";
    count.textContent = String(state.totalItems);
    price.textContent = `$${Number(state.totalPrice || 0).toFixed(2)}`;

    if (!state.cart.length) {
      body.appendChild(createEmptyState("Your cart is empty."));
      return;
    }

    state.cart.forEach((item) => {
      const card = createElement("article", "cart-line");
      const image = createElement("img", "cart-line-image");
      image.src = imageForBook(item.book || { id: item.book_id });
      image.alt = item.book?.name || "Book cover";
      image.onerror = () => { image.src = "/static/ui/assets/bookstore-hero.svg"; };

      const content = createElement("div", "cart-line-content");
      content.appendChild(createElement("h4", "cart-line-title", item.book?.name || `Book #${item.book_id}`));
      content.appendChild(createElement("p", "cart-line-author", item.book?.author || "Unknown author"));
      content.appendChild(createElement("p", "cart-line-price", `$${Number(item.book?.price || 0).toFixed(2)}`));

      const controls = createElement("div", "qty-stepper inline");
      const minus = createElement("button", "qty-btn", "-");
      minus.type = "button";
      minus.addEventListener("click", async () => {
        const next = Math.max(0, Number(item.quantity || 0) - 1);
        if (next <= 0) {
          await removeCartItem(item.id);
        } else {
          await setCartItemQuantity(item.id, next);
        }
      });

      const qty = createElement("span", "qty-value", String(item.quantity || 0));
      const plus = createElement("button", "qty-btn", "+");
      plus.type = "button";
      plus.addEventListener("click", async () => {
        await setCartItemQuantity(item.id, Number(item.quantity || 0) + 1);
      });
      controls.append(minus, qty, plus);

      const remove = createElement("button", "btn ghost cart-remove", "Remove");
      remove.type = "button";
      remove.addEventListener("click", async () => {
        await removeCartItem(item.id);
      });

      content.appendChild(controls);
      content.appendChild(remove);
      card.append(image, content);
      body.appendChild(card);
    });
  }

  async function setCartItemQuantity(itemId, quantity) {
    const response = await apiRequest(`/carts/update/${itemId}`, {
      method: "PUT",
      body: JSON.stringify({ quantity }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Failed to update item");
    }
    state.cart = Array.isArray(payload.data) ? payload.data : [];
    state.totalItems = Number(payload.total_items || 0);
    state.totalPrice = Number(payload.total_price || 0);
    refreshCartCount(state.totalItems);
    renderCartItems();
    showToast("Cart updated");
  }

  async function removeCartItem(itemId) {
    const response = await apiRequest(`/carts/delete/${itemId}`, { method: "DELETE" });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Failed to remove item");
    }
    state.cart = Array.isArray(payload.data) ? payload.data : [];
    state.totalItems = Number(payload.total_items || 0);
    state.totalPrice = Number(payload.total_price || 0);
    refreshCartCount(state.totalItems);
    renderCartItems();
    showToast("Item removed");
  }

  async function openCartDrawer() {
    ensureCartUi();
    await loadCart();
    renderCartItems();
    document.getElementById(ids.drawer)?.classList.remove("hidden");
    document.getElementById(ids.backdrop)?.classList.remove("hidden");
    document.getElementById(ids.drawer)?.setAttribute("aria-hidden", "false");
  }

  function closeCartDrawer() {
    document.getElementById(ids.drawer)?.classList.add("hidden");
    document.getElementById(ids.backdrop)?.classList.add("hidden");
    document.getElementById(ids.drawer)?.setAttribute("aria-hidden", "true");
  }

  async function initCartUi() {
    ensureCartUi();
    document.addEventListener("click", (event) => {
      const trigger = event.target.closest?.("[data-cart-open]");
      if (trigger) {
        event.preventDefault();
        openCartDrawer();
      }
    });
    await loadCart().catch(() => refreshCartCount(0));
  }

  window.openQuickAddModal = openQuickAddModal;
  window.openCartDrawer = openCartDrawer;
  window.refreshCartCount = refreshCartCount;
  window.openCheckoutPrompt = openCheckoutPrompt;
  window.closeCheckoutPrompt = closeCheckoutPrompt;
  window.closeCartDrawer = closeCartDrawer;

  document.addEventListener("DOMContentLoaded", initCartUi);
})();
