/**
 * Calculator Frontend
 *
 * Runs entirely in the browser – no FastAPI backend required.
 * Open static/index.html directly or serve the static folder.
 */

function round10(n) {
  return Math.round((n + Number.EPSILON) * 1e10) / 1e10;
}

function performOperation(endpoint, a, b) {
  switch (endpoint) {
    case "add":
      return round10(a + b);
    case "subtract":
      return round10(a - b);
    case "multiply":
      return round10(a * b);
    case "divide":
      if (b === 0) throw new Error("Cannot divide by zero");
      return round10(a / b);
    case "power":
      return round10(Math.pow(a, b));
    case "modulus":
      if (b === 0) throw new Error("Cannot compute modulus with zero");
      return round10(a % b);
    default:
      throw new Error("Unknown operation");
  }
}

let currentInput = "0";
let previousValue = null;
let pendingOperation = null;

const expressionEl = document.getElementById("expression");
const resultEl = document.getElementById("result");
const errorEl = document.getElementById("error");
const historyEl = document.getElementById("history");

const MAX_HISTORY = 20;
const history = [];

function updateDisplay() {
  resultEl.textContent = formatNumber(parseFloat(currentInput));
  errorEl.textContent = "";
}

function formatNumber(n) {
  if (Number.isNaN(n)) return "Error";
  const str = n.toString();
  // Limit display length
  if (str.length > 12) {
    return n.toPrecision(10);
  }
  return str;
}

function addHistoryEntry(expr, result) {
  history.push({ expression: expr, result: result });
  if (history.length > MAX_HISTORY) {
    history.shift();
  }
  renderHistory();
}

function renderHistory() {
  historyEl.textContent = "";
  for (let i = history.length - 1; i >= 0; i--) {
    const entry = history[i];
    const div = document.createElement("div");
    div.className = "history-entry";
    const exprSpan = document.createElement("span");
    exprSpan.className = "history-expression";
    exprSpan.textContent = entry.expression;
    const resultSpan = document.createElement("span");
    resultSpan.className = "history-result";
    resultSpan.textContent = entry.result;
    div.appendChild(exprSpan);
    div.appendChild(resultSpan);
    div.addEventListener("click", () => {
      currentInput = entry.result.toString();
      previousValue = null;
      pendingOperation = null;
      expressionEl.textContent = " ";
      updateDisplay();
    });
    historyEl.appendChild(div);
  }
}

function showExpression(text) {
  expressionEl.textContent = text;  // euron: ignore-security — textContent, not innerHTML
}

function appendDigit(digit) {
  if (currentInput === "0" && digit !== ".") {
    currentInput = digit;
  } else {
    currentInput += digit;
  }
  updateDisplay();
}

function handleOperator(opLabel, apiEndpoint) {
  const currentValue = parseFloat(currentInput);
  if (previousValue !== null && pendingOperation) {
    // Chain: compute previous operation first
    callApi(pendingOperation, previousValue, currentValue)
      .then(result => {
        previousValue = result;
        currentInput = result.toString();
        updateDisplay();
        pendingOperation = apiEndpoint;
        showExpression(formatNumber(previousValue) + " " + opLabel);
      })
      .catch(err => showError(err));
  } else {
    previousValue = currentValue;
    pendingOperation = apiEndpoint;
    currentInput = "0";
    showExpression(formatNumber(currentValue) + " " + opLabel);
  }
}

async function callApi(endpoint, a, b) {
  return performOperation(endpoint, a, b);
}

async function callSingleOpApi(endpoint, value) {
  if (endpoint === "sqrt") {
    if (value < 0) {
      throw new Error("Cannot take the square root of a negative number");
    }
    return round10(Math.sqrt(value));
  }
  throw new Error("Unknown operation");
}

function showError(msg) {
  errorEl.textContent = msg;
  expressionEl.textContent = "";  // euron: ignore-security — textContent, not innerHTML
  previousValue = null;
  pendingOperation = null;
}

// -- Button handlers ----------------------------------------------------------

// Number buttons
document.querySelectorAll("[data-num]").forEach(btn => {
  btn.addEventListener("click", () => appendDigit(btn.dataset.num));
});

// Decimal
document.querySelector("[data-action='decimal']").addEventListener("click", () => {
  if (!currentInput.includes(".")) {
    currentInput += ".";
    updateDisplay();
  }
});

// Operators (+, -, ×, ÷)
document.querySelectorAll("[data-op]").forEach(btn => {
  btn.addEventListener("click", () => handleOperator(btn.textContent, btn.dataset.api));
});

// Clear
document.querySelector("[data-action='clear']").addEventListener("click", () => {
  currentInput = "0";
  previousValue = null;
  pendingOperation = null;
  expressionEl.textContent = "\u00A0";  // euron: ignore-security — textContent, not innerHTML
  updateDisplay();
});

// Negate
document.querySelector("[data-action='negate']").addEventListener("click", () => {
  if (currentInput !== "0") {
    currentInput = currentInput.startsWith("-")
      ? currentInput.slice(1)
      : "-" + currentInput;
    updateDisplay();
  }
});

// Square root
document.querySelector("[data-action='sqrt']").addEventListener("click", async () => {
  const value = parseFloat(currentInput);
  try {
    const result = await callSingleOpApi("sqrt", value);
    currentInput = result.toString();
    showExpression("√(" + formatNumber(value) + ")");
    previousValue = null;
    pendingOperation = null;
    updateDisplay();
  } catch (err) {
    showError(err.message);
  }
});

// Power
document.querySelector("[data-action='power']").addEventListener("click", () => {
  handleOperator("↑", "power");
});

// Modulus
document.querySelector("[data-action='mod']").addEventListener("click", () => {
  handleOperator("%", "modulus");
});

// -- Keyboard support ---------------------------------------------------------

document.addEventListener("keydown", (e) => {
  if (e.key >= "0" && e.key <= "9") {
    appendDigit(e.key);
  } else if (e.key === ".") {
    if (!currentInput.includes(".")) {
      currentInput += ".";
      updateDisplay();
    }
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
    // Evaluate pending operation
    if (pendingOperation && previousValue !== null) {
      const currentValue = parseFloat(currentInput);
      callApi(pendingOperation, previousValue, currentValue)
        .then(result => {
          const expr = expressionEl.textContent;
          addHistoryEntry(expr + " " + previousValue + " = ", result.toString());
          currentInput = result.toString();
          previousValue = null;
          pendingOperation = null;
          updateDisplay();
        })
        .catch(err => showError(err.message));
    }
  } else if (e.key === "Escape" || e.key === "c" || e.key === "C") {
    currentInput = "0";
    previousValue = null;
    pendingOperation = null;
    expressionEl.textContent = "\u00A0";  // euron: ignore-security — textContent, not innerHTML
    updateDisplay();
  }
});

// Initial display
updateDisplay();
