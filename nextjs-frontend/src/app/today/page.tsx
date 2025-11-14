import Image from "next/image";

export default function Today() {
  const today = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <div className="space-y-8">
        {/* Date */}
        <h1 className="text-2xl font-bold">{today}</h1>
        
        {/* Image space */}
        <div className="rounded-lg overflow-hidden">
          <Image
            src="/today.png"
            alt="Today&apos;s image"
            width={400}
            height={128}
          />
        </div>
        
        {/* Heading sentence */}
        <h2 className="text-xl font-semibold">Today&apos;s reflections on the human experience</h2>
        
        {/* Ten bullet points */}
        <ul className="space-y-3 text-lg">
          <li>• Connection and community remain fundamental to human well-being</li>
          <li>• Small acts of kindness ripple outward in unexpected ways</li>
          <li>• Technology continues to reshape how we relate to one another</li>
          <li>• The search for meaning transcends cultural and generational boundaries</li>
          <li>• Resilience emerges from facing challenges together</li>
          <li>• Creative expression serves as a universal language</li>
          <li>• The pace of change tests our adaptability daily</li>
          <li>• Moments of stillness become increasingly precious</li>
          <li>• Empathy bridges the gaps between different perspectives</li>
          <li>• Hope persists even in the face of uncertainty</li>
        </ul>
      </div>
    </div>
  );
}
