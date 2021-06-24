import React from 'react';
import { Route, Redirect, Switch } from 'react-router-dom'
import './App.css';
import Home from './pages/Home'
import TestPage from './pages/test';

function App() {
  return (
    <div className="App">
      <Switch>
        <Route path="/" component={Home} />
        <Route path="/testpage" component={TestPage} />
        <Redirect to="/" />
      </Switch>
    </div>
  );
}

export default App;
