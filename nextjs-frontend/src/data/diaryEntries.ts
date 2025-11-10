import diaryEntriesData from './diaryEntries.json'

export type DiaryEntry = {
  date: string
  title: string
  body: string[]
}

const diaryEntries = diaryEntriesData as DiaryEntry[]

export function getDiaryEntries(): DiaryEntry[] {
  return diaryEntries
}

export function getDiaryEntryByDate(date: string): DiaryEntry | undefined {
  return diaryEntries.find((entry) => entry.date === date)
}
