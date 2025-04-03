import { useContext, useEffect, useState } from 'react';
import '../App.css'
import '../style/OrcamentoMensalERelatorio.css';
import StoreContext from '../components/store/Context.tsx';
import { useNavigate } from 'react-router-dom';
import adicionar from "../imagens/adicionardespesareceita-bege.png"
import perfil from "../imagens/perfil-bege.png"
import home from "../imagens/home-bege.png"
import resume from "../imagens/resumo-bege.png"
import relatorio from "../imagens/relatorio-bege.png"
import relatorio1 from "../imagens/relatorio-claro.png"
import icone from "../imagens/icon1.png"
import moneywise from "../imagens/moneywise.png"
import data from "../imagens/data.png"
import alimentacao from "../imagens/alimentacao.png"
import compras from "../imagens/compras.png"
import educacao from "../imagens/educacao.png"
import entretenimento from "../imagens/entretenimento.png"
import outros from "../imagens/outros.png"
import roupa from "../imagens/roupa.png"
import saude from "../imagens/saude.png"
import viagens from "../imagens/viagens.png"
import transporte from "../imagens/transporte.png"
import categoria from "../imagens/categoria.png"
import valor from "../imagens/valor.png"
import axios from 'axios';



const OrcamentoMensalERelatorio: React.FC = () => {

    const navigate = useNavigate();
    const context = useContext(StoreContext);

    if (!context) {
        throw new Error("StoreContext deve ser usado dentro de um Provider");
    }
    
    const { cpf } = context;

    const [ano, setAno] = useState(new Date().getFullYear());
    const [mes, setMes] = useState("Janeiro");
    const [valorGasto, setValorGasto] = useState(0);
    const [relatorio, setRelatorio] = useState<{ [key: string]: number }>({});

    const gerarAnos = () => {
        const anoAtual = new Date().getFullYear();
        return Array.from({ length: 6 }, (_, i) => anoAtual - i);
    };
    
    const gerarMeses = () => [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ];

    const categorias = [
        "Alimentação", "Casa", "Compras", "Educação", "Entretenimento",
        "Outros", "Roupa", "Saúde", "Transporte", "Viagens"
    ];

    const iconesCategorias: Record<string, string> = {
        "Alimentação": alimentacao,
        "Casa": home,
        "Compras": compras,
        "Educação": educacao,
        "Entretenimento": entretenimento,
        "Outros": outros,
        "Roupa": roupa,
        "Saúde": saude,
        "Transporte": transporte,
        "Viagens": viagens,
    };

    useEffect(() => {
        if (cpf) {
          buscarOrcamentoMensal();
          buscarRelatorio();
        }
    }, [cpf, ano, mes]);

    const buscarOrcamentoMensal = async () => {
        try {
            const response = await axios.get("http://localhost:5000/api/orcamentoMensal", {
                params: {
                login: cpf,
                ano: ano,
                mes: mes,
                },
            });

            setValorGasto(response.data || 0 );;

        } catch (error) {
            console.error("Erro ao buscar orçamento mensal:", error);
        }
    }

    const buscarRelatorio = async () => {
        try {
            const response = await axios.get("http://localhost:5000/api/relatorio", {
                params: { 
                    login: cpf,
                    ano: ano,
                    mes: mes,
                },
            });

            setRelatorio(response.data || {});

        } catch (error) {
            console.error("Erro ao buscar relatório:", error);
        }

    }

    if (!cpf) {
        return <p>Carregando...</p>;
    }


    const metade = Math.ceil(categorias.length / 2);
    const primeiraColuna = categorias.slice(0, metade);
    const segundaColuna = categorias.slice(metade);


    return (
        <div className="telainicio">
            <div className="sidebar">
            <button onClick={() => navigate('/EditarPerfil')} className="button"><img src={perfil} className='adicionar'/></button>
            <button onClick={() => navigate('/Home')} className="button"><img src={home} className='adicionar'/></button>
            <button onClick={() => navigate('/adicionarReceitaOuDespesa')} className="button"><img src={adicionar} className='adicionar'/></button>
            <button onClick={() => navigate('/ResumoFinanceiro')} className="button"><img src={resume} className='adicionar'/></button>
            <button onClick={() => navigate('/OrcamentoMensalERelatorio')} className="button"><img src={relatorio1} className='adicionar'/></button>

            <img src={icone} className='logo-final'/>
            <img src={moneywise} className='moneywise'/>

            </div>
            <div className="pagina">
                <div className="orcamento-conatainer">
                    <div className="orcamento-mensal">
                    <div className="orcamento-titulo"><label><img src={relatorio1} className='icon-orcamento'/>Orçamento Mensal</label></div>
                    <div className="mes-container">
                        <div className="mes-titulo"><label><img src={data} className='icon-orcamento'/>Mês/Ano:</label></div>
                            <div className="orcamento-inputs">
                                <select
                                    value={mes}
                                    onChange={(e) => setMes((parseInt(e.target.value)).toString())}>
                                    {gerarMeses().map((mes, index) => (
                                    <option key={index} value={index + 1}>
                                        {mes}
                                    </option>
                                    ))}
                                </select>
                                <select
                                    value={ano}
                                    onChange={(e) => setAno(parseInt(e.target.value))}
                                >
                                    {gerarAnos().map((ano) => (
                                    <option key={ano} value={ano}>
                                        {ano}
                                    </option>
                                    ))}
                                </select>
                            </div>
                            </div>
                            <div className="titulo-valor"><label><img src={valor} className='icon-orcamento'/>Valor total gasto: R$ {valorGasto.toFixed(2)}</label></div>
                        </div> 
                    </div>
            

                    <div className="relatorio">
                        <div className="orcamento-titulo"><label><img src={relatorio1} className='icon-orcamento'/>Relatório</label></div>
                        <div className="orcamento-titulo"><label><img src={categoria} className='icon-orcamento'/>Despesas por categorias</label></div>
                        <div className="relatorio-container">
                            <div className="relatorio-coluna">
                                <ul>
                                    {primeiraColuna.map((categoria) => (
                                        <li key={categoria}>
                                            <img src={iconesCategorias[categoria]} alt={categoria}/>
                                            <span >{categoria}</span> <span className="porcentagem">{((relatorio[categoria] || 0) * 100).toFixed(2)}%</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                            <div className="relatorio-coluna">
                                <ul>
                                    {segundaColuna.map((categoria) => (
                                        <li key={categoria}>
                                            <img src={iconesCategorias[categoria]} alt={categoria}/>
                                            <span >{categoria}</span> <span className="porcentagem">{((relatorio[categoria] || 0)* 100).toFixed(2)}%</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    </div>

            </div>
        </div>
            

       
    )



   


}

export default OrcamentoMensalERelatorio;