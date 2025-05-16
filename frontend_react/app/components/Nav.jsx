'use client'

import { Navbar, NavbarBrand, NavbarToggle } from 'flowbite-react'
import { Button } from 'flowbite-react'
import Link from 'next/link'

export function Nav() {
  return (
    <Navbar fluid rounded>                                                
      <NavbarBrand as={Link} href="/">
        <span className="self-center whitespace-nowrap text-xl font-semibold">
          COMP3161
        </span>
      </NavbarBrand>                                                      
      <div className="flex md:order-2">                                    
        <Button as={Link} href="/signup" outline size="md">Sign Up</Button> 
        <Button as={Link} href="/login" className="ml-2" size="md">Login</Button> 
        <NavbarToggle />                                                    
      </div>
    </Navbar>
  )
}
