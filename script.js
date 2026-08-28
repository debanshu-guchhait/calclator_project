/* ============================================================
   DEBANSHU'S CALCULATOR
   JAVASCRIPT ENGINE
   Developed By: Debanshu Guchhait
   ============================================================ */


/* ============================================================
   DOM ELEMENTS
   ============================================================ */

const display =
    document.getElementById("display");

const expressionDisplay =
    document.getElementById("expressionDisplay");

const historyCard =
    document.getElementById("historyCard");

const historyList =
    document.getElementById("historyList");

const historyToggle =
    document.getElementById("historyToggle");

const clearHistoryButton =
    document.getElementById("clearHistory");

const scientificToggle =
    document.getElementById("scientificToggle");

const scientificPanel =
    document.getElementById("scientificPanel");

const angleButton =
    document.getElementById("angleButton");


/* ============================================================
   STATE
   ============================================================ */

let history = [];

let scientificVisible = false;

let historyVisible = false;

let angleMode = "DEG";


/* ============================================================
   LOCAL STORAGE
   ============================================================ */

const HISTORY_STORAGE_KEY =
    "debanshuCalculatorHistory";


/* ============================================================
   LOAD HISTORY
   ============================================================ */

function loadHistory() {

    try {

        const savedHistory =
            localStorage.getItem(
                HISTORY_STORAGE_KEY
            );

        if (!savedHistory) {

            history = [];

            return;
        }

        const parsed =
            JSON.parse(savedHistory);

        if (Array.isArray(parsed)) {

            history = parsed;

        } else {

            history = [];

        }

    } catch (error) {

        console.error(
            "History loading error:",
            error
        );

        history = [];

    }

}


/* ============================================================
   SAVE HISTORY
   ============================================================ */

function saveHistory() {

    try {

        localStorage.setItem(
            HISTORY_STORAGE_KEY,
            JSON.stringify(history)
        );

    } catch (error) {

        console.error(
            "History saving error:",
            error
        );

    }

}


/* ============================================================
   FORMAT RESULT
   ============================================================ */

function formatResult(value) {

    if (!Number.isFinite(value)) {

        if (value === Infinity) {

            return "Infinity";

        }

        return "Error";

    }


    if (
        Number.isInteger(value)
    ) {

        return String(value);

    }


    /*
       Limit floating-point noise.
    */

    return Number(
        value.toPrecision(12)
    ).toString();

}


/* ============================================================
   ADD TO DISPLAY
   ============================================================ */

function addToDisplay(value) {

    let current =
        display.value;


    if (
        current === "Error" ||
        current === "Infinity"
    ) {

        current = "";

    }


    display.value =
        current + String(value);

}


/* ============================================================
   CLEAR DISPLAY
   ============================================================ */

function clearDisplay() {

    display.value = "";

    expressionDisplay.textContent = "";

}


/* ============================================================
   BACKSPACE
   ============================================================ */

function backspace() {

    display.value =
        display.value.slice(0, -1);

}


/* ============================================================
   ANGLE CONVERSION
   ============================================================ */

function toRadians(value) {

    if (angleMode === "DEG") {

        return value * Math.PI / 180;

    }

    return value;

}


/* ============================================================
   FACTORIAL
   ============================================================ */

function factorial(value) {

    if (value < 0) {

        throw new Error(
            "Factorial requires a non-negative number"
        );

    }


    if (!Number.isInteger(value)) {

        throw new Error(
            "Factorial requires an integer"
        );

    }


    if (value > 170) {

        throw new Error(
            "Number is too large"
        );

    }


    let result = 1;


    for (
        let i = 2;
        i <= value;
        i++
    ) {

        result *= i;

    }


    return result;

}


/* ============================================================
   TOKENIZER
   ============================================================ */

