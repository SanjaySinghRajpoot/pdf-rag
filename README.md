# PDF RAG Application

A full-stack PDF document query system that allows users to upload PDF documents and query their content using AI-powered semantic search. Built with FastAPI backend and React frontend.

## 🚀 Features

- **PDF Upload & Processing**: Securely upload PDF documents for processing
- **Semantic Search**: Query documents using natural language
- **AI-Powered Responses**: Get accurate, contextual answers from your documents
- **Vector Embeddings**: Uses OpenAI embeddings for intelligent document chunking
- **PostgreSQL with pgvector**: Efficient similarity search capabilities
- **Modern UI**: Clean, responsive interface built with React and Tailwind CSS

## 🏗️ Architecture

- **Backend**: FastAPI with Python
- **Frontend**: React with TypeScript and Vite
- **Database**: PostgreSQL with pgvector extension
- **AI/ML**: OpenAI API for embeddings and text generation
- **Styling**: Tailwind CSS with custom design system

## 📋 Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+ with pgvector extension
- OpenAI API key

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd pdf-rag
```

### 2. Backend Setup

#### Navigate to backend directory
```bash
cd backend
```

#### Create Python virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install dependencies
```bash
pip install -r requirements.txt
```

#### Environment configuration
1. Copy the sample environment file:
```bash
cp sample.env .env
```

2. Edit `.env` file with your configuration:
```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/pdf_rag_db

# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# App Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
```

#### Database setup
1. Create PostgreSQL database:
```sql
CREATE DATABASE pdf_rag_db;
```

2. Install pgvector extension:
```sql
CREATE EXTENSION vector;
```

#### Run the backend
```bash
# From backend directory
python main.py
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

#### Navigate to frontend directory
```bash
cd frontend
```

#### Install dependencies
```bash
npm install
# or using bun
bun install
```

#### Environment configuration
Create `.env` file in frontend directory:
```env
VITE_API_BASE_URL=http://localhost:8000
```

#### Run the frontend
```bash
npm run dev
# or using bun
bun dev
```

The frontend will be available at `http://localhost:8080`

## 🐳 Docker Setup (Alternative)

You can also run the application using Docker:

```bash
# Build and run with docker-compose
docker-compose up --build
```

This will start both backend and frontend services with the database.

## 🔧 Development

### Backend Development
- API documentation: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/v1/health`
- Statistics: `http://localhost:8000/api/v1/stats`

### Frontend Development
- Built with Vite for fast hot reloading
- Tailwind CSS for styling
- TypeScript for type safety
- React Query for API state management

### Key Backend Files
- [`backend/app/main.py`](backend/app/main.py) - FastAPI application entry point
- [`backend/app/routes/routes.py`](backend/app/routes/routes.py) - API routes definition
- [`backend/app/controller/controller.py`](backend/app/controller/controller.py) - Business logic controllers
- [`backend/app/services/db_interaction.py`](backend/app/services/db_interaction.py) - Database operations

### Key Frontend Files
- [`frontend/src/App.tsx`](frontend/src/App.tsx) - Main application component
- [`frontend/src/pages/Index.tsx`](frontend/src/pages/Index.tsx) - Main page
- [`frontend/src/components/PDFUpload.tsx`](frontend/src/components/PDFUpload.tsx) - PDF upload component

## 📡 API Endpoints

- `POST /api/v1/ingest` - Upload and process PDF documents
- `POST /api/v1/query` - Query documents with natural language
- `GET /api/v1/health` - Health check endpoint
- `GET /api/v1/stats` - System statistics

## 🎨 UI Components

The frontend uses a custom design system with:
- Responsive layout
- Dark theme optimized
- Custom gradients and animations
- Accessible components built with Radix UI

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 🚀 Production Deployment

1. Set environment variables for production
2. Configure PostgreSQL with proper security settings
3. Set up reverse proxy (nginx recommended)
4. Enable SSL/TLS certificates
5. Configure CORS settings appropriately

## 📝 Environment Variables

### Backend
- `DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` - OpenAI API key for embeddings
- `ENVIRONMENT` - deployment environment (development/production)
- `LOG_LEVEL` - logging level

### Frontend
- `VITE_API_BASE_URL` - Backend API base URL

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.