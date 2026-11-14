/* -- Calculator state --------------------------------------------------------- */

let currentInput = "0";
let previousValue = null;
let pendingOperation = null;        // endpoint string, e.g. "add"
let shouldResetInput = false;

const displayEl = document.getElementById("display");
const expressionEl = document.getElementById("expression");
const historyListEl = document.getElementById("history-list");
const errorEl = document.getElementById("error");

/* -- Helper: format a number for display (avoid floating-point noise) --------- */

function formatNumber(n) {
  if (Number.isInteger(n) && Math.abs(n) < 1e15) return n.toString();
  return parseFloat(n.toPrecision(12)).toString();
}

/* -- Display helpers --------------------------------------------------------- */

function updateDisplay() {
  const parts = currentInput.split(".");
  if (parts.length === 2 && parts[1].length > 10) {
    currentInput = parseFloat(currentInput).toFixed(10);
  }
  displayEl.textContent = formatNumber(parseFloat(currentInput) || 0);
}

function showExpression(text) {
  expressionEl.textContent = text;
}

function showError(msg) {
  errorEl.textContent = msg;
  setTimeout(() => { errorEl.textContent = ""; }, 4000);
}

/* -- API calls (server-side) ------------------------------------------------- */

const OP_MAP = {
  add: "+", subtract: "-", multiply: "*", divide: "/",
  power: "**", modulus: "%"
};

/** Call /calculate with an expression string, return the numeric result. */
async function callApi(operation, a, b) {
  const op = OP_MAP[operation];
  const expression = `${a} ${op} ${b}`;
  showExpression(expression);
  const resp = await fetch("/calculate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ expression })
  });
  const data = await resp.json();
  if (!resp.ok) {
    throw new Error(data.detail || "Calculation failed");
  }
  return data.result;
}

/** Call /calculate for a single-operand operation (e.g. sqrt). */
async function callSingleOpApi(operation, value) {
  if (operation === "sqrt") {
    showExpression(`sqrt(${value})`);
    const resp = await fetch("/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ expression: `sqrt(${value})` })
    });
    const data = await resp.json();
    if (!resp.ok) {
      throw new Error(data.detail || "Calculation failed");
    }
    return data.result;
  }
  if (operation === "negate") {
    showExpression(`negate(${value})`);
    const resp = await fetch("/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ expression: `negate(${value})` })
    });
    const data = await resp.json();
    if (!resp.ok) {
      throw new Error(data.detail || "Calculation failed");
    }
    return data.result;
  }
  throw new Error("Unknown operation");
}

/* -- History ----------------------------------------------------------------- */

function addHistoryEntry(expression, result) {
  const li = document.createElement("li");
  li.textContent = `${expression} = ${result}`;
  historyListEl.prepend(li);
  while (historyListEl.children.length > 20) {
    historyListEl.removeChild(historyListEl.lastChild);
  }
}

/** Fetch history from the server and render it. */
async function loadHistory() {
  try {
    const resp = await fetch("/history");
    if (!resp.ok) return;
    const data = await resp.json();
    const history = data.history || data;
    historyListEl.innerHTML = "";
    // server returns newest last; display newest first
    for (let i = history.length - 1; i >= 0; i--) {
      const entry = history[i];
      const li = document.createElement("li");
      li.textContent = `${entry.expression} = ${entry.result}`;
      historyListEl.appendChild(li);
    }
  } catch (_) {
    // history is not critical for the UI to work
  }
}

/* -- Button handlers --------------------------------------------------------- */

function appendDigit(digit) {
  if (shouldResetInput) {
    currentInput = "0";
    shouldResetInput = false;
  }
  if (digit === ".") {
    if (currentInput.includes(".")) return;
    currentInput += ".";
  } else {
    if (currentInput === "0") {
      currentInput = digit;
    } else {
      currentInput += digit;
    }
  }
  updateDisplay();
}