function tokenize(expression) {

    const tokens = [];

    let i = 0;


    while (
        i < expression.length
    ) {

        const char =
            expression[i];


        /*
           Ignore spaces.
        */

        if (
            /\s/.test(char)
        ) {

            i++;

            continue;

        }


        /*
           Numbers.
        */

        if (
            /[0-9.]/.test(char)
        ) {

            let number = "";

            let dotCount = 0;


            while (
                i < expression.length &&
                /[0-9.]/.test(expression[i])
            ) {

                if (
                    expression[i] === "."
                ) {

                    dotCount++;

                }

                number +=
                    expression[i];

                i++;

            }


            if (dotCount > 1) {

                throw new Error(
                    "Invalid number"
                );

            }


            const value =
                Number(number);


            if (Number.isNaN(value)) {

                throw new Error(
                    "Invalid number"
                );

            }


            tokens.push({
                type: "number",
                value: value
            });


            continue;

        }


        /*
           Constants.
        */

        if (char === "π") {

            tokens.push({
                type: "number",
                value: Math.PI
            });

            i++;

            continue;

        }


        if (char === "e") {

            tokens.push({
                type: "number",
                value: Math.E
            });

            i++;

            continue;

        }


        /*
           Operators.
        */

        if (
            "+-*/%^()".includes(char)
        ) {

            tokens.push({
                type: char,
                value: char
            });

            i++;

            continue;

        }


        /*
           Functions.
        */

        if (
            /[a-zA-Z]/.test(char)
        ) {

            let name = "";


            while (
                i < expression.length &&
                /[a-zA-Z]/.test(expression[i])
            ) {

                name +=
                    expression[i];

                i++;

            }


            tokens.push({
                type: "function",
                value: name.toLowerCase()
            });


            continue;

        }


        throw new Error(
            "Invalid character"
        );

    }


    return tokens;

}


/* ============================================================
   PARSER
   ============================================================ */

class Parser {

    constructor(tokens) {

        this.tokens = tokens;

        this.position = 0;

    }


    current() {

        return this.tokens[
            this.position
        ];

    }


    eat(type) {

        const token =
            this.current();


        if (
            !token ||
            token.type !== type
        ) {

            throw new Error(
                "Invalid expression"
            );

        }


        this.position++;

        return token;

    }


    parse() {

        const result =
            this.parseExpression();


        if (
            this.position <
            this.tokens.length
        ) {

            throw new Error(
                "Invalid expression"
            );

        }


        return result;

    }


    /*
       Addition / subtraction
    */

    parseExpression() {

        let left =
            this.parseTerm();


        while (
            this.current() &&
            (
                this.current().type === "+" ||
                this.current().type === "-"
            )
        ) {

            const operator =
                this.current().type;

            this.position++;


            const right =
                this.parseTerm();


            if (
                operator === "+"
            ) {

                left += right;

            } else {

                left -= right;

            }

        }


        return left;

    }


    /*
       Multiplication / division / modulo
    */

    parseTerm() {

        let left =
            this.parsePower();


        while (
            this.current() &&
            (
                this.current().type === "*" ||
                this.current().type === "/" ||
                this.current().type === "%"
            )
        ) {

            const operator =
                this.current().type;

            this.position++;


            const right =
                this.parsePower();


            if (
                operator === "*"
            ) {

                left *= right;

            }


            else if (
                operator === "/"
            ) {

                if (right === 0) {

                    throw new Error(
                        "Cannot divide by zero"
                    );

                }

                left /= right;

            }


            else {

                left %= right;

            }

        }


        return left;

    }


    /*
       Powers
    */

    parsePower() {

        let left =
            this.parseUnary();


        if (
            this.current() &&
            this.current().type === "^"
        ) {

            this.position++;


            const right =
                this.parsePower();


            left =
                Math.pow(
                    left,
                    right
                );

        }


        return left;

    }


    /*
       Unary + / -
    */

    parseUnary() {

        if (
            this.current() &&
            this.current().type === "+"
        ) {

            this.position++;

            return +this.parseUnary();

        }


        if (
            this.current() &&
            this.current().type === "-"
        ) {

            this.position++;

            return -this.parseUnary();

        }


        return this.parsePrimary();

    }


    /*
       Numbers / parentheses / functions
    */

    parsePrimary() {

        const token =
            this.current();


        if (!token) {

            throw new Error(
                "Invalid expression"
            );

        }


        /*
           Number
        */

        if (
            token.type === "number"
        ) {

            this.position++;

            return token.value;

        }


        /*
           Parentheses
        */

        if (
            token.type === "("
        ) {

            this.position++;


            const value =
                this.parseExpression();


            this.eat(")");


            return value;

        }


        /*
           Function
        */

        if (
            token.type === "function"
        ) {

            const functionName =
                token.value;

            this.position++;


            this.eat("(");


            const value =
                this.parseExpression();


            this.eat(")");


            return applyFunction(
                functionName,
                value
            );

        }


        throw new Error(
            "Invalid expression"
        );

    }

}


