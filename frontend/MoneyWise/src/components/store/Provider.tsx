import React, { ReactNode } from 'react';
import StoreContext from './Context';
import useStorage from '../utils/useStorage.tsx';

interface StoreProviderProps {
  children: ReactNode;
}

const StoreProvider: React.FC<StoreProviderProps> = ({ children }) => {
  const [token, setToken] = useStorage<string | null>("token", null);
  const [cpf, setCpf] = useStorage<string | null>("cpf", null);
  const [nome, setNome] = useStorage<string | null>("nome", null);

  return (
    <StoreContext.Provider
      value={{
        token,
        setToken,
        cpf,
        setCpf,
        nome,
        setNome,
      }}
    >
      {children}
    </StoreContext.Provider>
  )
}


export default StoreProvider;