async function handleOperator(symbol, endpoint) {
  const currentValue = parseFloat(currentInput);
  if (pendingOperation && previousValue !== null && !shouldResetInput) {
    // chain operation
    try {
      const result = await callApi(pendingOperation, previousValue, currentValue);
      previousValue = result;
      currentInput = result.toString();
      updateDisplay();
    } catch (err) {
      showError(err.message);
      return;
    }
  } else {
    previousValue = currentValue;
  }
  pendingOperation = endpoint;
  shouldResetInput = true;
  if (previousValue !== null) {
    showExpression(formatNumber(previousValue) + " " + symbol);
  }
}

async function handleEquals() {
  if (!pendingOperation || previousValue === null) {
    if (currentInput.includes(".")) {
      currentInput = parseFloat(currentInput).toFixed(10);
      updateDisplay();
    }
    return;
  }
  const currentValue = parseFloat(currentInput);
  try {
    const result = await callApi(pendingOperation, previousValue, currentValue);
    const expr = `${formatNumber(previousValue)} ${OP_MAP[pendingOperation]} ${formatNumber(currentValue)}`;
    addHistoryEntry(expr, formatNumber(result));
    currentInput = result.toString();
    previousValue = null;
    pendingOperation = null;
    shouldResetInput = true;
    updateDisplay();
  } catch (err) {
    showError(err.message);
    pendingOperation = null;
    previousValue = null;
    shouldResetInput = true;
  }
}

async function handleSqrt() {
  const value = parseFloat(currentInput);
  if (value < 0) {
    showError("Cannot calculate the square root of a negative number");
    return;
  }
  try {
    const result = await callSingleOpApi("sqrt", value);
    addHistoryEntry(`sqrt(${formatNumber(value)})`, formatNumber(result));
    currentInput = result.toString();
    previousValue = null;
    pendingOperation = null;
    shouldResetInput = true;
    updateDisplay();
  } catch (err) {
    showError(err.message);
  }
}

async function handleNegate() {
  const value = parseFloat(currentInput);
  try {
    const result = await callSingleOpApi("negate", value);
    currentInput = result.toString();
    updateDisplay();
  } catch (err) {
    showError(err.message);
  }
}

function handleClear() {
  currentInput = "0";
  previousValue = null;
  pendingOperation = null;
  shouldResetInput = false;
  showExpression("\u00A0");
  errorEl.textContent = "";
  updateDisplay();
}

/* -- Wire up buttons --------------------------------------------------------- */

document.querySelectorAll("[data-digit]").forEach(btn => {
  btn.addEventListener("click", () => appendDigit(btn.dataset.digit));
});
document.querySelector("[data-digit='.']").addEventListener("click", () => appendDigit("."));

document.querySelectorAll("[data-op]").forEach(btn => {
  btn.addEventListener("click", () => handleOperator(btn.textContent.trim(), btn.dataset.api));
});

document.querySelector("[data-action='clear']").addEventListener("click", handleClear);
document.querySelector("[data-action='equals']").addEventListener("click", handleEquals);

document.querySelector("[data-action='sqrt']").addEventListener("click", handleSqrt);
document.querySelector("[data-action='negate']").addEventListener("click", handleNegate);

document.querySelector("[data-action='power']").addEventListener("click", () => {
  handleOperator("^", "power");
});
document.querySelector("[data-action='mod']").addEventListener("click", () => {
  handleOperator("%", "modulus");
});

/* -- Keyboard support --------------------------------------------------------- */

document.addEventListener("keydown", (e) => {
  if (e.key >= "0" && e.key <= "9") {
    appendDigit(e.key);
  } else if (e.key === ".") {
    appendDigit(".");
  } else if (e.key === "+") {
    handleOperator("+", "add");
  } else if (e.key === "-") {
    handleOperator("-", "subtract");
  } else if (e.key === "*") {
    handleOperator("×", "multiply");
  } else if (e.key === "/") {
    e.preventDefault();
    handleOperator("÷", "divide");
  } else if (e.key === "Enter" || e.key === "=") {
    handleEquals();
  } else if (e.key === "Escape" || e.key === "c" || e.key === "C") {
    handleClear();
  }
});

/* -- Init -------------------------------------------------------------------- */

updateDisplay();
loadHistory();