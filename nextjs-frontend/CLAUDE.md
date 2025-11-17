# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

- `npm run dev` - Start development server (http://localhost:3000)
- `npm run build` - Build production application
- `npm start` - Start production server
- `npm run lint` - Run ESLint for code quality checks

## Project Architecture

This is a Next.js 15 frontend application using the App Router architecture with TypeScript and Tailwind CSS.

### Key Structure
- **App Router**: Uses Next.js App Router (`src/app/`) with file-based routing
- **TypeScript Configuration**: Strict mode enabled with `@/*` path aliases pointing to `src/*`
- **Styling**: Tailwind CSS v4 with custom CSS variables for theming and Geist fonts
- **Layout System**: Root layout (`src/app/layout.tsx`) handles global fonts and metadata

### Technology Stack
- Next.js 15.4.3 with React 19.1.0
- TypeScript with strict configuration
- Tailwind CSS v4 with PostCSS
- Geist font family (Sans & Mono)
- ESLint with Next.js configuration

### Styling Approach
- Uses Tailwind CSS with custom CSS variables in `globals.css`
- Light/dark theme support via CSS variables
- Font variables configured in root layout for Geist Sans and Mono

### Current State
This is a fresh Next.js application created with `create-next-app` with the default starter template still in place.