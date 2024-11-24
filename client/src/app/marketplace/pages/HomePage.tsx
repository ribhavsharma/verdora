'use client';

import React, { FC, useEffect, useState } from 'react';
import ProductList from '../components/ProductList';

export interface Product {
    id: number;
    name: string;
    price: string; // Since the API returns price as a string
    image?: string; // Optional if no image is provided
}

const HomePage: FC = () => {
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/getAllItems', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
                if (!response.ok) {
                    throw new Error('Failed to fetch products');
                }
                const data: Product[] = await response.json();
                const formattedProducts = data.map((item) => ({
                    ...item,
                }));
                setProducts(formattedProducts);
            } catch (error) {
                console.error('Error fetching products:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }, []);

    return (
        <main className="home-container">
            <h2 className="welcome-text">Welcome to the Marketplace!</h2>
            {loading ? (
                <p className="text-center">Loading products...</p>
            ) : (
                <ProductList products={products} />
            )}
        </main>
    );
};

export default HomePage;
