# F1

## Tech Stack
- Frontend: NextJS, Tailwind CSS
- Backend: Python

## Backend - The Model

It uses real-timing data of the seasons 2023, 2024 and 2025 to learn how quickly F1 tyres degrades. It tests this on races that have never happened before.

### Getting Started

```bash
pip install -r backend/requirements.text
python -m backend/fetch_open 2023 2024 2025
python -m backend/eval_deg
```

## Frontend - The Interface

It fetches data from the JSON files and renders them on different pages--drivers, teams, past races, strategy.

Some pages are unfinished as of the moment.

### Getting Started

First, install the project dependencies:

```bash
npm install
# or
yarn install
# or
pnpm install
# or
bun install
```

Second, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.