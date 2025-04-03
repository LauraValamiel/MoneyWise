import React, { useContext, useEffect, useState } from 'react';
import StoreContext from './store/Context';
import axios from 'axios';
import './graficodespesa.css'

const DespesasPorCategoria = () => {
  const context = useContext(StoreContext);

  if (!context) {
    throw new Error("StoreContext deve ser usado dentro de um Provider");
  }

  const { cpf } = context;

  //console.log("CPF do contexto:", cpf[0]);
  const cpfCerto = cpf[0].toString(); // Corrigindo o CPF para string
  //console.log("tipo CPF corrigido:", typeof cpfCerto);

  const [graficoUrl, setGraficoUrl] = useState<string>('');
  const [resultados, setResultados] = useState<Record<string, number>>({});
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([]);
  const [error, setError] = useState<string | null>(null);


  useEffect(() => {

    if(!cpfCerto) return; // Verifica se o CPF está definido antes de fazer a requisição
      setLoading(true);
      setError(null);

    const fetchDespesasPorCategoria = async () => {
      try{
        const response = await axios.get('http://localhost:5000/api/despesasPorCategoria', {
          params:{ cpf: cpfCerto },
        });

        const data = response.data;

        console.log("Resposta da api:", data)
        
        setResultados(data.resultados);
        if (data.grafico_url){
          const imageUrl = `${data.grafico_url}?t=${new Date().getTime()}`;
          setGraficoUrl(imageUrl);
          console.log("URL da imagem:", imageUrl);
        }else{
          console.error("Erro: 'grafico_url' não recebido da API.");
          setGraficoUrl('');
        }
        
      }catch (err) {
        console.error("Erro ao buscar dados:", err);
        setError("Erro ao carregar as despesas.");
      } finally {
        setLoading(false);
      }

    };

    fetchDespesasPorCategoria();
  }, [cpfCerto]);


  useEffect(() => {
    if (graficoUrl) {
      console.log("URL da imagem (atualizado):", graficoUrl);
    }
  }, [graficoUrl]);

  return (
    <div className="grafico-container">
      <h1 className="titulo-grafico">Despesas por Categoria</h1>
      {/*<div>
        {Object.entries(resultados).map(([categoria, valor]) => (
          <div key={categoria}>
            <strong>{categoria}: </strong>{valor.toFixed(2)}%
          </div>
        ))}
      </div>*/}
      <div >{graficoUrl && <img src={graficoUrl} alt="Despesas por Categoria" className="imagem-grafico" />}</div>
    </div>
  );
};

export default DespesasPorCategoria;
