'use client'

import { Sidebar, SidebarItems, SidebarItemGroup, SidebarItem } from 'flowbite-react'
import {
  HiBookOpen,
  HiUsers,
  HiChatAlt2,
  HiCalendar,
} from 'react-icons/hi'

export default function DashboardLayout({ children }) {
  return (
    <div className="flex min-h-screen bg-gray-100">
      <Sidebar className='min-h-screen' aria-label="Dashboard sidebar">
        <SidebarItems className='flex-1 min-h-screen'>
          <SidebarItemGroup>
            <SidebarItem className='mb-10 text-center font-bold'>
              COMP 3161
            </SidebarItem>
            <SidebarItem href="/dashboard/courses" icon={HiBookOpen}>
              Courses
            </SidebarItem>
            <SidebarItem href="/dashboard/members" icon={HiUsers}>
              Members
            </SidebarItem>
            <SidebarItem href="/dashboard/forums" icon={HiChatAlt2}>
              Forums
            </SidebarItem>
            <SidebarItem href="/dashboard/events" icon={HiCalendar}>
              Events
            </SidebarItem>
          </SidebarItemGroup>
        </SidebarItems>
      </Sidebar>

      <main className="flex-1 p-6">
        {children}
      </main>
    </div>
  )
}
