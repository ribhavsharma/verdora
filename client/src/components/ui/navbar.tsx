"use client";

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { FaBell } from 'react-icons/fa'; // Install react-icons if not already installed

const Navbar = () => {
    const [isSignedIn, setIsSignedIn] = useState(false);

    useEffect(() => {
      const signedIn = localStorage.getItem("auth");
      if (signedIn) {
        setIsSignedIn(true);
      }
    }, []);

    const logOut  = () =>{
      localStorage.removeItem("auth");
      localStorage.removeItem("user");
      window.location.href = "/auth";
    }

    return (
      <nav style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px', borderBottom: '1px solid #ccc' }}>
      {/* Left: Bell Icon */}
      <div className='ml-5'>
        <FaBell size={24} />
      </div>

      {/* Right: Links */}
      <div style={{ display: 'flex', gap: '20px' }}>
        {isSignedIn ?
          <Link href="/">Home</Link>
          :
          <Link href="/">Home</Link>
        }

        {isSignedIn ?
          <span className="cursor-pointer" onClick={logOut}>Sign Out</span>
          :
          <Link href="/auth">Sign In</Link>
        }
      </div>
    </nav>
    );
  };

export default Navbar;