import { BrowserRouter, Routes, Route, Navigate} from 'react-router-dom'
import { MoneyWise } from './pages/MoneyWise'
import { Login } from './pages/Login'
import { Cadastro } from './pages/Cadastro'
import { Home } from './pages/Home'
import { AdicionarReceitaDespesa } from './pages/AdicionarReceitaDespesa'
import { EditarPerfil } from './pages/EditarPerfil'
import { ResumoFinanceiro } from './pages/ResumoFinanceiro'
import OrcamentoMensalERelatorio from './pages/OrcamentoMensalERelatorio'


export const AppRoutes = () => {

    return(
        <BrowserRouter>
            <Routes>
                <Route path='*' element={<Navigate to='/MoneyWise'/>}/>
                <Route path='/MoneyWise' element={<MoneyWise/>}/>
                <Route path='/login' element={<Login/>}/>
                <Route path='/cadastro' element={<Cadastro/>}/>
                <Route path='/EditarPerfil' element={<EditarPerfil/>}/>
                <Route path='/home' element={<Home/>}/>
                <Route path='/adicionarReceitaDespesa' element={<AdicionarReceitaDespesa/>}/>
                <Route path='/resumoFinanceiro' element={<ResumoFinanceiro/>}/>
                <Route path='/OrcamentoMensalERelatorio' element={<OrcamentoMensalERelatorio/>}/>

            </Routes>
        </BrowserRouter>

    )
}