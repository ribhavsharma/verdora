import React, { FC } from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ProductPage from './pages/ProductPage';
import './App.css';


const MarketplacePage: FC = () => {
    return (
      <div className="app">
        {/* <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/product/:id" element={<ProductPage />} />
        </Routes> */}
      </div>
    );
};

export default MarketplacePage;