interface GridStore {
  data: number[][];

  emptyRows: number[];

  columnHighlight: number;

  init: (data: number[][]) => void;

  onMouseOver: (col: number) => void;

  onMouseOut: (col: number) => void;

  onCellClick: (col: number) => void;

  isColumnFull: (col: number) => boolean;

  getToken: (row: number, col: number) => number;
}

const gridStore: GridStore = {
  data: [],

  emptyRows: [],

  columnHighlight: -1,

  init(data: number[][]) {
    if (this.data.length === 0) {
      this.data = data;

      // Initialize emptyRows array to the length of the data array
      this.emptyRows = new Array(this.data[0].length).fill(0);

      // For each column find the first empty row from the bottom
      for (let i = 0; i < this.data[0].length; i++) {
        for (let j = this.data.length - 1; j >= 0; j--) {
          if (this.data[j][i] === 0) {
            this.emptyRows[i] = j;
            break;
          }
        }
      }
    }
  },

  getToken(row: number, col: number) {
    return this.data[row][col];
  },

  onMouseOver(col: number) {
    this.columnHighlight = col;
  },

  onMouseOut(col: number) {
    this.columnHighlight = -1;
  },

  onCellClick(col: number) {
    const row = this.emptyRows[col];

    if (row === -1) {
      return;
    }

    // TODO: Change to backend call
    this.data[row][col] = row % 2 === 0 ? 1 : 2;

    this.emptyRows[col]--;
  },

  isColumnFull(col: number) {
    if (this.data[0][col] === 0) {
      return false;
    }
    return true;
  },

  // Check if player has won, then return the player details
 
};

export default gridStore;
