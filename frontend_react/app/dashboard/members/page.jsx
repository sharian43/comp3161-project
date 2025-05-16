"use client";

import { useState, useEffect } from "react";
import { Select } from "flowbite-react";

export default function MembersPage() {
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState("");
  const [members, setMembers] = useState([]);
  const [loadingCourses, setLoadingCourses] = useState(true);
  const [loadingMembers, setLoadingMembers] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCourses = async () => {
      const token = localStorage.getItem("token")
      try {
        const response = await fetch("/courses/retrieve-courses", {
          method: "GET",
          "Authorization": `Bearer ${token}`,
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        });
        if (!response.ok) {
          console.log(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setCourses(data.allCourses);
        if (data.allCourses.length > 0) {
          setSelectedCourse(data.allCourses[0].id);
        }
      } catch (err) {
        console.error("Error fetching members:", err);
        setError("Failed to load members.");
      } finally {
        setLoadingCourses(false);
      }
    };

    fetchCourses();
  }, []);

  useEffect(() => {
    if (!selectedCourse) return;

    const fetchMembers = async () => {
      setLoadingMembers(true);
      try {
        const response = await fetch(`/courses/${selectedCourse}/members`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        });
        if (!response.ok) {
          console.log(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setMembers(data.members);
      } catch (err) {
        console.error("Error fetching members:", err);
        setError("Failed to load members.");
        setMembers([]);
      } finally {
        setLoadingMembers(false);
      }
    };

    fetchMembers();
  }, [selectedCourse]);

  if (loadingCourses) {
    return <p>Loading members...</p>;
  }

  if (error) {
    return <p className="text-red-500">{error}</p>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Members</h1>

      <div className="mb-6">
        <label htmlFor="course-select" className="block mb-2 font-medium">
          Select Course
        </label>
        <Select
          id="course-select"
          value={selectedCourse}
          onChange={(e) => setSelectedCourse(e.target.value)}
        >
          {courses.map((course) => (
            <option key={course.courseID} value={course.courseID}>
              {course.name}
            </option>
          ))}
        </Select>
      </div>

      {loadingMembers ? (
        <p>Loading members...</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left text-gray-700">
            <thead className="text-xs uppercase bg-gray-200">
              <tr>
                <th className="px-4 py-2">#</th>
                <th className="px-4 py-2">First Name</th>
                <th className="px-4 py-2">Last Name</th>
                <th className="px-4 py-2">Role</th>
              </tr>
            </thead>
            <tbody>
              {members.length > 0 ? (
                members.map((member, idx) => (
                  <tr key={member.id} className="bg-white border-b">
                    <td className="px-4 py-2">{idx + 1}</td>
                    <td className="px-4 py-2">{member.firstName}</td>
                    <td className="px-4 py-2">{member.lastName}</td>
                    <td className="px-4 py-2">{member.accRole}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td
                    colSpan={4}
                    className="px-4 py-6 text-center text-gray-500"
                  >
                    No members found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
