import { useContext, useState } from 'react';
import '../App.css'
import Card from "../components/Card.tsx";
import StoreContext from '../components/store/Context';
//import useResumoFinanceiro from "../hooks/useResumoFinanceiro";
import useResumoFinanceiro from '../components/resumofinanceiroti.tsx';
import ResumoMesAno from '../components/resumomes.tsx';
import GraficosDespesas from '../components/graficodespesa.tsx';
import EvolucaoDespesas from '../components/evolucaodespesa.tsx';
import { useNavigate } from 'react-router-dom';
import adicionar from "../imagens/adicionardespesareceita-bege.png"
import perfil from "../imagens/perfil-bege.png"
import home from "../imagens/home-claro.png"
import resume from "../imagens/resumo-bege.png"
import relatorio from "../imagens/relatorio-bege.png"
import icone from "../imagens/icon1.png"
import moneywise from "../imagens/moneywise.png"



export const Home = () => {

    const navigate = useNavigate();
    const context = useContext(StoreContext);

    if (!context) {
        throw new Error("StoreContext deve ser usado dentro de um Provider");
    }

   //const { setToken, setCpf, setNome } = context;

   const { resumo, loading, error } = useResumoFinanceiro();
     
    return(
        <div className="telainicio">
            <div className="sidebar">
            <button onClick={() => navigate('/editarPerfil')} className="button"><img src={perfil} className='adicionar'/></button>
            <button onClick={() => navigate('/Home')} className="button"><img src={home} className='adicionar'/></button>
            <button onClick={() => navigate('/adicionarReceitaOuDespesa')} className="button"><img src={adicionar} className='adicionar'/></button>
            <button onClick={() => navigate('/ResumoFinanceiro')} className="button"><img src={resume} className='adicionar'/></button>
            <button onClick={() => navigate('/OrcamentoMensalERelatorio')} className="button"><img src={relatorio} className='adicionar'/></button>

            <img src={icone} className='logo-final'/>
            <img src={moneywise} className='moneywise'/>

            </div>
            <main className="main-content">
                    {loading ? (
                <p>Carregando...</p>
                ) : error ? (
                <p className="error">{error}</p>
                ) : (
                <div className="cards">
                    <Card title="Saldo atual" amount={`$${typeof resumo?.saldo === "number" ? resumo.saldo.toFixed(2) : "0.00"}`}/>
                    <Card title="Receita" amount={`$${typeof resumo?.receita === "number" ? resumo.receita.toFixed(2) : "0.00"}`}/>
                    <Card title="Despesas" amount={`$${typeof resumo?.despesa === "number" ? resumo.despesa.toFixed(2) : "0.00"}`}/>
                </div>
                )}

                <ResumoMesAno/>
                
                <div className="container-graficos">
                    <GraficosDespesas />

                    <EvolucaoDespesas />
                </div>
                

            </main>

        </div>
    )

}