/* ============================================================
   SCIENTIFIC FUNCTION ENGINE
   ============================================================ */

function applyFunction(
    functionName,
    value
) {

    switch (functionName) {

        case "sqrt":

            if (value < 0) {

                throw new Error(
                    "Square root requires a non-negative number"
                );

            }

            return Math.sqrt(value);


        case "log":

            if (value <= 0) {

                throw new Error(
                    "Log requires a positive number"
                );

            }

            return Math.log10(value);


        case "ln":

            if (value <= 0) {

                throw new Error(
                    "ln requires a positive number"
                );

            }

            return Math.log(value);


        case "sin":

            return Math.sin(
                toRadians(value)
            );


        case "cos":

            return Math.cos(
                toRadians(value)
            );


        case "tan":

            return Math.tan(
                toRadians(value)
            );


        case "abs":

            return Math.abs(value);


        default:

            throw new Error(
                "Unknown function"
            );

    }

}


/* ============================================================
   EVALUATE EXPRESSION
   ============================================================ */

function evaluateExpression(
    expression
) {

    /*
       Convert × and ÷.
    */

    expression =
        expression
            .replaceAll("×", "*")
            .replaceAll("÷", "/")
            .replaceAll("−", "-");


    /*
       Tokenize.
    */

    const tokens =
        tokenize(expression);


    /*
       Parse.
    */

    const parser =
        new Parser(tokens);


    const result =
        parser.parse();


    if (
        !Number.isFinite(result)
    ) {

        if (
            result === Infinity
        ) {

            return Infinity;

        }

        throw new Error(
            "Invalid result"
        );

    }


    return result;

}


/* ============================================================
   ADD HISTORY
   ============================================================ */

function addHistory(
    expression,
    result
) {

    const item = {

        expression:
            expression,

        result:
            result,

        timestamp:
            new Date().toISOString()

    };


    history.unshift(item);


    /*
       Maximum 100 entries.
    */

    if (
        history.length > 100
    ) {

        history =
            history.slice(0, 100);

    }


    saveHistory();

    renderHistory();

}


/* ============================================================
   FORMAT TIME
   ============================================================ */

function formatTimestamp(
    timestamp
) {

    try {

        const date =
            new Date(timestamp);


        return date.toLocaleString(
            undefined,
            {
                day: "2-digit",
                month: "short",
                year: "numeric",
                hour: "2-digit",
                minute: "2-digit"
            }
        );

    } catch {

        return "";

    }

}


/* ============================================================
   RENDER HISTORY
   ============================================================ */

function renderHistory() {

    historyList.innerHTML = "";


    if (
        history.length === 0
    ) {

        historyList.innerHTML = `
            <div class="empty-history">
                No calculation history
            </div>
        `;

        return;

    }


    history.forEach(
        (item, index) => {

            const historyItem =
                document.createElement("div");


            historyItem.className =
                "history-item";


            historyItem.innerHTML = `

                <div class="history-expression">
                    ${escapeHTML(
                        item.expression
                    )}
                </div>

                <div class="history-result">
                    = ${escapeHTML(
                        item.result
                    )}
                </div>

                <div class="history-time">
                    ${escapeHTML(
                        formatTimestamp(
                            item.timestamp
                        )
                    )}
                </div>

            `;


            /*
               Click history item
               to reuse the result.
            */

            historyItem.addEventListener(
                "dblclick",
                () => {

                    display.value =
                        item.result;

                    expressionDisplay.textContent =
                        item.expression;

                }
            );


            historyList.appendChild(
                historyItem
            );

        }
    );

}


/* ============================================================
   HTML ESCAPE
   ============================================================ */

function escapeHTML(value) {

    return String(value)

        .replaceAll(
            "&",
            "&amp;"
        )

        .replaceAll(
            "<",
            "&lt;"
        )

        .replaceAll(
            ">",
            "&gt;"
        )

        .replaceAll(
            '"',
            "&quot;"
        )

        .replaceAll(
            "'",
            "&#039;"
        );

}


/* ============================================================
   CALCULATE
   ============================================================ */

