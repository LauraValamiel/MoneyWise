import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import "./ResumoMes.css";
import StoreContext from './store/Context';

const ResumoMesAno: React.FC = () => {
  const context = useContext(StoreContext);

  if (!context) {
    throw new Error("StoreContext deve ser usado dentro de um Provider");
  }

  const { cpf } = context;

  //console.log("CPF do contexto:", cpf[0]);
  const cpfCerto = cpf[0].toString(); // Corrigindo o CPF para string
  //console.log("tipo CPF corrigido:", typeof cpfCerto);

  const [ano, setAno] = useState<number>(new Date().getFullYear());
  const [mes, setMes] = useState<number>(new Date().getMonth() + 1);
  const [resumo, setResumo] = useState<{ receitas: number; despesas: number}>({
    receitas: 0,
    despesas: 0,
  });
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Função para buscar dados do backend
  const fetchResumoMesAno = async (anoEscolhido: number, mesEscolhido: number) => {
    if(!cpfCerto) return;
    setLoading(true);
    setError(null);
    try {
      const mesFormatado = mesEscolhido < 10 ? `0${mesEscolhido}` : `${mesEscolhido}`;

      const respostaReceita = await axios.get("http://localhost:5000/api/resumoDoMesReceita", {
        params:{ ano: anoEscolhido, mes: mesFormatado, cpf: cpfCerto },
        withCredentials: true,
      });

      const respostaDespesa = await axios.get("http://localhost:5000/api/resumoDoMesDespesa", {
        params:{ ano: anoEscolhido, mes: mesFormatado, cpf: cpfCerto },
        withCredentials: true,
      });
      
      setResumo({
        receitas: respostaReceita.data.receitas || 0,
        despesas: respostaDespesa.data.despesas || 0,
      });

      }catch (erro) {
      console.error('Erro ao buscar dados:', erro);
      setError("Erro ao carregar os dados.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if(cpfCerto){// Verifica se o CPF está definido antes de fazer a requisição
    fetchResumoMesAno(ano, mes);
    }
  }, [ano, mes, cpfCerto]);

  const gerarAnos = () => {
    const anoAtual = new Date().getFullYear();
    return Array.from({ length: 6 }, (_, i) => anoAtual - i);
  };

  const gerarMeses = () => [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
  ];

  return (
    <div className="resumo-mes">
      <div className="header-resumo">
        <div className='titulo-resumo'>
          {/*<h3>Resumo de {gerarMeses()[mes - 1]} de {ano}</h3>*/}
          <h3>Resumo do mês</h3>
          <div className="seletores">
            {/* Seleção de Ano */}
            <select value={ano} onChange={(e) => setAno(Number(e.target.value))}>
              {gerarAnos().map((anoOpcao) => (
                <option key={anoOpcao} value={anoOpcao}>
                  {anoOpcao}
                </option>
              ))}
            </select>

            {/* Seleção de Mês */}
            <select value={mes} onChange={(e) => setMes(Number(e.target.value))}>
              {gerarMeses().map((mesNome, index) => (
                <option key={index} value={index + 1}>
                  {mesNome}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {loading ? (
        <p>Carregando...</p>
      ) : error ? (
        <p className="error">{error}</p>
      ) : resumo ? (
        <div className="conteudo-sumario">
          <div className="item-sumario">
            <span>Receitas</span>
            <span className="amount">
              R$ {Number(resumo.receitas || 0).toFixed(2)}
            </span>
          </div>
          <div className="item-sumario">
            <span>Despesas</span>
            <span className="amount">
              R$ {Number(resumo.despesas || 0).toFixed(2)}

            </span>
          </div>
        </div>
      ) : (
        <p className="error">Erro ao carregar os dados do resumo.</p>
      )}
    </div>
  );
};

export default ResumoMesAno;
