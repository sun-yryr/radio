import React from 'react';
import { BrowserRouter, Route } from 'react-router-dom';
import Top from './components/Top';
import Search from './components/Search';

const App: React.FC = () => (
    <BrowserRouter>
        <Route exact path="/" component={Top} />
        <Route path="/search" component={Search} />
    </BrowserRouter>
);

export default App;
