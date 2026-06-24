(function () {
  function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
  }

  function setupArchivePagination(nav) {
    var archive = nav.closest(".archive");
    if (!archive) return;

    var list = archive.querySelector("[data-archive-list]");
    var pageButtons = nav.querySelector("[data-archive-pages]");
    var prevButton = nav.querySelector("[data-archive-prev]");
    var nextButton = nav.querySelector("[data-archive-next]");
    if (!list || !pageButtons || !prevButton || !nextButton) return;

    var items = Array.prototype.slice.call(list.querySelectorAll("[data-archive-item]"));
    var pageSize = parseInt(list.getAttribute("data-archive-page-size"), 10) || 10;
    var totalPages = Math.ceil(items.length / pageSize);
    if (totalPages <= 1) return;

    var currentPage = 1;

    function renderPageButtons() {
      pageButtons.innerHTML = "";

      for (var page = 1; page <= totalPages; page += 1) {
        var button = document.createElement("button");
        button.className = "af-page-link archive-page-button";
        button.type = "button";
        button.textContent = String(page);
        button.setAttribute("data-archive-page", String(page));
        button.setAttribute("aria-label", "Archive page " + page);

        if (page === currentPage) {
          button.classList.add("active");
          button.setAttribute("aria-current", "page");
        }

        pageButtons.appendChild(button);
      }
    }

    function showPage(page, shouldScroll) {
      currentPage = clamp(page, 1, totalPages);
      var start = (currentPage - 1) * pageSize;
      var end = start + pageSize;

      items.forEach(function (item, index) {
        var isVisible = index >= start && index < end;
        item.hidden = !isVisible;
        item.classList.toggle("archive-post-hidden", !isVisible);
      });

      prevButton.disabled = currentPage === 1;
      nextButton.disabled = currentPage === totalPages;
      renderPageButtons();

      if (shouldScroll) {
        archive.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }

    nav.addEventListener("click", function (event) {
      var target = event.target;
      if (!(target instanceof HTMLElement)) return;

      if (target.matches("[data-archive-prev]")) {
        showPage(currentPage - 1, true);
        return;
      }

      if (target.matches("[data-archive-next]")) {
        showPage(currentPage + 1, true);
        return;
      }

      var page = target.getAttribute("data-archive-page");
      if (page) {
        showPage(parseInt(page, 10), true);
      }
    });

    showPage(1, false);
  }

  document.querySelectorAll("[data-archive-pagination]").forEach(setupArchivePagination);
})();
