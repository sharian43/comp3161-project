import Link from "next/link";

const forumThreads = [
  { id: "nextjs-routing", title: "Understanding Next.js Routing" },
  { id: "tailwind-tips", title: "Tailwind CSS Tips and Tricks" },
  {
    id: "deployment-strategies",
    title: "Deployment Strategies for Next.js Apps",
  },
];

export default function ForumPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Forum Threads</h1>
      <ul className="space-y-4">
        {forumThreads.map((thread) => (
          <li key={thread.id}>
            <Link href={`/dashboard/forums/${thread.id}`}>
              <div className="block p-4 border border-gray-200 rounded hover:bg-gray-100 transition">
                <h2 className="text-lg font-semibold">{thread.title}</h2>
                <p className="text-sm text-gray-600">
                  Click to view the discussion
                </p>
              </div>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
