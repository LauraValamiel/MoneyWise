import { useNavigate } from "react-router-dom"
import { useContext, useState } from "react"
import StoreContext from '../components/store/Context.tsx'
import axios from 'axios'
import '../App.css'



export const Cadastro = () => {
    const navigate = useNavigate()
    const context = useContext(StoreContext);

    if (!context) {
        throw new Error("StoreContext deve ser usado dentro de um Provider");
    }

    const { setToken, token, setCpf, cpf, setNome, nome } = context;

    //const { setToken, token, setCpf, cpf, setNome, nome } = useContext(StoreContext);

    const [errorMessage, setErrorMessage] = useState<string | null>(null);


   const[formData, setFormData] = useState({
        nome: '',
        email: '',
        cpf: '',
        telefone: '',
        senha: '',

   })

   const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = event.target;
        setFormData((prevData) => ({
        ...prevData,
        [name]: value,
        }));
   }

   const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        axios.post('http://127.0.0.1:5000/api/cadastro', formData)
        .then(response => {
        console.log(response.data);
        if(response.data.error != true){
            setNome(response.data.cliente.nome);
            setToken("1");
            navigate('/Home');
        } else {
            window.alert("Erro ao fazer cadastro" + response.data.message);
        }
        
        })
        .catch(error => {
        console.error('Erro ao enviar dados:', error);
        });

        /*try {
            const response = await axios.post('http://127.0.0.1:5000/api/cadastro', formData);
            
            console.log(response.data);

            if (response.data && response.data.data && response.data.data.nome) {
                setNome(response.data.data.nome);
                
            } else {
                setErrorMessage("Erro: Nome não encontrado na resposta.");
            }     
            
            if (response?.data?.error === false && response.data.data) {
                setNome(response.data.data.nome);
                setToken("1");
                navigate('/Home');
            } else {
                setErrorMessage(response.data?.mensagem || "Erro ao processar o cadastro.");
            }
            
    
            /*if (!response.data.error) {
                setNome(response.data.data.nome);
                setToken("1"); // Simula token válido
                navigate('/Home');
            } else {
                // Exibe erro no formulário ao invés de só um alerta
                setErrorMessage(response.data.mensagem);
            }*/
        } /*catch (error) {
            console.error('Erro ao enviar dados:', error);
            setErrorMessage("Erro inesperado ao tentar cadastrar. Tente novamente.");
        }*/
        
    

    return(
        <div className="App-header">
            <form onSubmit={handleSubmit}>
                <div className="form">
                <label>Cadastro</label>
                <label>
                    Nome completo:<br/>
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
                        onChange={handleInputChange}
                    />
                </label>
                <label>
                    CPF:<br/>
                    <input
                        name="cpf"
                        className='dadosLogin'
                        value={formData.cpf}
                        onChange={handleInputChange}
                    />
                </label>
                <label>
                    N° de celular:<br/>
                    <input
                        name="telefone"
                        className='dadosLogin'
                        value={formData.telefone}
                        onChange={handleInputChange}
                    />
                </label>
                <label>
                    Senha:<br/>
                    <input
                    name="senha"
                    className='dadosLogin'
                    value={formData.senha}
                    onChange={handleInputChange}/>

                </label>
                <button type="submit" className=" button button-logincadastro"> Cadastrar </button>
                </div>
            </form>

        </div>
    )
    

}