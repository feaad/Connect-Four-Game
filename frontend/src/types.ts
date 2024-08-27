export interface Token {
  accessToken: string;
  refreshToken: string;
  accessTokenExpires: number;
  player_id: string;
  user_id?: string;
  guest_id?: string;
}

export interface UserToken extends Token {
  username: string;
  email?: string;
}
