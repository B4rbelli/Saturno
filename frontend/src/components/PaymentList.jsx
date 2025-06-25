import React, { useEffect, useState } from "react";

const PaymentList = () => {
  const [pagamentos, setPagamentos] = useState([]);
  const [token, setToken] = useState(localStorage.getItem("token") || "");

  useEffect(() => {
    if (!token) return;

    fetch("http://localhost:8000/pagamentos", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then((res) => res.json())
      .then((data) => setPagamentos(data))
      .catch((err) => console.error("Erro ao buscar pagamentos:", err));
  }, [token]);

  if (!token) {
    return <p>Você precisa estar logado para ver os pagamentos.</p>;
  }

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.reload(); // Ou use window.location.href = '/auth/login' se quiser redirecionar
  };

  return (
    <div>
      <h2>Lista de Pagamentos</h2>
      <ul>
        {pagamentos.map((p) => (
          <li key={p.id}>
            <strong>{p.moeda}</strong> | R$ {p.valor.toFixed(2)} |{" "}
            {p.descricao || "sem descrição"}
          </li>
        ))}
      </ul>
      <button onClick={handleLogout} style={{ marginTop: "20px" }}>
        Sair
      </button>
    </div>
  );
};

export default PaymentList;