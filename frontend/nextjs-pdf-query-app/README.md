# Next.js PDF Query Application

This is a simple Next.js application built with TypeScript that allows users to upload PDF files and submit queries. The application interacts with a backend API to handle file uploads and process user queries.

## Features

- Upload PDF files from your local system.
- Submit user queries and receive responses from the backend.
- Built with Next.js and TypeScript for a modern web development experience.

## Getting Started

### Prerequisites

- Node.js (version 14 or later)
- npm (Node Package Manager)

### Installation

1. Clone the repository:

   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:

   ```
   cd nextjs-pdf-query-app
   ```

3. Install the dependencies:

   ```
   npm install
   ```

### Running the Application

To start the development server, run:

```
npm run dev
```

The application will be available at `http://localhost:3000`.

### Usage

1. **Upload a PDF**: Click the upload button to select a PDF file from your local system. The file will be sent to the backend for processing.
2. **Submit a Query**: Enter your query in the provided input field and click the submit button. The response will be displayed on the screen.

### API Endpoints

- **Upload PDF**: `POST /api/upload`
- **Submit Query**: `POST /api/query`

### License

This project is licensed under the MIT License. See the LICENSE file for more details.