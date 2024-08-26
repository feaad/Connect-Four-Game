import { Game } from "@/types/types";

import { getGameData } from "@/actions/getGameData";
interface GridStore {
  gameId: string;

  game: Game;

  emptyRows: number[];

  token: number;

  columnHighlight: number;

  init: (gameId:string) => void;

  onMouseOver: (col: number) => void;

  onMouseOut: (col: number) => void;

  onCellClick: (col: number) => void;

  isColumnFull: (col: number) => boolean;

  isMyTurn: () => boolean;

  getToken: (row: number, col: number) => number;

  updateGame: (playerToken: number, row: number, col: number) => void;
}

const gridStore: GridStore = {
  gameId: '',

  game: {
    gameId: '',
    playerOne: "",
    playerTwo: "",
    rows: 0,
    cols: 0,
    board: [],
    currentTurn: "",
    username: "",
  },

  emptyRows: [],

  token: 0,

  columnHighlight: -1,

  async init(gameId: string) {
    if (this.game.gameId === "") {
      const game = (await getGameData(gameId)) as Game;

      if (!game) {
        return;
      }
      this.game = game;

      this.token = this.game.username === this.game.playerOne ? 1 : 2;

      // Initialize emptyRows array to the length of the data array
      this.emptyRows = new Array(this.game.cols).fill(0);

      // For each column find the first empty row from the bottom
      for (let i = 0; i < this.game.cols; i++) {
        for (let j = this.game.rows - 1; j >= 0; j--) {
          if (this.game.board[j][i] === 0) {
            this.emptyRows[i] = j;
            break;
          }
        }
      }
    }
  },

  getToken(row: number, col: number) {
    return this.game.board[row][col];
  },

  onMouseOver(col: number) {

    // this.columnHighlight = col;
    if (this.isMyTurn()){
      this.columnHighlight = col;
    } else {
      this.columnHighlight = -1;
    }
  },

  onMouseOut(col: number) {
    this.columnHighlight = -1;
  },

  onCellClick(col: number) {
    const row = this.emptyRows[col];

    if (row === -1) {
      return;
    }

    this.game.board[row][col] = this.token;

    this.emptyRows[col]--;

    this.game.currentTurn = this.game.currentTurn === this.game.playerOne ? this.game.playerTwo : this.game.playerOne;
  },

  isColumnFull(col: number) {
    if (this.game.board[0][col] === 0) {
      return false;
    }
    return true;
  },

  isMyTurn() {
    return this.game.currentTurn === this.game.username;
  },

  updateGame(playerToken: number, row: number, col: number) {
    this.game.board[row][col] = playerToken;

    if(playerToken !== this.token) {
      this.game.currentTurn = this.game.username;
    }

    this.emptyRows[col]--;
  },

 
};

export default gridStore;
