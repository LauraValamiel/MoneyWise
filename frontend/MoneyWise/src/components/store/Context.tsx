/*import { createContext } from 'react';

const StoreContext = createContext({
  token: null,
  setToken: () => {},
  cpf: null,
  setCpf: () => {},
  nome: null,
  setNome: () => {},
});

export default StoreContext;*/

import { createContext } from "react";

interface StoreContextType {
  token: string | null;
  setToken: (token: string) => void;
  cpf: string | null;
  setCpf: (cpf: string) => void;
  nome: string | null;
  setNome: (nome: string) => void;
  
}

const StoreContext = createContext<StoreContextType | undefined>(undefined);
/*const StoreContext = createContext<StoreContextType>({
  setToken: () => {},
  token: null,
  setCpf: () => {},
  cpf: null,
  setNome: () => {},
  nome: null,
  
});*/

export default StoreContext;