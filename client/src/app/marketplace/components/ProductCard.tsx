import React, { FC } from 'react';
import { Link } from 'react-router-dom';
import './ProductCard.css';
import '../pages/HomePage';
import { Product } from '../pages/HomePage';
import ProductImage from './images/IMG_1259.jpeg';

interface ProductCardProps {
    product: Product;
}

const ProductCard: FC<ProductCardProps> = ({ product }) => {

    const itemsPage  = () =>{
        window.location.href = "/marketplace/13";
    }

    return (
        <div 
        className="product-card" 
        onClick={itemsPage}>
                <img src={ProductImage.src} alt={product.name} />
                <h3>{product.name}</h3>
                <p>${product.price}</p>
            <button onClick={itemsPage}>View Item</button>
        </div>
    );
};

export default ProductCard;