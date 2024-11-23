import { AuthForm } from '@/components/auth-form'
import Navbar from '@/components/ui/navbar'
import { Fragment } from 'react'

export default function AuthPage() {
  return (
    <Fragment>
      <Navbar />
      <div className="min-h-screen flex items-center justify-center bg-[#bacbb3]">
        <AuthForm />
      </div>
    </Fragment>
  )
}

