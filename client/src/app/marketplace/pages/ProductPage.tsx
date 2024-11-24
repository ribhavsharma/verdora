import React, { FC } from 'react';
import { useParams } from 'react-router-dom';
import './ProductPage.css';
import './HomePage';
import { Product } from './HomePage';

const mockProducts: Product[] = [
  { id: 1, name: 'Product 1', price: 20, image: '/images/product1.jpg' },
  { id: 2, name: 'Product 2', price: 35, image: '/images/product2.jpg' },
  { id: 3, name: 'Product 3', price: 50, image: '/images/product3.jpg' },
];

const ProductPage: FC = () => {
  const { id } = useParams<{ id: string }>();
  const product: Product | undefined = mockProducts.find((p) => p.id === parseInt(id ?? "1"));

  if (!product) {
    return <h2>Product not found</h2>;
  }

  return (
    <>
      <div className="product-page">
        <img src={product.image} alt={product.name} />
        <h1>{product.name}</h1>
        <p>Price: ${product.price}</p>
        <button>View Item</button>
      </div>

    </>
  );
};

export default ProductPage;