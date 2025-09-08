// Copyright (c) 2017 Florian Klampfer
// Licensed under MIT

/* eslint-disable no-param-reassign */

import katex from "katex";

import { hasFeatures, hide, matches } from "./common";

const REQUIREMENTS = ["eventlistener", "queryselector"];

const KATEX_CSS_URL = 'https://unpkg.com/katex@0.7.1/dist/katex.min.css';
let katexStyle;
let katexLoaded = false;

function willChangeContent(mathBlocks) {
  Array.prototype.forEach.call(mathBlocks, (el) => {
    el.style.willChange = "content"; // eslint-disable-line no-param-reassign
  });
}

function replaceMathBlock(el, tex) {
  el.outerHTML = katex.renderToString(tex, {
    displayMode: el.type === "math/tex; mode=display",
  });
}

function renderKatex(el, tex) {
  try {
    const prev = el.previousElementSibling;
    replaceMathBlock(el, tex);
    if (prev && matches(prev, ".MathJax_Preview")) hide(prev);
  } catch (e) {
    if (process.env.NODE_ENV !== 'production') {
      console.error(e); // eslint-disable-line no-console
    }
  } finally {
    el.style.willChange = "";
  }
}

function readTexSource(el) {
  return el.textContent.replace("% <![CDATA[", "").replace("%]]>", "");
}

function changeContent(mathBlocks) {
  // kramdown generates script tags with type "math/tex"
  Array.prototype.forEach.call(mathBlocks, (script) => {
    const tex = readTexSource(script);
    renderKatex(script, tex);
  });
}

function loadKatexCSS(cb) {
  if (katexLoaded) {
    cb();
    return;
  }
  if (!katexStyle) {
    const ref = document.getElementsByTagName('style')[0];
    katexStyle = loadCSS(KATEX_CSS_URL, ref);
    katexStyle.addEventListener('load', () => {
      katexLoaded = true;
      cb();
    });
  } else {
    katexStyle.addEventListener('load', cb);
  }
}

export default function upgradeMathBlocks() {
  if (hasFeatures(REQUIREMENTS)) {
    const mathBlocks = document.querySelectorAll('script[type^="math/tex"]');
    if (mathBlocks.length) {
      willChangeContent(mathBlocks);
      loadKatexCSS(() => { changeContent(mathBlocks); });
    }
  }
}


upgradeMathBlocks();