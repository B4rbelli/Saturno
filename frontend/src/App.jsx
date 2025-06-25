import React, { useState } from "react";
import PaymentList from "./components/PaymentList";
import PaymentButtons from "./components/PaymentButtons";
import PixForm from "./components/PixForm";
import CartaoForm from "./components/CartaoForm";
import PayPalForm from "./components/PayPalForm";
import BoletoForm from "./components/BoletoForm";
import CriptoForm from "./components/CriptoForm";

export default function App() {
  const [metodoSelecionado, setMetodoSelecionado] = useState("");

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 font-sans">
      {/* Cabeçalho fixo com sombra */}
      <header className="bg-indigo-600 text-white px-6 py-4 shadow-md">
        <h1 className="text-2xl sm:text-3xl font-bold tracking-tight">
          Painel de Pagamentos
        </h1>
      </header>

      {/* Conteúdo principal com padding e espaçamento */}
      <main className="max-w-3xl mx-auto p-6 space-y-6">
        {/* Botões com função de seleção */}
        <PaymentButtons onSelecionarMetodo={setMetodoSelecionado} />

        {/* Formulário dinâmico com base no método selecionado */}
        {metodoSelecionado === "PIX" && <PixForm />}
        {metodoSelecionado === "CARTAO" && <CartaoForm />}
        {metodoSelecionado === "PAYPAL" && <PayPalForm />}
        {metodoSelecionado === "BOLETO" && <BoletoForm />}
        {metodoSelecionado === "CRIPTO" && <CriptoForm />}

        {/* Lista de pagamentos já feitos */}
        <PaymentList />
      </main>
    </div>
  );
}
