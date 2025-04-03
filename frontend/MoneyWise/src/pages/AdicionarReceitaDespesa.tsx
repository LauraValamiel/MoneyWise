import { useNavigate } from "react-router-dom"
import { useContext, useState } from "react"
import StoreContext from '../components/store/Context.tsx'
import axios from 'axios'
import '../App.css'
import '../style/AdicionarReceitaDespesa.css'
import adicionar from "../imagens/adicionardespesareceita-claro.png"
import adicionar1 from "../imagens/adicionardespesareceita-bege.png"
import perfil from "../imagens/perfil-bege.png"
import home from "../imagens/home-bege.png"
import resume from "../imagens/resumo-bege.png"
import relatorio from "../imagens/relatorio-bege.png"
import icone from "../imagens/icon1.png"
import moneywise from "../imagens/moneywise.png"
import valor from "../imagens/valor.png"
import data from "../imagens/data.png"
import categoria from "../imagens/categoria.png"
import descricao from "../imagens/descricao.png"

export const AdicionarReceitaDespesa = () => {
    const navigate = useNavigate()
    const context = useContext(StoreContext);

    if (!context) {
        throw new Error("StoreContext deve ser usado dentro de um Provider");
    }

    const { cpf } = context;
    const [errorMessage, setErrorMessage] = useState<string | null>(null);


    const getCurrentDate = (): string => {
        const today = new Date();
        return today.toISOString().split("T")[0]; // Formato YYYY-MM-DD
    };

   const[formData, setFormData] = useState({
        tipo: '',
        valor: '',
        descricao: '',
        categoria: '',
        data: getCurrentDate,

   })

    const tipos = ['Receita', 'Despesa']

    const categorias = ['Alimentação', 'Casa', 'Compras', 'Educação', 'Entretenimento', 'Outros', 'Roupa', 'Saúde', 'Transporte', 'Viagens']
      

   const handleInputChange = (event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = event.target;
        setFormData((prevData) => ({
        ...prevData,
        [name]: value,
        }));
   }

   const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        

        try {
            const response = await axios.post('http://127.0.0.1:5000/api/AdicionarReceitaDespesa', formData);
            
            console.log(response.data);

            if (response?.data?.error === false && response.data.data) {
                    setNome(response.data.data.nome);
                    setCpf(response.data.data.cpf);
                    setToken("1");
                    navigate("/Home");
            } else {
                    setErrorMessage(response.data?.mensagem || "Erro ao processar o cadastro.");
                }
            } catch (error) {
                console.error("Erro ao enviar dados:", error);
                setErrorMessage("Erro inesperado ao tentar cadastrar. Tente novamente.");
            }
        
    }
    
          

    return(
        <div className="telainicio">
             <div className="sidebar">
            <button onClick={() => navigate('/editarPerfil')} className="button"><img src={perfil} className='adicionar'/></button>
            <button onClick={() => navigate('/Home')} className="button"><img src={home} className='adicionar'/></button>
            <button onClick={() => navigate('/AdicionarReceitaDespesa')} className="button"><img src={adicionar} className='adicionar'/></button>
            <button onClick={() => navigate('/ResumoFinanceiro')} className="button"><img src={resume} className='adicionar'/></button>
            <button onClick={() => navigate('/OrcamentoMensalERelatorio')} className="button"><img src={relatorio} className='adicionar'/></button>

            <img src={icone} className='logo-final'/>
            <img src={moneywise} className='moneywise'/>

            </div>
            <div className="App-header">
                <form onSubmit={handleSubmit}>
                    <div className="form-adicionar">
                    <div className="titulo-adicionar"><label><img src={adicionar1} className='icon-adicionar'/>Adicionar nova despesa/receita</label></div>
                    <div className="form-group">
                        <label className="label-adicionar">
                            <img src={adicionar1} className='icon-adicionar'/>
                            Tipo:<br/>
                            <div className="seletores-adicionar">
                                <select name="tipo" value={formData.tipo} onChange={handleInputChange} className="custom-select-adicionar">
                                    <option value="">Tipo</option>
                                {tipos.map((tipoOpcao) => (
                                    <option key={tipoOpcao} value={tipoOpcao}>
                                    {tipoOpcao}
                                    </option>
                                ))}
                                </select>
                                </div>
                            </label>    
                    </div>
                    <div className="form-group">
                    <label>
                        <img src={valor} className='icon-adicionar'/>
                        Valor:<br/>
                        <input
                            name="valor"
                            className='dadosLogin'
                            value={formData.valor}
                            onChange={handleInputChange}
                        />
                    </label>
                    </div>
                    <div className="form-group">
                    <label>
                        <img src={descricao} className='icon-adicionar'/>
                        Descrição:<br/>
                        <input
                            name="descricao"
                            className='dadosLogin'
                            value={formData.descricao}
                            onChange={handleInputChange}
                        />
                    </label>
                    </div>
                    
                    <div className="form-group">
                    <label>
                        <img src={categoria} className='icon-adicionar'/>
                        Categoria:<br/>
                    <div className="seletores-adicionar">
                            {/* Seleção de Ano */}
                            <select name="categoria" value={formData.categoria} onChange={handleInputChange} className="custom-select-adicionar">
                                <option value="">Categoria</option>
                            {categorias.map((categoriaOpcao) => (
                                <option key={categoriaOpcao} value={categoriaOpcao}>
                                {categoriaOpcao}
                                </option>
                            ))}
                            </select>
                            </div>
                        </label>
                    </div>
                    <div className="form-group">
                    <label>
                        <img src={data} className='icon-adicionar'/>
                        Data:<br/>
                        <input
                        type="date"
                        name="data"
                        className='dadosLogin'
                        value={formData.data}
                        onChange={handleInputChange}/>

                    </label>
                    </div>
                    <button type="submit" className=" button button-adicionar"> Adicionar </button>
                    </div>
                </form>

            </div>
        </div>
    )

}