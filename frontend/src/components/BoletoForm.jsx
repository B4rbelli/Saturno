import React, { useState } from "react";

export default function BoletoForm() {
  const [valor, setValor] = useState("");
  const [descricao, setDescricao] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("token");
    const res = await fetch("http://localhost:8000/boleto/pagar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ valor: parseFloat(valor), descricao }),
    });

    const data = await res.json();
    alert(data.mensagem || "Boleto gerado com sucesso.");
    setValor("");
    setDescricao("");
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white p-6 mt-6 rounded-xl shadow-md max-w-md mx-auto space-y-4"
    >
      <h2 className="text-xl font-semibold text-indigo-700">Pagamento por Boleto</h2>

      <div>
        <label className="block text-sm font-medium mb-1">Valor (R$)</label>
        <input
          type="number"
          value={valor}
          onChange={(e) => setValor(e.target.value)}
          required
          className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Descrição</label>
        <input
          type="text"
          value={descricao}
          onChange={(e) => setDescricao(e.target.value)}
          className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
      </div>

      <button
        type="submit"
        className="bg-indigo-600 hover:bg-indigo-700 text-white py-2 px-4 rounded-md w-full font-semibold transition duration-200"
      >
        Gerar Boleto
      </button>
    </form>
  );
}
