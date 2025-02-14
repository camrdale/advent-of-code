import {LitElement, html, css} from 'lit';
import {customElement, state} from 'lit/decorators.js';
import {classMap} from 'lit/directives/class-map.js';

interface IntcodeState {
  memory: [number];
  input: [number];
  output: [number];
  relative_base: number;
}

interface Operation {
  instruction_pointer: number;
  instruction: number;
  num_parameters: number;
  short_name: string;
  operation_description: string;
  input: [number];
  output: [number];
  relative_base: number;
  input_parameter_locations: [number];
  output_location?: number;
  output_value?: number;
}

interface ReverseOperation {
  output_location?: number;
  output_value?: number;
}

@customElement('intcode-visualizer')
export class IntcodeVisualizer extends LitElement {
  static override styles = css`
    :host {
      width: 100%;
    }

    :host .visualizer {
      display: flex;
      align-items: stretch;
      justify-content: center;
      display: grid;
      grid-template-columns: 5% 60% 30%
    }

    :host .legend {
      display: grid;
      grid-template-columns: 5% repeat(9, 9%)
    }

    :host .memory {
      display: grid;
      grid-template-columns: 4% repeat(16, 6%)
    }

    :host .input-value.used {
      font-weight: bold;
      background-color: #4646FF;
    }

    :host .output-value.used {
      font-weight: bold;
      background-color: red;
    }

    :host .operation.used {
      font-weight: bold;
      background-color: #fff;
    }

    :host .operation.highlighted {
      font-weight: bold;
    }

    :host .operation.unhighlighted {
      color: darkgray;
    }

    :host .memory-value.instruction {
      background-color: #fff;
    }

    :host .memory-value.current-instruction {
      font-weight: bold;
      background-color: green;
    }

    :host .memory-value.parameter {
      font-weight: bold;
      background-color: pink;
    }

    :host .memory-value.input {
      font-weight: bold;
      background-color: #4646FF;
    }

    :host .memory-value.output {
      font-weight: bold;
      background-color: red;
    }
  `;

  @state()
  protected _error: string | null = null;

  @state()
  protected _initialState: IntcodeState | null = null;

  @state()
  protected _currentState: IntcodeState | null = null;

  @state()
  protected _operations = new Array<Operation>(0);

  @state()
  protected _currentOperation = -1;

  @state()
  protected _highlightedShortName = "";

  @state()
  protected _highlightedMemory = new Set<number>();

  protected _reverseOperations = new Array<ReverseOperation>(0);

  protected _allInstructions = new Set<number>();

  protected _allShortNames = new Set<string>();

  constructor() {
    super();
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    if (urlParams.has('f')) {
      const s = urlParams.get('f');
      if (s) {
        this.loadFile(s);
      }
    }
  }

  override connectedCallback() {
    super.connectedCallback()
    window.addEventListener('keydown', this.onKeyDown);
  }

  private async loadFile(filename: string) {
    try {
      const response = await fetch(window.location.origin + '/dumps/' + filename);
      if (response.status !== 200) {
        console.log(response);
        this._error = response.status + ' ' + response.statusText + ': ' + response.url;
        return;
      }
      const json = await response.json();
      console.log(json);
      this.initializeState(json['initial_state'], json['operations']);
    } catch (e) {
      console.log(e);
      this._error = `${e}`;
      return;
    }
  }

  private initializeState(state: IntcodeState, operations: [Operation]) {
    this._initialState = state;
    this._currentState = structuredClone(state);
    this._operations = operations;
    let tempState = structuredClone(state);
    this._reverseOperations = new Array<ReverseOperation>(operations.length);
    this._allInstructions = new Set<number>();
    this._allShortNames = new Set<string>();
    for (let i = 0; i < operations.length; i++) {
      const operation = operations[i]
      if (typeof operation.output_location !== 'undefined') {
        this._reverseOperations[i] = {
          output_location: operation.output_location,
          output_value: tempState.memory[operation.output_location],
        }
        tempState.memory[operation.output_location] = operation.output_value || 0;
      } else {
        this._reverseOperations[i] = {}
      }
      this._allInstructions.add(operation.instruction_pointer)
      this._allShortNames.add(operation.short_name)
    }
  }

