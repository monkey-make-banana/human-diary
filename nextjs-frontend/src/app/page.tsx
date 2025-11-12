import { getDiaryEntries } from '@/data/diaryEntries'
import { Link } from '@/app/components/ui-kit/link'
import { Divider } from './components/ui-kit/divider'
import { Heading } from './components/ui-kit/heading'
import { Pagination, PaginationGap, PaginationList, PaginationNext, PaginationPage, PaginationPrevious } from './components/ui-kit/pagination'
import { Table, TableBody, TableCell, TableRow } from './components/ui-kit/table'

const diaryEntries = getDiaryEntries()

const longDateFormatter = new Intl.DateTimeFormat('en-US', {
  weekday: 'long',
  month: 'long',
  day: 'numeric',
  year: 'numeric',
})

const asUTCDate = (isoDate: string) => new Date(`${isoDate}T00:00:00Z`)

const PAGE_SIZE = 5

type HomeProps = {
  searchParams?: Promise<Record<string, string | string[] | undefined>>
}

const getPaginationRange = (currentPage: number, totalPages: number) => {
  if (totalPages <= 5) {
    return Array.from({ length: totalPages }, (_, index) => index + 1)
  }

  const pages: Array<number | 'gap'> = [1]

  if (currentPage > 3) {
    pages.push('gap')
  }

  const start = Math.max(2, currentPage - 1)
  const end = Math.min(totalPages - 1, currentPage + 1)

  for (let page = start; page <= end; page++) {
    pages.push(page)
  }

  if (currentPage < totalPages - 2) {
    pages.push('gap')
  }

  pages.push(totalPages)

  return pages
}

export default async function Home({ searchParams }: HomeProps) {
  const resolvedSearchParams = (await searchParams) ?? {}
  const requestedPage =
    Number(Array.isArray(resolvedSearchParams.page) ? resolvedSearchParams.page[0] : resolvedSearchParams.page) || 1
  const totalPages = Math.max(1, Math.ceil(diaryEntries.length / PAGE_SIZE))
  const currentPage = Math.min(Math.max(requestedPage, 1), totalPages)
  const startIndex = (currentPage - 1) * PAGE_SIZE
  const currentEntries = diaryEntries.slice(startIndex, startIndex + PAGE_SIZE)
  const paginationRange = getPaginationRange(currentPage, totalPages)

  return (
    <div className="flex h-full flex-col justify-center gap-12 py-10">
      <section className="mx-auto max-w-3xl space-y-6 text-center">
        <Heading className="text-center">Dear Diary,</Heading>
        <p className="text-lg leading-relaxed text-zinc-700 dark:text-zinc-200">
          I’m sorry I’ve been so quiet. It’s not that nothing is happening—it’s that too much is. The world moves faster
          than I can write: wars and peace, breakthroughs and blackouts, kindness and chaos, all in a single day. I can’t
          keep up alone anymore.
        </p>
        <p className="text-lg leading-relaxed text-zinc-700 dark:text-zinc-200">
          <Link
            href="/what"
            className="inline-flex items-center gap-2 rounded-lg bg-zinc-100/70 px-3 py-1 font-semibold text-zinc-900 underline decoration-2 underline-offset-4 transition hover:bg-zinc-200 dark:bg-white/10 dark:text-white dark:hover:bg-white/20"
          >
            <span>So I’ve asked a small team of AIs to help.</span>
            <svg
              viewBox="0 0 20 20"
              className="h-4 w-4 stroke-current"
              fill="none"
              aria-hidden="true"
            >
              <path
                d="M11 4L16 4M16 4L16 9M16 4L9 11"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <path
                d="M9 4H6C4.34315 4 3 5.34315 3 7V14C3 15.6569 4.34315 17 6 17H13C14.6569 17 16 15.6569 16 14V11"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </Link>{' '}
          Some fetch the news from around the globe, some weave it into a story, some critique and question, and some
          quietly check the facts. Together, they’ll write my entries for a while. I don’t know when I’ll be back, but
          until then—stay safe.
        </p>
        <Heading className="text-center" level={2}>
          Sincerely, Humanity
        </Heading>
      </section>

      <Divider soft />

      <section className="mx-auto w-full max-w-3xl space-y-6">
        <Table striped className="w-full">
          <TableBody>
            {currentEntries.map((entry) => {
              const dateValue = asUTCDate(entry.date)
              const longLabel = longDateFormatter.format(dateValue)

              return (
                <TableRow key={entry.date} href={`/${entry.date}`} title={`${entry.title} — ${longLabel}`}>
                  <TableCell className="max-w-xl">
                    <p className="text-base font-semibold text-zinc-950 dark:text-white">{entry.title}</p>
                  </TableCell>
                  <TableCell className="text-right sm:w-32">
                    <p className="text-sm font-semibold uppercase tracking-[0.2em] text-zinc-500 dark:text-zinc-400">
                      {longLabel}
                    </p>
                  </TableCell>
                </TableRow>
              )
            })}
          </TableBody>
        </Table>

        {totalPages > 1 && (
          <Pagination className="items-center">
            <PaginationPrevious href={currentPage > 1 ? `/?page=${currentPage - 1}` : null} />
            <PaginationList>
              {paginationRange.map((page, index) =>
                page === 'gap' ? (
                  <PaginationGap key={`gap-${index}`} />
                ) : (
                  <PaginationPage key={page} href={`/?page=${page}`} current={page === currentPage}>
                    {page}
                  </PaginationPage>
                )
              )}
            </PaginationList>
            <PaginationNext href={currentPage < totalPages ? `/?page=${currentPage + 1}` : null} />
          </Pagination>
        )}
      </section>
    </div>
  )
}
