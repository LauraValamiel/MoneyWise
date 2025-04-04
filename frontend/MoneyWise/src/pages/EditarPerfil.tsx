import { useNavigate } from "react-router-dom"
import { useContext, useEffect, useState } from "react"
import StoreContext from '../components/store/Context.tsx'
import axios from 'axios'
import '../App.css'
import '../style/EditarPerfil.css'
import adicionar from "../imagens/adicionardespesareceita-bege.png"
import perfil from "../imagens/perfil-claro.png"
import perfil1 from "../imagens/perfil-bege.png"
import home from "../imagens/home-bege.png"
import resume from "../imagens/resumo-bege.png"
import relatorio from "../imagens/relatorio-bege.png"
import icone from "../imagens/icon1.png"
import moneywise from "../imagens/moneywise.png"


export const EditarPerfil = () => {
    const navigate = useNavigate()
    const context = useContext(StoreContext);

    if (!context) {
        throw new Error("StoreContext deve ser usado dentro de um Provider");
    }

    const { setToken, setCpf, cpf, setNome, nome } = context;
    const cpfCerto = cpf[0].toString();

    const [errorMessage, setErrorMessage] = useState<string | null>(null);


   const[formData, setFormData] = useState({
        nome: '',
        email: '',
        n_celular: '',
        cpf: cpfCerto,

   })

   /*console.log("Nome: " + nome);*/

   useEffect(() => {
    setFormData((prevData) => ({
        ...prevData,
        nome: nome || "",
        cpf: cpfCerto  
    }));
    }, [nome, cpfCerto]);

    const handleLogout = () => {
        event.preventDefault(); // Impede o envio do formulário
        event.stopPropagation();
        localStorage.removeItem('userToken'); // Remove token do usuário
        localStorage.removeItem('userData');  // Remove dados do usuário
        navigate('/MoneyWise'); // Redireciona para a tela de login
    };

   const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = event.target;
        setFormData((prevData) => ({
        ...prevData,
        [name]: value,
        }));
   }

   const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        axios.post('http://127.0.0.1:5000/api/editarCliente', formData)
        .then(response => {
        console.log(response.data);
        if (!response.data || response.data.error){
            window.alert("Erro ao atualizar o perfil: " + (response.data?.message || "Erro desconhecido"));
        }

        const data = response.data.data;
        
        if (data){
            setNome(data.nome || "");
            setCpf(data.cpf || "");

        }else{
            console.warn("Dados não retornados pela api.");
        }
        setToken("1");
        navigate('/EditarPerfil');
        window.alert("Os dados foram atualizados");
       
        
        })
        .catch(error => {
        console.error('Erro ao enviar dados:', error);
        });
    }
    
    /*console.log("Nome: " + nome);*/
          

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
            <div className="App-header">
                <form onSubmit={handleSubmit}>
                    <div className="form-editar">
                    <div><img src={perfil1} className="profile-icon"/></div>
                    <h2 className="nome-perfil">{nome}</h2>
                    <label>
                        Nome:<br/>
                        <input
                            name="nome"
                            className='dadosLogin'
                            value={formData.nome}
                            onChange={handleInputChange} />
                     </label>
                     <label>
                        Email:<br/>
                        <input
                            name="email"
                            className='dadosLogin'
                            value={formData.email}
                            onChange={handleInputChange} />
                    </label>
                    <label>
                        N° Celular:<br/>
                        <input
                            name="n_celular"
                            className='dadosLogin'
                            value={formData.n_celular}
                            onChange={handleInputChange} />
                    </label>
                    <button type="submit" className="button-editar"> Salvar </button>
                    <button onClick={handleLogout} className="button-logout">Logout</button>
                    </div>
                </form>

            </div>
        </div>
    )

}