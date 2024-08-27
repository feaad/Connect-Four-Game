"use client";

import axios from "axios";
import { useRouter } from "next/navigation";
import { useState } from "react";

const RegisterPage = () => {
  const router = useRouter();
  const [formData, setFormData] = useState({
    username: "fboos",
    email: "fb@example.com",
    password: "password",
    password2: "password",
  });
  const [error, setError] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (formData.password !== formData.password2) {
      setError("Passwords do not match");
      return;
    }

    try {
      console.log("formData", formData);
      await axios.post("/api/auth/register", formData);
      router.push("/login"); // Redirect to login after successful registration
    } catch (error) {
      setError("Registration failed");
    }
  };

  return (
    <div>
      <h1>Register</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Username"
          //   onChange={handleChange}
          value="fboos"
          required
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          //   onChange={handleChange}
          value="fb@example.com"
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          //   onChange={handleChange}
          value="password"
          required
        />
        <input
          type="password"
          name="password2"
          placeholder="Confirm Password"
          //   onChange={handleChange}
          value="password"
          required
        />
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default RegisterPage;
