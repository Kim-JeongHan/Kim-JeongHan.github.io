(() => {
  const typesetToc = () => {
    const tocSidebar = document.querySelector("#toc-sidebar");
    if (!tocSidebar) {
      return;
    }

    const render = () => {
      if (window.MathJax?.typesetPromise) {
        window.MathJax.typesetPromise([tocSidebar]).catch(() => {});
        return;
      }

      if (window.MathJax?.typeset) {
        window.MathJax.typeset([tocSidebar]);
      }
    };

    if (window.MathJax?.startup?.promise) {
      window.MathJax.startup.promise.then(render).catch(() => {});
      return;
    }

    window.requestAnimationFrame(() => window.requestAnimationFrame(render));
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", typesetToc);
  } else {
    typesetToc();
  }
})();
