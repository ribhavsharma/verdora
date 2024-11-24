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
    return (
        <div className="product-card">
            {/* <Link to={`/product/${product.id}`} className="product-link"> */}
                <img src={ProductImage.src} alt={product.name} />
                <h3>{product.name}</h3>
                <p>${product.price}</p>
            {/* </Link>  */}
            <button>Add to Cart</button>
        </div>
    );
};

export default ProductCard;