import React from 'react';
import { Route, Redirect, Switch } from 'react-router-dom'
import './App.css';
import Home from './pages/Home'

function App() {
  return (
    <div className="App">
      <Switch>
        <Route path="/" component={Home} />
        <Redirect to="/" />
      </Switch>
    </div>
  );
}

export default App;
