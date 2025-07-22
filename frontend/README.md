# Email Guard Frontend

A React-based frontend application for the Email Guard system, built with TypeScript and Vite.

## Features

- Email scanning and analysis dashboard
- User authentication and verification
- Real-time email threat detection
- Modern, responsive UI with Tailwind CSS

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **ESLint** for code quality

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create a `.env.local` file in the frontend directory:
```bash
VITE_API_URL=PUBLIC_URL
```

The `VITE_API_URL` environment variable should point to your backend API endpoint:
- For local development: `http://localhost:5000`
- For production: Your deployed backend URL

### Development

Start the development server:
```bash
npm run dev
```

The application will be available at VITE_API_URL or `http://localhost:5173`

### Building for Production

Build the application:
```bash
npm run build
```

The built files will be in the `dist` directory.

### Linting

Run ESLint to check code quality:
```bash
npm run lint
```

## Project Structure

```
src/
├── App.tsx              # Main application component
├── auth.tsx             # Authentication components
├── scan.tsx             # Email scanning interface
├── email-analysis-dashboard.tsx  # Analysis dashboard
├── main.tsx             # Application entry point
└── assets/              # Static assets
```

## Deployment

This frontend is configured for deployment on Vercel. The `vercel.json` file contains the necessary configuration for the deployment.

For local testing, run the frontend locally while the backend runs in Docker as described in the main project documentation.
