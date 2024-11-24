"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Bell, Menu, LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";

const Navbar = () => {
  const [isSignedIn, setIsSignedIn] = useState(false);
  const [user, setUser] = useState<string | null>(null);

  useEffect(() => {
    const signedIn = localStorage.getItem("auth");
    const userData = localStorage.getItem("user");
    if (signedIn && userData) { 
      setIsSignedIn(true);
      setUser(userData);
    }
  }, []);

  const logOut = () => {
    localStorage.removeItem("auth");
    localStorage.removeItem("user");
    window.location.href = "/auth";
  };

  const NavLinks = () => (
    <>
      <Link href="/classify" className="text-[#87c38f] md:text-[#f4f0bb] hover:text-[#87c38f] transition-colors">
        Home
      </Link>
      <Link href="/about" className="text-[#87c38f] md:text-[#f4f0bb] hover:text-[#87c38f] transition-colors">
        About
      </Link>
      <Link href="/contact" className="text-[#87c38f] md:text-[#f4f0bb] hover:text-[#87c38f] transition-colors">
        Contact
      </Link>
    </>
  );

  return (
    <nav className="bg-[#226f54] shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex-shrink-0">
            <Link href="/" className="text-2xl font-bold text-[#f4f0bb] hover:text-[#87c38f] transition-colors">
              verdora
            </Link>
          </div>
          <div className="hidden md:flex items-center space-x-4">
            <NavLinks />
            <Button variant="ghost" size="icon" className="text-[#f4f0bb] hover:text-[#87c38f] hover:bg-[#226f54]">
              <Bell className="h-5 w-5" />
            </Button>
            {isSignedIn ? (
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                    <Avatar className="h-8 w-8">
                    {user && <AvatarImage src={`https://api.dicebear.com/6.x/initials/svg?seed=${user}`} alt={user} />}
                      <AvatarFallback>{user??"".charAt(0)}</AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-56" align="end" forceMount>
                  <DropdownMenuItem className="cursor-pointer" onSelect={logOut}>
                    Log out
                  </DropdownMenuItem>
                  <DropdownMenuItem asChild>
                    <Link href="/profile">Profile</Link>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            ) : (
              <Button asChild variant="ghost" className="text-[#f4f0bb] hover:text-[#87c38f] hover:bg-[#226f54]">
                <Link href="/auth">Sign In</Link>
              </Button>
            )}
          </div>
          <div className="md:hidden">
            <Sheet>
              <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="text-[#f4f0bb] hover:text-[#87c38f] hover:bg-[#226f54]">
                  <Menu className="h-5 w-5" />
                  <span className="sr-only">Toggle menu</span>
                </Button>
              </SheetTrigger>
              <SheetContent side="right" className="w-[300px] sm:w-[400px] bg-white">
                <nav className="flex flex-col space-y-4">
                  <NavLinks />
                  <Button variant="ghost" size="sm" className="justify-start text-[#87c38f] md:text-[#f4f0bb] hover:text-[#87c38f] hover:bg-[#226f54]">
                    <Bell className="h-5 w-5 mr-2" />
                    Notifications
                  </Button>
                  {isSignedIn ? (
                    <Button variant="ghost" size="sm" className="justify-start text-[#87c38f] md:text-[#f4f0bb] hover:text-[#87c38f] hover:bg-[#226f54]" onClick={logOut}>
                      <LogOut className="h-5 w-5 mr-2" />
                      Log out
                    </Button>
                  ) : (
                    <Button asChild variant="ghost" size="sm" className="justify-start text-[#f4f0bb] hover:text-[#87c38f] hover:bg-[#226f54]">
                      <Link href="/auth">Sign In</Link>
                    </Button>
                  )}
                </nav>
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

