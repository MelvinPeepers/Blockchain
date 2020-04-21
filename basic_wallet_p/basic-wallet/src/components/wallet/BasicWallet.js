import React from 'react';

function BasWallet(props) {
  console.log("picture", props)
  return(
      <div className="nasa-images">
        <img src={props.url} className="nasa-images-frame" alt="NASA"></img>
      </div>
  )
}

export default BasWallet;