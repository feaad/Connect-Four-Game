interface User{
  id: string;
  username: string;
  email: string;
  password: string;
}

const users: User[] = [
  {
    id: "660e8586-01a0-4ca2-bc5c-d40850ddd14d",
    username: "user111",
    email: "a@email.com",
    password: "password",
  },
  {
    id: "820e4fda-c2f7-4c8d-a0f8-70a87c60afa5",
    username: "user222",
    email: "b@email.com",
    password: "password",
  },
  {
    id: "71802fd4-aae3-4ef6-a42f-4f6e9f7bb3a9",
    username: "user333",
    email: "c@email.com",
    password: "password",
  }

]

export const getUser = async (email: string) => {
  try {
    return users.find((user) => user.email === email);
  } catch {
    return null;
  }
};