function calculate() {

    const expression =
        display.value.trim();


    if (!expression) {

        return;

    }


    try {

        let workingExpression =
            expression;


        /*
           Replace factorial.

           Example:
           5! → factorial(5)
        */

        workingExpression =
            convertFactorials(
                workingExpression
            );


        /*
           Add implicit multiplication
           for constants where possible.
        */

        const result =
            evaluateExpression(
                workingExpression
            );


        const formatted =
            formatResult(result);


        expressionDisplay.textContent =
            expression;


        display.value =
            formatted;


        addHistory(
            expression,
            formatted
        );


    } catch (error) {

        console.error(error);


        expressionDisplay.textContent =
            error.message ||
            "Invalid Expression";


        display.value =
            "Error";

    }

}


/* ============================================================
   FACTORIAL CONVERTER
   ============================================================ */

function convertFactorials(
    expression
) {

    let result =
        expression;


    /*
       Simple factorial support.

       Examples:

       5!       → factorial(5)
       (5+2)!   → factorial(5+2)
    */


    while (
        result.includes("!")
    ) {

        /*
           Find !.
        */

        const index =
            result.indexOf("!");


        if (
            index <= 0
        ) {

            throw new Error(
                "Invalid factorial"
            );

        }


        let start =
            index - 1;


        /*
           Number before !
        */

        if (
            /[0-9.]/.test(
                result[start]
            )
        ) {

            while (
                start > 0 &&
                /[0-9.]/.test(
                    result[start - 1]
                )
            ) {

                start--;

            }


            const number =
                result.slice(
                    start,
                    index
                );


            const value =
                Number(number);


            const factorialResult =
                factorial(value);


            result =
                result.slice(
                    0,
                    start
                )
                +
                String(
                    factorialResult
                )
                +
                result.slice(
                    index + 1
                );


            continue;

        }


        /*
           Parenthesized expression.
        */

        if (
            result[start] === ")"
        ) {

            let depth = 0;


            for (
                let i = start;
                i >= 0;
                i--
            ) {

                if (
                    result[i] === ")"
                ) {

                    depth++;

                }


                if (
                    result[i] === "("
                ) {

                    depth--;

                }


                if (
                    depth === 0
                ) {

                    const inside =
                        result.slice(
                            i + 1,
                            start
                        );


                    const value =
                        evaluateExpression(
                            inside
                        );


                    const factorialResult =
                        factorial(value);


                    result =
                        result.slice(
                            0,
                            i
                        )
                        +
                        String(
                            factorialResult
                        )
                        +
                        result.slice(
                            index + 1
                        );


                    break;

                }

            }

        }

    }


    return result;

}


/* ============================================================
   SCIENTIFIC OPERATION
   ============================================================ */

function scientificOperation(
    action
) {

    const current =
        display.value.trim();


    if (!current) {

        return;

    }


    try {

        let expression;

        let result;


        switch (action) {

            case "sqrt":

                expression =
                    `sqrt(${current})`;

                result =
                    evaluateExpression(
                        expression
                    );

                break;


            case "square":

                expression =
                    `(${current})^2`;

                result =
                    evaluateExpression(
                        expression
                    );

                break;


            case "log":

                expression =
                    `log(${current})`;

                result =
                    evaluateExpression(
                        expression
                    );

                break;


            case "ln":

                expression =
                    `ln(${current})`;

                result =
                    evaluateExpression(
                        expression
                    );

                break;


            case "sin":

                expression =
                    `sin(${current})`;

                result =
                    evaluateExpression(
                        expression
                    );

                break;


            case "cos":

                expression =
                    `cos(${current})`;

                result =
                    evaluateExpression(
                        expression
                    );

                break;


            case "tan":

                expression =
                    `tan(${current})`;

                result =
                    evaluateExpression(
                        expression
                    );

                break;


            case "factorial":

                expression =
                    `${current}!`;

                result =
                    factorial(
                        evaluateExpression(
                            current
                        )
                    );

                break;


            default:

                throw new Error(
                    "Unknown scientific operation"
                );

        }


        const formatted =
            formatResult(result);


        expressionDisplay.textContent =
            expression;


        display.value =
            formatted;


        addHistory(
            expression,
            formatted
        );


    } catch (error) {

        expressionDisplay.textContent =
            error.message ||
            "Invalid Expression";


        display.value =
            "Error";

    }

}


/* ============================================================
   TOGGLE SCIENTIFIC MODE
   ============================================================ */

