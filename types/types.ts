export interface Token {
  accessToken: string;
  refreshToken: string;
  accessTokenExpires: number;
  player_id: string;
  username: string;
  user_id?: string;
  guest_id?: string;
}

export interface UserToken extends Token {
  email?: string;
}
export interface Game{
	gameId: string;
	playerOne: string;
	playerTwo: string;
	rows: number;
	cols: number;
	board: number[][];
  currentTurn: string;
  username: string;
}