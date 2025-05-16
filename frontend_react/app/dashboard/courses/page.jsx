"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

export default function CoursesPage() {
  const [allCourses, setAllCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token")
    const fetchCourses = async () => {
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
        setAllCourses(data.allCourses);
      } catch (error) {
        console.error("Error fetching courses:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  if (loading) {
    return <p>Loading courses...</p>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Courses</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
        {allCourses.map((course) => (
          <Link
            key={course.courseID}
            href={`/dashboard/courses/${course.id}`}
            className="block p-4 border border-gray-200 rounded-lg hover:bg-gray-100 transition"
          >
            <h2 className="text-lg font-semibold">{course.course_name}</h2>
            <p className="text-sm text-gray-600 mt-1">
              Click to view more details
            </p>
          </Link>
        ))}
      </div>
    </div>
  );
}
