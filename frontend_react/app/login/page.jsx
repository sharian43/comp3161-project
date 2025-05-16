'use client'

import { useState } from 'react'
import { Button, Label, TextInput } from 'flowbite-react'
import Link from 'next/link'

export default function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    try {
      const response = await fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: 'include',
        body: JSON.stringify({username, userPassword: password}),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      console.log(response)
      if (response.token) {
        localStorage.setItem("token", response.token)
      }
      router.push("/dashboard");
    } catch (e) {
      console.log(e);
    }
    console.log({ username, password })
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md bg-white p-8 rounded-lg shadow"
      >
        <h2 className="text-2xl font-semibold mb-6">Login</h2>

        <div className="mb-4">
          <Label htmlFor="username" value="Username" />                
          <TextInput
            id="username"
            type="text"
            required
            placeholder="Enter your username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />                                                          
        </div>

        <div className="mb-6">
          <Label htmlFor="password" value="Password" />               
          <TextInput
            id="password"
            type="password"
            required
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />                                                         
        </div>

        <Button type="submit" className="w-full">Login</Button>       

        <p className="mt-4 text-center text-sm text-gray-600">
          Don&apos;t have an account?{' '}
          <Link href="/signup" className="text-blue-600 hover:underline">
            Sign Up
          </Link>
        </p>
      </form>
    </div>
  )
}
