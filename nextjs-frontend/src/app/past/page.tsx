const pastEntries = [
  {
    date: 'July 23, 2025',
    dateTime: '2025-07-23',
    summary: 'Today\'s reflections on the human experience',
    preview: 'Connection and community remain fundamental to human well-being...',
    href: '/today',
  },
  {
    date: 'July 22, 2025', 
    dateTime: '2025-07-22',
    summary: 'Moments of quiet contemplation',
    preview: 'In the stillness of morning, we find clarity and purpose...',
    href: '#',
  },
  {
    date: 'July 21, 2025',
    dateTime: '2025-07-21', 
    summary: 'The art of human resilience',
    preview: 'Through adversity, we discover strength we never knew existed...',
    href: '#',
  },
  {
    date: 'July 20, 2025',
    dateTime: '2025-07-20',
    summary: 'Digital connections, human hearts',
    preview: 'Technology bridges distances but cannot replace presence...',
    href: '#',
  },
  {
    date: 'July 19, 2025',
    dateTime: '2025-07-19',
    summary: 'The rhythm of everyday kindness',
    preview: 'Small gestures create ripples that reach farther than we imagine...',
    href: '#',
  },
  {
    date: 'July 18, 2025',
    dateTime: '2025-07-18',
    summary: 'Learning from our collective past',
    preview: 'History teaches us that hope persists through the darkest times...',
    href: '#',
  },
]

export default function Past() {
  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">Past Reflections</h1>
      
      <ul
        role="list"
        className="divide-y divide-gray-100 overflow-hidden bg-white dark:bg-gray-900 shadow-xs ring-1 ring-gray-900/5 dark:ring-gray-100/5 sm:rounded-xl"
      >
        {pastEntries.map((entry) => (
          <li key={entry.dateTime} className="relative flex justify-between gap-x-6 px-4 py-5 hover:bg-gray-50 dark:hover:bg-gray-800 sm:px-6">
            <div className="flex min-w-0 gap-x-4">
              <div className="size-12 flex-none rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
                <span className="text-xs font-semibold text-gray-600 dark:text-gray-300">
                  {new Date(entry.dateTime).getDate()}
                </span>
              </div>
              <div className="min-w-0 flex-auto">
                <p className="text-sm/6 font-semibold text-gray-900 dark:text-gray-100">
                  <a href={entry.href}>
                    <span className="absolute inset-x-0 -top-px bottom-0" />
                    {entry.summary}
                  </a>
                </p>
                <p className="mt-1 text-xs/5 text-gray-500 dark:text-gray-400 truncate">
                  {entry.preview}
                </p>
              </div>
            </div>
            <div className="flex shrink-0 items-center gap-x-4">
              <div className="hidden sm:flex sm:flex-col sm:items-end">
                <p className="text-sm/6 text-gray-900 dark:text-gray-100">{entry.date}</p>
              </div>
              <svg className="size-5 flex-none text-gray-400" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
              </svg>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}