import { Link, useNavigate } from "react-router-dom"
import { use, useContext, useState } from "react"
import StoreContext from '../components/store/Context'
import axios from 'axios'
import '../App.css'



export const Login = () => {
   const navigate = useNavigate()
   const context = useContext(StoreContext);

   if (!context) {
       throw new Error("StoreContext deve ser usado dentro de um Provider");
   }

   const { setToken, setCpf, setNome } = context;


   const[formData, setFormData] = useState({
        login: '',
        senha: '',

   })

   const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = event.target;
        setFormData((prevData) => ({
        ...prevData,
        [name]: value,
        }));
   }

   

   const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {

        axios.post('http://127.0.0.1:5000/api/login', formData)
        .then(response => {
        console.log(response.data);
        console.log("Recebendo nome do banco:", response.data.data.nome);

        if(response.data.error != true){
            const nomeRecebido = response.data.data.nome;
            const nomeCorreto = typeof nomeRecebido === "object" ? nomeRecebido[0] : nomeRecebido;
            
            console.log("🔹 Nome recebido:", nomeCorreto);
            console.log("🔹 CPF recebido:", response.data.data.cpf.toString());
            
            setNome(nomeCorreto);
            setCpf(response.data.data.cpf);
            setToken("1");
            navigate('/Home');
        } else {
            window.alert("Erro ao fazer login! " + response.data.message);
        }

        
        })
        .catch(error => {
        console.error('Erro ao enviar dados:', error);
        });
        event.preventDefault();
    }

    return(
        <div className="App-header">
            <form onSubmit={handleSubmit}>
                <div className="form">
                <label>Login</label>
                <label>
                    Email:<br/>
                    <input
                        name="login"
                        className='dadosLogin'
                        value={formData.login}
                        onChange={handleInputChange} />
                </label>
                <label>
                    Senha:<br/>
                    <input
                    name="senha"
                    type="password"
                    className='dadosLogin'
                    value={formData.senha}
                    onChange={handleInputChange}/>

                </label>
                <button type="submit" className="button button-logincadastro"> Entrar </button>
                </div>
            </form>

        </div>
    )


}