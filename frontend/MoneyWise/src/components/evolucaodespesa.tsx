import React, { useContext, useEffect, useState } from 'react';
import StoreContext from './store/Context';
import axios from 'axios';
import './evolucaodespesa.css'

const EvolucaoDespesas = () => {
    const context = useContext(StoreContext);

    if (!context) {
        throw new Error("StoreContext deve ser usado dentro de um Provider");
    }

    const { cpf } = context;
    const cpfCerto = cpf[0].toString();
     
    const [graficoUrl, setGraficoUrl] = useState<string>('');
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!cpfCerto) return;

        const fetchEvolucaoDespesas = async () => {
            const source = axios.CancelToken.source(); // Criar token para cancelar a requisição
            setError(null);
            
            try {
                const response = await axios.get('http://localhost:5000/api/evolucaoDespesas', {
                    params: { cpf: cpfCerto },
                    withCredentials: true,
                });

                if (response.data.grafico_url){
                    setGraficoUrl(`${response.data.grafico_url}?t=${new Date().getTime()}`);
                }else{
                    setError("Erro: 'grafico_url' não foi recebido pela api.")
                }
            } catch (error) {
                console.error("Erro ao buscar dados:", error)
                setError("Erro ao carregar as despesas.")
                
            }
        };
        
        fetchEvolucaoDespesas();

    }, [cpfCerto]);

    return (
        <div className="grafico-container">
            <h1 className="titulo-grafico">Evolução das despesas</h1>
            {graficoUrl && <img src={graficoUrl} alt="Evolução das despesas" className="imagem-grafico" />}
            {error && <p className="erro">{error}</p>}
        </div>
    )

}

export default EvolucaoDespesas;