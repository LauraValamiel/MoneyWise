import { Link, useNavigate } from "react-router-dom"
import '../App.css'
import '../style/MoneyWise.css'
import logo from "../imagens/logo.png"
import ilustracao from "../imagens/ilustracao.png"



export const MoneyWise = () => {
    const navigate = useNavigate();
  
   return (
    

        <><header className="header-cabecalho">
            <img src={logo} className="logo-cabecalho"/>
            <div className="button-cabecalho">
                <button onClick={() => navigate('/login')} className="login-button">
                    Entrar
                </button>
                <button onClick={() => navigate('/cadastro')} className="login-button">
                    Cadastrar
                </button>
            </div>
       </header>
       {/*Corpo da pagina inicial*/}
       <div className="telainicial">
               <h1 className="title">Seja bem-vindo(a) ao MoneyWise!</h1>

                <div className="conteudo">
                    <img src={ilustracao} alt="Ilustração financeira" className="ilustracao"></img>

                    <div className="info-box">
                        <h2>O que é o MoneyWise?</h2>
                        <p>
                            O MoneyWise facilita a gestão financeira, ajudando a acompanhar gastos e tomar melhores decisões.
                        </p>

                        <h3>Com o MoneyWise, você pode:</h3>
                        <ul>
                            <li>✅ Registrar e categorizar suas despesas e receitas.</li>
                            <li>✅ Controlar seus gastos.</li>
                            <li>✅ Gerar relatórios para entender melhor sua vida financeira.</li>

                        </ul>

                    </div>

                </div>
               
           </div></>
    )
}


