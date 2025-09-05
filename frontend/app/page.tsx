'use client'

import { useState } from 'react'

export default function Home() {
  const [token, setToken] = useState<string>('');
  const [products, setProducts] = useState<any[]>([]);
  const [cart, setCart] = useState<any[]>([]);

  async function login() {
    const res = await fetch('http://localhost:8001/auth/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: 'user-1', email: 'user@example.com' })
    });
    const data = await res.json();
    setToken(data.access_token);
  }

  async function loadProducts() {
    const res = await fetch('http://localhost:8003/products');
    const data = await res.json();
    setProducts(data.items || []);
  }

  async function addToCart(sku: string) {
    await fetch('http://localhost:8002/cart', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ sku, qty: 1 })
    });
    await loadCart();
  }

  async function loadCart() {
    const res = await fetch('http://localhost:8002/cart', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const data = await res.json();
    setCart(data.items || []);
  }

  async function checkout() {
    const res = await fetch('http://localhost:8005/orders', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ items: cart })
    });
    const order = await res.json();
    alert(`Order ${order.order_id} total $${order.total}`);
  }

  return (
    <div>
      <h1>E-Commerce Demo</h1>
      <div style={{ display: 'flex', gap: 16 }}>
        <button onClick={login}>Login</button>
        <button onClick={loadProducts}>Load Products</button>
        <button onClick={loadCart} disabled={!token}>Load Cart</button>
        <button onClick={checkout} disabled={!token || cart.length === 0}>Checkout</button>
      </div>
      <p>Token: {token ? token.slice(0, 16) + '...' : 'not logged in'}</p>
      <h2>Products</h2>
      <ul>
        {products.map(p => (
          <li key={p.sku}>
            {p.name} - ${p.price} <button onClick={() => addToCart(p.sku)} disabled={!token}>Add</button>
          </li>
        ))}
      </ul>
      <h2>Cart</h2>
      <ul>
        {cart.map((c, idx) => (
          <li key={idx}>{c.sku} x {c.qty}</li>
        ))}
      </ul>
    </div>
  );
}

