"use client";

import { useState } from "react";
import { Button, Label, TextInput, Select } from "flowbite-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function SignUpPage() {
  const [form, setForm] = useState({
    username: "",
    password: "",
    firstName: "",
    lastName: "",
    acc_contact_info: "",
    accRole: "student",
    department: '',
  });
  const router = useRouter();

  function handleChange(e) {
    setForm({ ...form, [e.target.id]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const response = await fetch("/register/account", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      console.log(response)
      router.push("/login");
    } catch (e) {
      console.log(e);
    }
    // console.log(form);
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-lg bg-white p-8 rounded-lg shadow"
      >
        <h2 className="text-2xl font-semibold mb-6">Sign Up</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <Label htmlFor="firstName" value="First Name" />
            <TextInput
              id="firstName"
              type="text"
              required
              placeholder="First Name"
              value={form.firstName}
              onChange={handleChange}
            />
          </div>
          <div>
            <Label htmlFor="lastName" value="Last Name" />
            <TextInput
              id="lastName"
              type="text"
              required
              placeholder="Last Name"
              value={form.lastName}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="mt-4">
          <Label htmlFor="username" value="Username" />
          <TextInput
            id="username"
            type="text"
            required
            placeholder="Choose a username"
            value={form.username}
            onChange={handleChange}
          />
        </div>

        <div className="mt-4">
          <Label htmlFor="password" value="Password" />
          <TextInput
            id="password"
            type="password"
            required
            placeholder="Enter your password"
            value={form.password}
            onChange={handleChange}
          />
        </div>

        <div className="mt-4">
          <Label htmlFor="acc_contact_info" value="Contact Info" />
          <TextInput
            id="acc_contact_info"
            type="text"
            required
            placeholder="email or phone"
            value={form.acc_contact_info}
            onChange={handleChange}
          />
        </div>

        <div className="mt-4">
          <Label htmlFor="accRole" value="Account Role" />
          <Select
            id="accRole"
            required
            value={form.accRole}
            onChange={handleChange}
          >
            <option value="student">Student</option>
            <option value="teacher">Teacher</option>
          </Select>
        </div>

        <div className="mt-4">
          <Label htmlFor="department" value="Department" />
          <TextInput
            id="department"
            type="text"
            required
            placeholder="Department"
            value={form.department}
            onChange={handleChange}
          />
        </div>

        <Button type="submit" className="w-full mt-6">
          Create Account
        </Button>

        <p className="mt-4 text-center text-sm text-gray-600">
          Already have an account?{" "}
          <Link href="/login" className="text-blue-600 hover:underline">
            Login
          </Link>
        </p>
      </form>
    </div>
  );
}
