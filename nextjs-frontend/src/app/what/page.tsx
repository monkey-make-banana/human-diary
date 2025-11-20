import { Divider } from '@/app/components/ui-kit/divider'
import { Heading, Subheading } from '@/app/components/ui-kit/heading'
import { Link } from '@/app/components/ui-kit/link'

const references = [
  {
    key: 'Lu2024',
    label: 'Lu et al., “The AI Scientist,” arXiv:2408.06292 (2024)',
    url: 'https://arxiv.org/abs/2408.06292',
  },
  {
    key: 'Yamada2025',
    label: 'Yamada et al., “AI Scientist-v2,” arXiv:2504.08066 (2025)',
    url: 'https://arxiv.org/abs/2504.08066',
  },
  {
    key: 'Villaescusa2025',
    label: 'Villaescusa-Navarro et al., “Denario Project,” arXiv:2510.26887 (2025)',
    url: 'https://arxiv.org/abs/2510.26887',
  },
  {
    key: 'Jiang2025',
    label: 'Jiang et al., “BadScientist,” arXiv:2510.18003 (2025)',
    url: 'https://arxiv.org/abs/2510.18003',
  },
  {
    key: 'Silva2025',
    label: 'Silva et al., “AI-Assisted Tools for Scientific Review Writing,” ACS Appl. Mater. Interfaces 17 (34) (2025)',
    url: 'https://doi.org/10.1021/acsami.5c08837',
  },
]

export default function WhatPage() {
  return (
    <article className="mx-auto flex h-full max-w-5xl flex-col gap-10 py-10">
      <Link
        href="/"
        className="mx-auto inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.3em] text-zinc-500 transition hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-white"
      >
        <span aria-hidden="true">←</span>
        Back to diary
      </Link>
      <header className="space-y-4 text-center">
        <Heading className="text-3xl sm:text-4xl">How the diary writes itself</Heading>
        <p className=" leading-relaxed text-zinc-700 dark:text-zinc-200 sm:text-lg">
          Humanity’s Diary runs like a compact AI newsroom built on agent orchestration. A{' '}
          <strong className="font-semibold text-zinc-900 dark:text-white">planner–reviewer loop</strong> balances regions
          and themes, then hands a slate to retrieval, analysis, and writing teams. Retriever → cleaner → cluster agents
          sweep sources, normalize provenance, and dedupe before grouping stories by theme. Sense-making agents convert
          those clusters into concise bullets with impact/uncertainty signals so downstream writers inherit both facts
          and why they matter. Draft → critic → revision chains produce the narrative; multiple variants are scored for
          factuality, balance, and narrative quality, and a selector picks or merges the best. Publish + memory agents
          export the entry, capture feedback, and condition tomorrow’s plan—mirroring modular research pipelines where
          idea, literature, method, analysis, paper, and review stay coordinated yet independent.
        </p>
        <div className="mx-auto w-fit rounded-full border border-zinc-200 px-4 py-1 text-xs uppercase tracking-[0.3em] text-zinc-500 dark:border-white/10 dark:text-zinc-400">
          Inspired by modern agentic research labs
        </div>
      </header>

      <div className="flex justify-center">
        <Link
          href="https://github.com/monkey-make-banana/human-diary"
          className="inline-flex items-center gap-2 rounded-full border border-zinc-900/10 bg-zinc-900 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:-translate-y-0.5 hover:bg-zinc-800 dark:border-white/20 dark:bg-white dark:text-zinc-900"
        >
          Check out the source code
          <span aria-hidden="true">→</span>
        </Link>
      </div>

      <Divider soft />

      <section className="rounded-3xl border border-zinc-100 bg-zinc-50/80 p-8 text-left shadow-sm dark:border-white/5 dark:bg-white/5 dark:shadow-none">
        <Subheading level={2} className="text-xl uppercase tracking-[0.4em] text-zinc-500 dark:text-zinc-400">
          Under the hood
        </Subheading>
        <div className="space-y-4 leading-relaxed text-zinc-700 dark:text-zinc-200">
          <p>
            The stack uses <strong>graph-based orchestration</strong> (LangGraph) plus planning-and-control strategies
            (BabyAGI) to decompose work, route state, and iterate via propose–critique cycles. Literature
            novelty checks and citation injection pull from <strong>Semantic Scholar</strong> and{' '}
            <strong>Perplexity Sonar</strong>; OpenAI Web Search, SerpAPI, and NewsAPI.ai add structured signals before
            clustering.
          </p>
          <p>
            Long-context summaries and lightweight LaTeX assembly keep outputs reproducible. A critic/score/selector
            loop—akin to an automated peer-review pass—gates publication quality before release. The overall rhythm
            borrows the end-to-end flow popularized by AI Scientist work (idea generation → experiment iteration → paper
            write-up → automated review) but adapts it for a newsroom that must justify claims, track provenance, and
            refine continuously.
          </p>
        </div>
      </section>

      <Divider soft />

      <section className="space-y-4">
        <Subheading level={2}>References & inspiration</Subheading>
        <ul className="space-y-2 text-sm text-zinc-600 dark:text-zinc-300">
          {references.map((reference) => (
            <li key={reference.key} className="leading-relaxed">
              {/* <span className="font-semibold text-zinc-900 dark:text-white">{reference.key}</span> */}
              {/* <span className="px-2 text-zinc-400">·</span> */}
              <a
                href={reference.url}
                target="_blank"
                rel="noreferrer"
                className="text-zinc-900 underline decoration-zinc-500/50 hover:decoration-zinc-900 dark:text-white dark:decoration-white/50"
              >
                {reference.label}
              </a>
            </li>
          ))}
        </ul>
      </section>
    </article>
  )
}
