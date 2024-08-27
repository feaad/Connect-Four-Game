const directions = [
  { dr: 0, dc: 1 }, // Horizontal (right)
  { dr: 1, dc: 0 }, // Vertical (down)
  { dr: 1, dc: 1 }, // Diagonal (down-right)
  { dr: 1, dc: -1 }, // Diagonal (down-left)
];

const isWithinBounds = (board: number[][], row: number, col: number): boolean =>
  row >= 0 && row < board.length && col >= 0 && col < board[0].length;

const checkDirection = (
  row: number,
  col: number,
  dr: number,
  dc: number,
  token: number,
  board: number[][],
): string[] => {
  const connected: string[] = [`${row}-${col}`];

  for (let step = 1; step < 4; step++) {
    const newRow = row + dr * step;
    const newCol = col + dc * step;

    if (
      isWithinBounds(board, newRow, newCol) &&
      board[newRow][newCol] === token
    ) {
      connected.push(`${newRow}-${newCol}`);
    } else {
      break;
    }
  }

  return connected.length === 4 ? connected : [];
};

export const findConnectedToken = (board: number[][]): string[] => {
  const result: string[] = [];

  board.forEach((row, rowIndex) => {
    row.forEach((token, colIndex) => {
      if (token === 0) {
        return;
      }

      directions.forEach(({ dr, dc }) => {
        const connected = checkDirection(
          rowIndex,
          colIndex,
          dr,
          dc,
          token,
          board,
        );
        if (connected.length > 0) {
          result.push(...connected);
        }
      });
    });
  });

  return result;
};
