import { useContext, useEffect, useState } from "react";
import axios from "axios";
import StoreContext from "./store/Context";

interface ResumoFinanceiro {
  saldo: number;
  receita: number;
  despesa: number;
}

const useResumoFinanceiro = () => {

  const context = useContext(StoreContext);

  if (!context) {
    throw new Error("StoreContext deve ser usado dentro de um Provider");
  }

  const { cpf } = context;

  //console.log("CPF do contexto:", cpf[0]);
  const cpfCerto = cpf[0].toString(); // Corrigindo o CPF para string
  //console.log("tipo CPF corrigido:", typeof cpfCerto);

  const [resumo, setResumo] = useState<ResumoFinanceiro | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  
  useEffect(() => {
    const fetchResumo = async () => {
      if(!cpfCerto) return; // Verifica se o CPF está definido antes de fazer a requisição
      setLoading(true);
      setError(null);

      try {

        const saldoRes = await axios.get("http://localhost:5000/api/saldoAtual", {
          params:{ cpf: cpfCerto },
          withCredentials: true,
        });

        const receitaRes = await axios.get("http://localhost:5000/api/receitas", {
          params:{ cpf: cpfCerto },
          withCredentials: true,
        });

        const despesaRes = await axios.get("http://localhost:5000/api/despesas", {
          params:{ cpf: cpfCerto },
          withCredentials: true,
        });


        if (saldoRes.status !== 200 || receitaRes.status !== 200 || despesaRes.status !== 200) {
          throw new Error("Erro ao buscar dados financeiros");
        }

        const saldoData = saldoRes.data;
        const receitaData = receitaRes.data;
        const despesaData = despesaRes.data;

        setResumo({
          saldo: Number(saldoData.saldo) || 0,
          receita: Number(receitaData.sum) || 0, // Garante que pega o valor correto da receita
          despesa: Number(despesaData.sum) || 0, // Garante que pega o valor correto da despesa
        });

      } catch (error) {
        setError("Erro ao carregar os dados financeiros");
      } finally {
        setLoading(false);
      }
    };

    fetchResumo();
  }, []);

  return { resumo, loading, error };
};

export default useResumoFinanceiro;
