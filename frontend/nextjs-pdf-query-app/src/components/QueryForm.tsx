import React, { useState } from 'react';

const QueryForm: React.FC = () => {
    const [query, setQuery] = useState('');
    const [response, setResponse] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const res = await fetch('/api/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query }),
            });
            const data = await res.json();
            setResponse(data.message || 'No response from server');
        } catch (error) {
            setResponse('Error submitting query');
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Enter your query"
                    required
                />
                <button type="submit">Submit Query</button>
            </form>
            {response && <div className="response">{response}</div>}
        </div>
    );
};

export default QueryForm;