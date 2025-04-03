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

    const { setToken, setCpf, setNome, nome } = context;

    const [errorMessage, setErrorMessage] = useState<string | null>(null);


   const[formData, setFormData] = useState({
        nome: '',
        email: '',
        n_celular: '',

   })

   console.log("Nome: " + nome);

   useEffect(() => {
    setFormData((prevData) => ({
        ...prevData,
        nome: nome || "",  
    }));
}, [nome]);


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
        if(response.data.error != true){
            setNome(response.data.data.nome);
            setCpf(response.data.data.cpf);
            setToken("1");
            navigate('/EditarPerfil');
            window.alert("Os dados foram atualizados");
        } else {
            window.alert("Erro ao fazer login! " + response.data.message);
        }
        
        })
        .catch(error => {
        console.error('Erro ao enviar dados:', error);
        });
    }
    
    console.log("Nome: " + nome);
          

    return(
        <div className="telainicio">
             <div className="sidebar">
            <button onClick={() => navigate('/EditarPerfil')} className="button"><img src={perfil} className='adicionar'/></button>
            <button onClick={() => navigate('/Home')} className="button"><img src={home} className='adicionar'/></button>
            <button onClick={() => navigate('/AdicionarReceitaDespesa')} className="button"><img src={adicionar} className='adicionar'/></button>
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
                    <button type="submit" className=" button-editar"> Sair </button>
                    </div>
                </form>

            </div>
        </div>
    )

}