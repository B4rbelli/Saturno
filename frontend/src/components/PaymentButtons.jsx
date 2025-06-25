import React from "react";

const botoes = [
  { label: "PIX", valor: "PIX" },
  { label: "Cartão", valor: "CARTAO" },
  { label: "PayPal", valor: "PAYPAL" },
  { label: "Boleto", valor: "BOLETO" },
  { label: "Cripto", valor: "CRIPTO" },
];

export default function PaymentButtons({ onSelecionarMetodo }) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
      {botoes.map((botao) => (
        <button
          key={botao.valor}
          onClick={() => onSelecionarMetodo(botao.valor)}
          className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-xl transition duration-200 shadow-sm"
        >
          {botao.label}
        </button>
      ))}
    </div>
  );
}
