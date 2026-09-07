function loadPlotly() {
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = "https://cdn.plot.ly/plotly-4.0.0.min.js";
    script.integrity = "sha256-FEYfO0yRyLtZCpnW0Dw/0DHKQO7Afrq3ml4+rBB818o=";
    script.crossOrigin = "anonymous";
    script.onload = resolve;
    script.onerror = () => reject(new Error("Cannot load Plotly"));
    document.head.append(script);
  });
}

async function startDemo(root) {
  root.innerHTML = `
    <p class="demo-message" role="status">예제를 준비하고 있습니다. 첫 실행에는 잠시 시간이 걸립니다.</p>
    <p class="demo-result" aria-live="polite"></p>
    <div class="demo-plot"></div>
    <form class="demo-controls" aria-label="예제 설정">
      <button type="reset" disabled>초기화</button>
    </form>
    <button class="demo-retry" type="button" hidden>다시 불러오기</button>
  `;
  const message = root.querySelector(".demo-message");
  const status = root.querySelector(".demo-result");
  const plot = root.querySelector(".demo-plot");
  const form = root.querySelector(".demo-controls");
  const reset = form.querySelector("button");
  const retry = root.querySelector(".demo-retry");
  const pending = new Map();
  const parameters = {};
  let worker;
  let requestId = 0;
  let busy = false;
  let queued = false;
  let failed = false;

  function fail(error) {
    if (failed) return;
    failed = true;
    console.error("Python demo:", error);
    worker?.terminate();
    for (const request of pending.values()) request.reject(error);
    pending.clear();
    form.querySelectorAll("input, button").forEach((control) => { control.disabled = true; });
    root.setAttribute("aria-busy", "false");
    message.textContent = "예제를 불러오거나 계산하지 못했습니다. 다시 불러와 주세요.";
    retry.hidden = false;
  }

  function request(operation, payload = {}) {
    return new Promise((resolve, reject) => {
      const id = ++requestId;
      pending.set(id, { resolve, reject });
      worker.postMessage({ id, operation, ...payload });
    });
  }

  async function update() {
    if (failed) return;
    queued = true;
    if (busy) return;
    busy = true;
    root.setAttribute("aria-busy", "true");
    message.textContent = "계산 중…";
    try {
      // Only the latest slider position needs a result when inputs arrive quickly.
      while (queued && !failed) {
        queued = false;
        const result = await request("compute", { parameters: { ...parameters } });
        if (queued) continue;
        const layout = {
          ...result.figure.layout,
          autosize: true,
          height: 460,
          paper_bgcolor: "transparent",
          plot_bgcolor: "transparent",
          font: { ...result.figure.layout?.font, color: getComputedStyle(root).color },
        };
        await Plotly.react(plot, result.figure.data, layout, { responsive: true, displaylogo: false });
        status.textContent = result.status;
      }
      if (!failed) message.textContent = "";
    } catch (error) {
      fail(error);
    } finally {
      busy = false;
      root.setAttribute("aria-busy", "false");
    }
  }

  retry.addEventListener("click", () => location.reload());
  form.addEventListener("submit", (event) => event.preventDefault());
  root.setAttribute("aria-busy", "true");

  try {
    worker = new Worker(new URL("./python-worker.js", import.meta.url), { type: "module" });
    worker.onerror = (event) => fail(new Error(event.message || "Cannot start Python worker"));
    worker.onmessage = ({ data: { id, result, error } }) => {
      const request = pending.get(id);
      if (!request) return;
      pending.delete(id);
      if (error) request.reject(new Error(error));
      else request.resolve(result);
    };
    window.addEventListener("pagehide", (event) => {
      if (!event.persisted) worker.terminate();
    });

    const [controls] = await Promise.all([
      request("initialize", {
        source: new URL(root.dataset.source, document.baseURI).href,
        packages: JSON.parse(root.dataset.packages || "[]"),
      }),
      loadPlotly(),
    ]);

    const inputs = controls.map((control) => {
      const label = document.createElement("label");
      label.className = "demo-control";
      const name = document.createElement("span");
      name.textContent = control.label;
      const input = document.createElement("input");
      input.type = "range";
      input.name = control.name;
      input.min = control.min;
      input.max = control.max;
      input.step = control.step;
      input.value = control.value;
      input.setAttribute("aria-label", control.label);
      const output = document.createElement("output");
      const sync = () => {
        parameters[control.name] = Number(input.value);
        output.value = Number(input.value).toFixed(control.decimals ?? 2);
      };
      sync();
      input.addEventListener("input", () => { sync(); update(); });
      label.append(name, input, output);
      form.insertBefore(label, reset);
      return { input, control, sync };
    });
    form.addEventListener("reset", (event) => {
      event.preventDefault();
      for (const { input, control, sync } of inputs) {
        input.value = control.value;
        sync();
      }
      update();
    });
    reset.disabled = false;
    await update();
  } catch (error) {
    fail(error);
  }
}

const root = document.querySelector("[data-python-demo]");
if (root) startDemo(root);
