import React, { useState, useEffect } from "react";
import axios from 'axios';
import BasWallet from "./BasicWallet";

import './Wallet.css';


function BasicWallet() {
  const blockchain = 'http://0.0.0.0:5000/'
  const [basicWallet, setBasicWallet] = useState();

  useEffect(() => {
    axios
      .get(`${blockchain}/chain`)
      .then(response => {
        setBasicWallet(response.data)
      })
      .catch(error => console.log(error));
  }, []);

  return(
    <div className="wallet-wrapper">
      <h1>Wallet</h1>
      
    </div>
  )
}

export default BasicWallet;