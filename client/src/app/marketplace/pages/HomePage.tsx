'use client';
import React, { FC } from 'react';
import ProductList from '../components/ProductList';
import './HomePage.css';

export interface Product {
    id: number;
    name: string;
    price: number;
    image: string;
}

const products: Product[] = [
    { id: 1, name: 'Product 1', price: 20, image: '/images/product1.jpg' },
    { id: 2, name: 'Product 2', price: 35, image: '/images/product2.jpg' },
    { id: 3, name: 'Product 3', price: 50, image: '/images/product3.jpg' },
    { id: 4, name: 'Product 4', price: 65, image: '/images/product4.jpg' }
];

const HomePage: FC = () => {
    return (
        <>
            <main className="home-container">
                <h2 className="welcome-text">Welcome to the Marketplace!</h2>
                <ProductList products={products} />
            </main>
        </>
    );
};

export default HomePage;