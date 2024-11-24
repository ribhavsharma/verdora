import React, { FC } from 'react';
import ProductCard from './ProductCard';
import './ProductList.css';
import Product from '../pages/HomePage';

interface ProductListProps {
  products: Product[];
}

const ProductList: FC<ProductListProps> = ({ products }) => {
    if (!products || products.length === 0) {
        return <h2>No Products Available</h2>;
    }
    
    return (
        <div className="product-list">
          {products.map((product) => (
            <ProductCard key={product.id}  product={product} />
          ))}
        </div>
    );
};

export default ProductList;