  readonly onKeyDown = (e: KeyboardEvent) => {
    if (e.key == 'ArrowDown' && this._currentOperation < this._operations.length - 1) {
      this.advanceToOperation(this._currentOperation + 1)
      e.preventDefault();
    } else if (e.key == 'ArrowUp' && this._currentOperation >= 0) {
      this.advanceToOperation(this._currentOperation - 1)
      e.preventDefault();
    } else if (e.key == 'PageDown') {
      let i = this._currentOperation + 1;
      if (i >= this._operations.length) {
        return;
      }
      while (i < this._operations.length - 1 && !this.isHighlighted(this._operations[i])) {
        i += 1;
      }
      e.preventDefault();
      this.advanceToOperation(i);
    } else if (e.key == 'PageUp') {
      let i = this._currentOperation - 1;
      if (i < -1) {
        return;
      }
      while (i >= 0 && !this.isHighlighted(this._operations[i])) {
        i -= 1;
      }
      e.preventDefault();
      this.advanceToOperation(i);
    }
  };

  private advanceToOperation(newOperation: number) {
    if (!this._currentState || !this._initialState) {
      return;
    }
    if (newOperation == -1) {
      this._currentState.input = this._initialState.input;
      this._currentState.output = this._initialState.output;
      this._currentState.relative_base = this._initialState.relative_base;
    } else {
      if (newOperation == 0) {
        this._currentState.input = this._initialState.input;
      } else {
        this._currentState.input = this._operations[newOperation-1].input;
      }
      this._currentState.output = this._operations[newOperation].output;
      this._currentState.relative_base = this._operations[newOperation].relative_base;
    }
    if (newOperation > this._currentOperation) {
      for (let i = this._currentOperation + 1; i <= newOperation; i++) {
        const operation = this._operations[i];
        if (typeof operation.output_location !== 'undefined') {
          this._currentState.memory[operation.output_location] = operation.output_value || 0;
        }
      }
    }
    if (newOperation < this._currentOperation) {
      for (let i = this._currentOperation; i > newOperation; i--) {
        const operation = this._reverseOperations[i];
        if (typeof operation.output_location !== 'undefined') {
          this._currentState.memory[operation.output_location] = operation.output_value || 0;
        }
      }
    }
    this._currentOperation = newOperation;
  }

  private changeFilterOperation() {
    const inputElement = this.shadowRoot?.getElementById('filter-operation-select') as HTMLInputElement;
    if (inputElement) {
      this._highlightedShortName = inputElement.value;
    } else {
      console.error('Input element not found');
    }

  }

  private setMemoryFilter(index: number) {
    const inputElement = this.shadowRoot?.getElementById('filter-memory-box') as HTMLInputElement;
    if (inputElement) {
      if (this._highlightedMemory.has(index)) {
        this._highlightedMemory.delete(index);
      } else {
        this._highlightedMemory.add(index);
      }
      inputElement.value = (Array.from(this._highlightedMemory)).join();
      this.requestUpdate();
    } else {
      console.error('Input element not found');
    }
  }

  private changeFilterMemory() {
    const inputElement = this.shadowRoot?.getElementById('filter-memory-box') as HTMLInputElement;
    if (inputElement) {
      this._highlightedMemory = new Set<number>();
      for (const memory of inputElement.value.split(',')) {
        this._highlightedMemory.add(parseInt(memory));
      }
      this.requestUpdate();
    } else {
      console.error('Input element not found');
    }
  }

  private setIntersection(iterable: Iterable<number>, set: Set<number>) {
    for (const num of iterable) {
      if (set.has(num)) {
        return true;
      }
    }
    return false;
  }

  private setContainsRange(set: Set<number>, rangeStart: number, rangeEnd: number) {
    for (let i = rangeStart; i <= rangeEnd; i++) {
      if (set.has(i)) {
        return true;
      }
    }
    return false;
  }

  private isHighlighted(operation: Operation) {
    if (this._highlightedShortName) {
      if (operation.short_name === this._highlightedShortName) {
        return true;
      }
    }
    if (this._highlightedMemory.size > 0) {
      if (this._highlightedMemory.has(operation.instruction_pointer) ||
        this.setIntersection(operation.input_parameter_locations, this._highlightedMemory) ||
        this._highlightedMemory.has(operation.output_location || -1) ||
        this.setContainsRange(this._highlightedMemory, operation.instruction_pointer + 1, operation.instruction_pointer + operation.num_parameters)
      ) {
        return true;
      }
    }
    return false;
  }

