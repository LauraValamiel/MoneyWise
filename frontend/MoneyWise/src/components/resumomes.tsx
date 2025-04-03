import React, { useState, useEffect } from 'react';
import axios from 'axios';
import "./ResumoMes.css";

const ResumoMesAno: React.FC = () => {
  const [ano, setAno] = useState<number>(new Date().getFullYear());
  const [mes, setMes] = useState<number>(new Date().getMonth() + 1);
  const [resumo, setResumo] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Função para buscar dados do backend
  const fetchResumoMesAno = async (anoEscolhido: number, mesEscolhido: number) => {
    setLoading(true);
    setError(null);
    try {
      const mesFormatado = mesEscolhido < 10 ? `0${mesEscolhido}` : `${mesEscolhido}`;
      const resposta = await axios.get(`/api/resumo/${anoEscolhido}-${mesFormatado}`);
      setResumo(resposta.data);
    } catch (erro) {
      console.error('Erro ao buscar dados:', erro);
      setError("Erro ao carregar os dados.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResumoMesAno(ano, mes);
  }, [ano, mes]);

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
              R$ {resumo?.receitas ? resumo.receitas.toFixed(2) : "0.00"}
            </span>
          </div>
          <div className="item-sumario">
            <span>Despesas</span>
            <span className="amount">
              R$ {resumo?.despesas ? resumo.despesas.toFixed(2) : "0.00"}
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
