import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import { getDiaryEntries, getDiaryEntryByDate } from '@/data/diaryEntries'
import { Divider } from '@/app/components/ui-kit/divider'
import { Heading } from '@/app/components/ui-kit/heading'
import { Link } from '@/app/components/ui-kit/link'

const longDateFormatter = new Intl.DateTimeFormat('en-US', {
  weekday: 'long',
  month: 'long',
  day: 'numeric',
  year: 'numeric',
})

const asUTCDate = (isoDate: string) => new Date(`${isoDate}T00:00:00Z`)

type PageProps = {
  params: Promise<{
    date: string
  }>
}

export function generateStaticParams() {
  return getDiaryEntries().map((entry) => ({ date: entry.date }))
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { date } = await params
  const entry = getDiaryEntryByDate(date)
  if (!entry) {
    return {
      title: 'Entry not found',
    }
  }

  const longLabel = longDateFormatter.format(asUTCDate(entry.date))

  return {
    title: `${entry.title} — ${longLabel}`,
  }
}

export default async function DiaryEntryPage({ params }: PageProps) {
  const { date } = await params
  const entry = getDiaryEntryByDate(date)

  if (!entry) {
    notFound()
  }

  const dateValue = asUTCDate(entry.date)
  const longLabel = longDateFormatter.format(dateValue)

  return (
    <article className="mx-auto flex h-full max-w-4xl flex-col gap-10 py-10">
      <Link
        href="/"
        className="inline-flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-zinc-500 transition hover:text-zinc-200 dark:text-zinc-400 dark:hover:text-white"
        aria-label="Back to diary home"
      >
        <span aria-hidden="true">←</span>
        Back to entries
      </Link>

      <div className="space-y-4 text-center">
        <Heading className="text-4xl sm:text-5xl">{entry.title}</Heading>
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-zinc-500 dark:text-zinc-400">
          {longLabel}
        </p>
      </div>

      <Divider soft />

      <section className="space-y-6 text-left">
        {entry.body.map((paragraph, index) => (
          <p key={paragraph.slice(0, 12) + index} className="text-lg leading-relaxed text-zinc-700 dark:text-zinc-200">
            {paragraph}
          </p>
        ))}
      </section>
    </article>
  )
}
