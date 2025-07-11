import type { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';

export const config = {
  api: {
    bodyParser: false,
  },
};

const uploadHandler = (req: NextApiRequest, res: NextApiResponse) => {
  if (req.method === 'POST') {
    const filePath = path.join(process.cwd(), 'uploads'); // Ensure this directory exists
    const fileName = `uploaded_${Date.now()}.pdf`;
    const fileStream = fs.createWriteStream(path.join(filePath, fileName));

    req.pipe(fileStream);

    fileStream.on('finish', () => {
      res.status(200).json({ message: 'File uploaded successfully', fileName });
    });

    fileStream.on('error', (error) => {
      res.status(500).json({ message: 'Error uploading file', error });
    });
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
};

export default uploadHandler;