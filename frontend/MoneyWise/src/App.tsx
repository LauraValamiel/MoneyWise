import { AppRoutes } from "./routes";
import StoreProvider from './components/store/Provider.jsx';


export function App() {

  return(
    <StoreProvider>
      <AppRoutes />
    </StoreProvider>

  ) 
}
