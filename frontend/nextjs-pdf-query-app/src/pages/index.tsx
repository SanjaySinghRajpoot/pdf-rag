import { useState } from 'react';
import PdfUpload from '../components/PdfUpload';
import QueryForm from '../components/QueryForm';

const Home = () => {
  const [response, setResponse] = useState<string | null>(null);

  const handleQueryResponse = (data: string) => {
    setResponse(data);
  };

  return (
    <div>
      <h1>PDF Upload and Query Application</h1>
      <PdfUpload />
      <QueryForm onQueryResponse={handleQueryResponse} />
      {response && <div className="response">{response}</div>}
    </div>
  );
};

export default Home;