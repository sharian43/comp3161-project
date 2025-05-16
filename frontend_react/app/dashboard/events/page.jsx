import Link from 'next/link';

const events = [
  {
    id: 'event-1',
    title: 'React Conference 2025',
    date: 'June 10, 2025',
    location: 'San Francisco, CA',
    description: 'Join us for a day of React insights and networking.',
  },
  {
    id: 'event-2',
    title: 'Node.js Summit',
    date: 'July 15, 2025',
    location: 'New York, NY',
    description: 'Deep dive into Node.js and backend development.',
  },
];

export default function EventsPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Upcoming Events</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {events.map((event) => (
          <Link
            key={event.id}
            href={`/dashboard/events/${event.id}`}
            className="block p-4 border border-gray-200 rounded hover:bg-gray-100 transition"
          >
            <h2 className="text-lg font-semibold">{event.title}</h2>
            <p className="text-sm text-gray-600">{event.date} | {event.location}</p>
            <p className="mt-2 text-gray-700">{event.description}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
