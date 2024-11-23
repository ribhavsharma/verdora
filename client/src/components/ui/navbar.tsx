import Link from 'next/link';
import { FaBell } from 'react-icons/fa'; // Install react-icons if not already installed

const Navbar = () => (
    <nav style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px', borderBottom: '1px solid #ccc' }}>
    {/* Left: Bell Icon */}
    <div className='ml-5'>
      <FaBell size={24} />
    </div>

    {/* Right: Links */}
    <div style={{ display: 'flex', gap: '20px' }}>
      <Link href="/">Home</Link>
      <Link href="/about">About</Link>
      <Link href="/contact">Contact</Link>
    </div>
  </nav>
);

export default Navbar;