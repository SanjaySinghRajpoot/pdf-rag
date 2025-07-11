import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    if (req.method === 'POST') {
        const { query } = req.body;

        // Here you would typically process the query, interact with your backend logic,
        // and generate a response based on the query.
        // For demonstration purposes, we'll just echo the query back.

        if (!query) {
            return res.status(400).json({ error: 'Query is required' });
        }

        // Simulate a response based on the query
        const response = `You asked: ${query}`;

        return res.status(200).json({ response });
    } else {
        res.setHeader('Allow', ['POST']);
        return res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}