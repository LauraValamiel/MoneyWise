import { useContext, useEffect, useState } from 'react';
import '../App.css'
import '../style/ResumoFinanceiro.css';
import StoreContext from '../components/store/Context.tsx';
import { useNavigate } from 'react-router-dom';
import adicionar from "../imagens/adicionardespesareceita-bege.png"
import perfil from "../imagens/perfil-bege.png"
import home from "../imagens/home-bege.png"
import resume from "../imagens/resumo-claro.png"
import resume1 from "../imagens/resumo-bege.png"
import relatorio from "../imagens/relatorio-bege.png"
import icone from "../imagens/icon1.png"
import moneywise from "../imagens/moneywise.png"
import data from "../imagens/data.png"
import axios from 'axios';


export const ResumoFinanceiro = () => {
    const navigate = useNavigate();
    const context = useContext(StoreContext);

    if (!context) {
        throw new Error("StoreContext deve ser usado dentro de um Provider");
    }

    
    const { cpf } = context;
    const cpfCerto = cpf[0].toString();
    const [ano, setAno] = useState(new Date().getFullYear());
    const [mes, setMes] = useState(new Date().getMonth() + 1/*"Janeiro"*/);
    const [dadosTabela, setDadosTabela] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    
    const gerarAnos = () => {
        const anoAtual = new Date().getFullYear();
        return Array.from({ length: 6 }, (_, i) => anoAtual - i);
    };

    const gerarMeses = () => [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ];

    const meses: { [key: string]: number } = {
        "Janeiro": 1, "Fevereiro": 2, "Março": 3, "Abril": 4,
        "Maio": 5, "Junho": 6, "Julho": 7, "Agosto": 8,
        "Setembro": 9, "Outubro": 10, "Novembro": 11, "Dezembro": 12
      };
      
      

    const fetchResumoFinanceiro = async (anoEscolhido: number, mesEscolhido: string) => {
        if(!cpfCerto) return;
        setLoading(true);
        setError(null);

        const mesNumero = meses[mesEscolhido];

        console.log("mesNumero:", mesNumero);
        console.log("Parâmetros enviados:", { ano: anoEscolhido, mes: mesNumero, cpf: cpfCerto });

        try{
            const response = await axios.get('http://127.0.0.1:5000/api/resumoFinanceiro', {
                params: { ano: anoEscolhido, mes: mesNumero, cpf: cpfCerto },
            })

            setDadosTabela(response.data);
        }catch(error) {
                console.error("Erro ao buscar dados financeiros:", error);
                setError("Erro ao carregar os dados.");
        }finally {
            setLoading(false);
        }
    }

    //console.log("Dados recebidos do backend:", response.data);
    
    useEffect(() => {
        if(cpfCerto){// Verifica se o CPF está definido antes de fazer a requisição
            fetchResumoFinanceiro(ano, gerarMeses()[mes - 1]);
            }
    }, [cpf, mes, ano]);

    

    return(
        <div className="telainicio">
            <div className="sidebar">
            <button onClick={() => navigate('/EditarPerfil')} className="button"><img src={perfil} className='adicionar'/></button>
            <button onClick={() => navigate('/Home')} className="button"><img src={home} className='adicionar'/></button>
            <button onClick={() => navigate('/adicionarReceitaOuDespesa')} className="button"><img src={adicionar} className='adicionar'/></button>
            <button onClick={() => navigate('/ResumoFinanceiro')} className="button"><img src={resume} className='adicionar'/></button>
            <button onClick={() => navigate('/OrcamentoMensalERelatorio')} className="button"><img src={relatorio} className='adicionar'/></button>

            <img src={icone} className='logo-final'/>
            <img src={moneywise} className='moneywise'/>

            </div>


            {/*<div className="form-resumo">*/}
                <div className="resumo-container">
                    <div className="resumo-titulo"><label><img src={resume1} className='icon'/>Resumo Financeiro</label></div>
                    <div className="selecao-container">
                        <div className="mes-titulo"><label><img src={data} className='icon'/>Mês/Ano:</label></div>
                        <div className="selecao-inputs">
                        <select 
                            id="mes" 
                            value={mes} 
                            onChange={(e) => setMes(Number(e.target.value))}>
                            {Object.entries(meses).map(([nomeMes, numeroMes]) => (
                                <option key={numeroMes} value={numeroMes}>{nomeMes}</option>
                            ))}
                        </select>
                            
                            <label htmlFor="ano"></label>
                            <select 
                                id="ano" 
                                value={ano} 
                                onChange={(e) => setAno(Number(e.target.value))}>

                                {gerarAnos().map((ano) => (
                                    <option key={ano} value={ano}>{ano}</option>
                                ))}
                            </select>
                        </div>
                    </div>

                    <table className="tabela-resumo">
                        <thead>
                            <tr>
                                {/*<th>ID</th>*/}
                                <th>Tipo</th>
                                <th>Valor</th>
                                <th>Descrição</th>
                                <th>Categoria</th>
                                <th>Data</th>
                            </tr>
                        </thead>
                        <tbody>
                            {dadosTabela.length > 0 ? (
                                dadosTabela.map((item, index) => ( 
                                    <tr key={index}>
                                        {/*<td>{item.ID}</td>*/}
                                        <td>{item.Tipo}</td>
                                        <td>R$ {item.Valor}</td>
                                        <td>{item.Descricao}</td>
                                        <td>{item.Categoria}</td>
                                        <td>{new Date(item.Data).toLocaleDateString('pt-BR')}</td>
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan={5} className="mensagem-vazia">Nenhum dado encontrado</td>
                                </tr>
                            )}
                        </tbody>
                    </table>    


                </div>
                
               {/*} </div>*/}
        </div>
    );

};