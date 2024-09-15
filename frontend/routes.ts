/**
 * An array of routes that are accessible to the public
 * These routes do not require authentication
 * @type {string[]}
 */
export const publicRoutes = [
	"/",
	"/guest"
];

/**
 * An array of routes that are used for authentication
 * These routes will redirect logged in users to /settings
 * @type {string[]}
 */
export const authRoutes = [
	"/auth/signin",
	"/auth/signup"
];

/**
 * An Array of allowed backend API routes
 * @type {string[]}
 */
export const allowedApiRoutes = [
	"/api/auth/login",
	"/api/user/register"
];

/**
 * The prefix for API authentication routes
 * Routes that start with this prefix are used for API authentication purposes
 * @type {string}
 */
export const apiAuthPrefix = "/api/auth";

/**
 * The default redirect path after logging in
 * @type {string}
 */
export const DEFAULT_LOGIN_REDIRECT = "/";

/**
 * An array of routes that should lead to 404 pages
 * @type {string}
 */
export const disabledRoutes = [""];
