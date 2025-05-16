const eventDetails = {
  'event-1': {
    title: 'React Conference 2025',
    date: 'June 10, 2025',
    location: 'San Francisco, CA',
    description: 'Join us for a day of React insights and networking.',
    agenda: [
      'Keynote by React Core Team',
      'React Hooks Deep Dive',
      'Building Scalable Applications',
    ],
  },
  'event-2': {
    title: 'Node.js Summit',
    date: 'July 15, 2025',
    location: 'New York, NY',
    description: 'Deep dive into Node.js and backend development.',
    agenda: [
      'Node.js Performance Tuning',
      'Microservices Architecture',
      'Security Best Practices',
    ],
  },
};

export default async function EventDetails({ params }) {
  const { id } = await params;

  const event = eventDetails[id];

  if (!event) {
    return <p className="p-6">Event not found.</p>;
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-2">{event.title}</h1>
      <p className="text-gray-600">{event.date} | {event.location}</p>
      <p className="mt-4">{event.description}</p>
      <h2 className="text-xl font-semibold mt-6">Agenda</h2>
      <ul className="list-disc list-inside mt-2">
        {event.agenda.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
