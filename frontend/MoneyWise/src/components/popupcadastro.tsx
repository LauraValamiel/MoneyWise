import React from 'react';
import Popup from 'reactjs-popup';
import './popupcadastro.css';

export default () => (
  <Popup
    trigger={<button className="button"> Open Modal </button>}
    modal
    nested
  >
    {close => (
      <div className="modal">
        <button className="close" onClick={close}>
          &times;
        </button>
        <div className="header"> Erro ao fazer login </div>
        <div className="content">
          {' '}
          Verifique seu usuario e senha e tente novamente
        </div>
        <div className="actions">
          <button
            className="button"
            onClick={() => {
              console.log('modal closed ');
              close();
            }}
          >
            Fechar
          </button>
        </div>
      </div>
    )}
  </Popup>
);