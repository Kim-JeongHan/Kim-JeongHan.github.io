import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v314.0.6/full/pyodide.mjs";

let python;

self.onmessage = async ({ data: { id, operation, source, packages, parameters } }) => {
  try {
    let result;
    if (operation === "initialize") {
      const response = await fetch(source);
      if (!response.ok) throw new Error(`Cannot load ${source}: HTTP ${response.status}`);
      const code = await response.text();
      python = await loadPyodide({ packages });
      await python.runPythonAsync(code, { filename: source });
      python.runPython("import json as _demo_json");
      result = python.runPython("_demo_json.dumps(CONTROLS, allow_nan=False)");
    } else if (operation === "compute") {
      python.globals.set("_demo_parameters", JSON.stringify(parameters));
      result = python.runPython(
        "_demo_json.dumps(compute(_demo_json.loads(_demo_parameters)), allow_nan=False)",
      );
    } else {
      throw new Error(`Unknown operation: ${operation}`);
    }
    self.postMessage({ id, result: JSON.parse(result) });
  } catch (error) {
    self.postMessage({ id, error: error.message });
  }
};
