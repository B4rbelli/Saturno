import React, { useState } from "react";

const Login = ({ onLogin }) => {
  const [token, setToken] = useState("");

  const handleLogin = () => {
    // Armazena o token localmente e chama callback
    localStorage.setItem("token", token);
    onLogin(token);
  };

  return (
    <div style={{ padding: "1rem" }}>
      <h2>Login com Token</h2>
      <input
        type="text"
        placeholder="Cole o token aqui..."
        value={token}
        onChange={(e) => setToken(e.target.value)}
        style={{ width: "300px", marginRight: "10px" }}
      />
      <button onClick={handleLogin}>Entrar</button>
    </div>
  );
};

export default Login;