function toggleScientific() {

    scientificVisible =
        !scientificVisible;


    scientificPanel.classList.toggle(
        "hidden",
        !scientificVisible
    );


    if (
        scientificVisible
    ) {

        scientificToggle.textContent =
            "BASIC";

        scientificToggle.style.background =
            "#25235c";

    } else {

        scientificToggle.textContent =
            "SCI";

        scientificToggle.style.background =
            "#344154";

    }


    display.focus();

}


/* ============================================================
   TOGGLE HISTORY
   ============================================================ */

function toggleHistory() {

    historyVisible =
        !historyVisible;


    historyCard.classList.toggle(
        "hidden",
        !historyVisible
    );


    if (
        historyVisible
    ) {

        historyToggle.textContent =
            "✕";

    } else {

        historyToggle.textContent =
            "🕘";

    }

}


/* ============================================================
   TOGGLE DEG / RAD
   ============================================================ */

function toggleAngleMode() {

    if (
        angleMode === "DEG"
    ) {

        angleMode = "RAD";

    } else {

        angleMode = "DEG";

    }


    angleButton.textContent =
        angleMode;

}


/* ============================================================
   BUTTON EVENTS
   ============================================================ */

document
    .querySelectorAll(
        ".calculator-button"
    )
    .forEach(
        button => {

            button.addEventListener(
                "click",
                () => {

                    const value =
                        button.dataset.value;

                    const action =
                        button.dataset.action;


                    if (value !== undefined) {

                        addToDisplay(
                            value
                        );

                        return;

                    }


                    if (
                        action === "clear"
                    ) {

                        clearDisplay();

                        return;

                    }


                    if (
                        action === "backspace"
                    ) {

                        backspace();

                        return;

                    }


                    if (
                        action === "calculate"
                    ) {

                        calculate();

                    }

                }
            );

        }
    );


/* ============================================================
   SCIENTIFIC BUTTON EVENTS
   ============================================================ */

document
    .querySelectorAll(
        ".scientific-button"
    )
    .forEach(
        button => {

            button.addEventListener(
                "click",
                () => {

                    const value =
                        button.dataset.value;

                    const action =
                        button.dataset.action;


                    if (
                        action === "angle"
                    ) {

                        toggleAngleMode();

                        return;

                    }


                    if (
                        value !== undefined
                    ) {

                        addToDisplay(
                            value
                        );

                        return;

                    }


                    if (
                        action
                    ) {

                        scientificOperation(
                            action
                        );

                    }

                }
            );

        }
    );


/* ============================================================
   HEADER EVENTS
   ============================================================ */

scientificToggle.addEventListener(
    "click",
    toggleScientific
);


historyToggle.addEventListener(
    "click",
    toggleHistory
);


clearHistoryButton.addEventListener(
    "click",
    () => {

        history = [];

        saveHistory();

        renderHistory();

    }
);


/* ============================================================
   KEYBOARD SUPPORT
   ============================================================ */

document.addEventListener(
    "keydown",
    event => {

        const key =
            event.key;


        /*
           Numbers
        */

        if (
            /^[0-9]$/.test(key)
        ) {

            addToDisplay(key);

            return;

        }


        /*
           Operators
        */

        if (
            "+-*/().%".includes(key)
        ) {

            addToDisplay(key);

            return;

        }


        /*
           Power
        */

        if (
            key === "^"
        ) {

            addToDisplay("^");

            return;

        }


        /*
           Enter
        */

        if (
            key === "Enter" ||
            key === "="
        ) {

            event.preventDefault();

            calculate();

            return;

        }


        /*
           Backspace
        */

        if (
            key === "Backspace"
        ) {

            event.preventDefault();

            backspace();

            return;

        }


        /*
           Escape
        */

        if (
            key === "Escape"
        ) {

            clearDisplay();

            return;

        }


        /*
           Pi
        */

        if (
            key.toLowerCase() === "p"
        ) {

            addToDisplay("π");

            return;

        }


        /*
           Scientific shortcuts
        */

        if (
            key.toLowerCase() === "s"
        ) {

            scientificOperation(
                "sin"
            );

            return;

        }


        if (
            key.toLowerCase() === "c"
        ) {

            scientificOperation(
                "cos"
            );

            return;

        }


        if (
            key.toLowerCase() === "t"
        ) {

            scientificOperation(
                "tan"
            );

            return;

        }

    }
);


/* ============================================================
   INITIALIZE
   ============================================================ */

loadHistory();

renderHistory();

display.focus();