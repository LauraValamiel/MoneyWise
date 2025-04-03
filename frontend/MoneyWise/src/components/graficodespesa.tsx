import React, { useEffect, useState } from 'react';

const DespesasPorCategoria = () => {
  const [graficoUrl, setGraficoUrl] = useState<string>('');
  const [resultados, setResultados] = useState<Record<string, number>>({});

  useEffect(() => {
    const fetchDespesasPorCategoria = async () => {
      const response = await fetch('http://localhost:5000/api/despesasPorCategoria?login=usuario');
      const data = await response.json();
      
      setResultados(data.resultados);
      setGraficoUrl(data.grafico_url); // URL da imagem gerada
    };

    fetchDespesasPorCategoria();
  }, []);

  return (
    <div>
      <h1>Despesas por Categoria</h1>
      <div>
        {Object.entries(resultados).map(([categoria, valor]) => (
          <div key={categoria}>
            <strong>{categoria}: </strong>{valor}%
          </div>
        ))}
      </div>

      <h2>Gráfico:</h2>
      {graficoUrl && <img src={graficoUrl} alt="Despesas por Categoria" />}
    </div>
  );
};

export default DespesasPorCategoria;