  override render() {
    if (this._error) {
      return html`
        <div>Error occurred: ${this._error}</div>
      `;
    }
    if (!this._currentState || !this._initialState) {
      return html`
        <div>Append the intcode JSON file to the URL. For example <a href='?f=FOO.json'>${window.location}?f=FOO.json</a></div>
      `;
    }

    const currentOperation = this._currentOperation >= 0 ? this._operations[this._currentOperation] : null;
    const input_data = this._currentState.input.map((data, index) => {
      const classes = {
        "input-value": true, 
        used: !!currentOperation && currentOperation.short_name=='IN' && index == 0
      }
      return html`
        <div class=${classMap(classes)}>
          ${data}
        </div>
      `;
    });
    const output_data = this._currentState.output.map((data, index, data_array) => {
      const classes = {
        "output-value": true,
        used: !!currentOperation && currentOperation.short_name=='OUT' && index == data_array.length - 1
      }
      return html`
        <div class=${classMap(classes)}>
          ${data}
        </div>
      `;
    });
    const memory_data = this._currentState.memory.map((data, index) => {
      let columnHeader = html``;
      if (index % 16 == 0) {
        columnHeader = html`${index}:`;
      }
      const classes = {
        "memory-value": true,
        instruction: this._allInstructions.has(index),
        "current-instruction": !!currentOperation && currentOperation.instruction_pointer == index,
        input: !!currentOperation && currentOperation.input_parameter_locations.includes(index),
        output: !!currentOperation && index == currentOperation.output_location,
        parameter: !!currentOperation && index > currentOperation.instruction_pointer && index <= currentOperation?.instruction_pointer + currentOperation.num_parameters,
      }
      return html`
        ${columnHeader}
        <div class=${classMap(classes)} @click="${() => this.setMemoryFilter(index)}">
          ${data}
        </div>
      `;
    });
    const initialClasses = {
      "operation": true,
      used: this._currentOperation == -1,
    }
    const operations_list = [html`
      <div class=${classMap(initialClasses)} @click="${() => this.advanceToOperation(-1)}">
        INITIAL STATE
      </div>
    `].concat(this._operations?.map((operation, index) => {
      let highlight = false;
      let unhighlight = false;
      if (this._highlightedShortName || this._highlightedMemory.size > 0) {
        highlight = this.isHighlighted(operation);
        unhighlight = !highlight;
      }
      const classes = {
        "operation": true,
        used: index == this._currentOperation,
        highlighted: highlight,
        unhighlighted: unhighlight,
      }
      return html`
        <div class=${classMap(classes)} @click="${() => this.advanceToOperation(index)}">
          ${operation.operation_description}
        </div>
      `;
    }));
    const filter_operations_options = Array.from(this._allShortNames).map((shortName) => {
      return html`
        <option value="${shortName}">${shortName}</option>
      `
    })

    return html`
      <div class="filters">
        <div class="filter-operation">
          <label for="filter-operation-select">Operation:</label>
          <select name="filter-operation" id="filter-operation-select" @change="${this.changeFilterOperation}">
            <option value="">Choose an operation</option>
            ${filter_operations_options}
          </select>
        </div>
        <div class="filter-memory">
          <label for="filter-memory-box">Memory Location:</label>
          <input name="filter-memory" id="filter-memory-box" type="text" @input="${this.changeFilterMemory}"/>
        </div>
      </div>
      <div class="legend">
        <div class="legend-label">Legend:</div>
        <div class="input-value used">Input Read</div>
        <div class="output-value used">Output Written</div>
        <div class="memory-value instruction">All Instructions</div>
        <div class="memory-value current-instruction">Current Instruction</div>
        <div class="memory-value parameter">Instruction Parameter</div>
        <div class="memory-value input">Memory Read</div>
        <div class="memory-value output">Memory Written</div>
        <div class="operation used">Current Operation</div>
      </div>
      <div class="visualizer">
        <div class="non-memory-state">
          <div class="input-label">Input</div>
          <div class="input">${input_data}</div>
          <div class="output-label">Output</div>
          <div class="output">${output_data}</div>
          <div class="relative-base-label">Relative<br/>Base</div>
          <div class="relative-base">${this._currentState.relative_base}</div>
        </div>
        <div class="memory-state">
          <div class="memory-label">Memory</div>
          <div class="memory">${memory_data}</div>
        </div>
        <div class="operations-list">
          <div class="operations-label">Operations</div>
          <div class="operations">${operations_list}</div>
        </div>
      </div>
      `;
  }
}
