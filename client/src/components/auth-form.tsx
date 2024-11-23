'use client'

import { useEffect, useState } from 'react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import Link from 'next/link'

export function AuthForm() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [page, setPage] = useState(0)  // 0 for login 1 for sign up

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // Here you would typically handle the authentication logic
    console.log('Login attempted with:', { username, password })
  }

  useEffect(() => {
    const hash = window.location.hash; // Get the hash
    if(hash=="#SignUp"){
      setPage(1)
    }
  }, []);

  const changePage  = (pageNum: number) => {
    setPage(pageNum);
  };

  return (
    <Card className="w-full max-w-md bg-white shadow-lg">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl font-bold text-center text-[#43291F]">
            {
              page == 0 ? 
              "Login" : "Sign Up"
            }
        </CardTitle>
        <CardDescription className="text-center text-[#43291F]/80">
          Enter your username and password to access your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="username" className="text-[#43291F]">Username</Label>
            <Input 
              id="username" 
              placeholder="Enter your username" 
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required 
              className="border-[#87C38F] focus:border-[#226F54] focus:ring-[#226F54] text-[#43291F]"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password" className="text-[#43291F]">Password</Label>
            <Input 
              id="password" 
              type="password" 
              placeholder="Enter your password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required 
              className="border-[#87C38F] focus:border-[#226F54] focus:ring-[#226F54] text-[#43291F]"
            />
          </div>
        </form>
      </CardContent>
      <CardFooter>
        <Button 
          type="submit" 
          className="w-full bg-[#226F54] hover:bg-[#87C38F] text-white"
          onClick={handleSubmit}
        >
          {
            page == 0 ? 
              "Sign In" : "Sign Up"
          }
        </Button>
      </CardFooter>
      <div className='w-[100%] text-center mb-5'>
        <Link className='text-sm text-center text-[#43291F]/80' href={page==0 ? "#SignUp" : ""}
          onClick={() => changePage(page==0 ? 1 : 0)}
        >
        {
            page == 0 ? 
              "Don't have an account yet? Sign up" : "Already have an account? Sign In"
          }
        </Link>
      </div>
    </Card>
  )
}

