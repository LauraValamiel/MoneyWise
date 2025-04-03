import { useEffect, useState } from "react";
import axios from "axios";

interface ResumoFinanceiro {
  saldo: number;
  receita: number;
  despesa: number;
}

const useResumoFinanceiro = () => {
  const [resumo, setResumo] = useState<ResumoFinanceiro | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [saldoRes, receitaRes, despesaRes] = await Promise.all([
          fetch("http://localhost:5000/api/saldoAtual"),
          fetch("http://localhost:5000/api/receitas"),
          fetch("http://localhost:5000/api/despesas"),
        ]);

        if (!saldoRes.ok || !receitaRes.ok || !despesaRes.ok) {
          throw new Error("Erro ao buscar dados financeiros");
        }

        const saldoData = await saldoRes.json();
        const receitaData = await receitaRes.json();
        const despesaData = await despesaRes.json();

        setResumo({
          saldo: Number(saldoData.saldo) || 0,
          receita: Number(receitaData[0]?.sum) || 0, // Garante que pega o valor correto da receita
          despesa: Number(despesaData[0]?.sum) || 0, // Garante que pega o valor correto da despesa
        });

      } catch (error) {
        setError("Erro ao carregar os dados financeiros");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return { resumo, loading, error };
};

export default useResumoFinanceiro;
