// app/layout.js   ← (server component by default)
import { Inter, Roboto_Mono } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })
const robotoMono = Roboto_Mono({ subsets: ['latin'] })

export const metadata = {
  title: 'My App',
  description: '…',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        suppressHydrationWarning
        className={`${inter.className} ${robotoMono.className} antialiased`}
      >
        {children}
      </body>
    </html>
  )
}