interface GridStore {
  data: number[][];

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

  columnHighlight: -1,

  init(data: number[][]) {
    if (this.data.length === 0) {
      this.data = data;
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
    // Iterate from the bottom of the data array
    for (let i = this.data.length - 1; i >= 0; i--) {
      if (this.data[i][col] === 0) {
        // TODO: Change to backend call
        this.data[i][col] = i % 2 === 0 ? 1 : 2;
        break;
      }
    }
  },

  isColumnFull(col: number) {
    if (this.data[0][col] === 0) {
      return false;
    }
    return true;
  },
};

export default gridStore;
