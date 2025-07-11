import React, { useState } from 'react';

const PdfUpload: React.FC = () => {
    const [file, setFile] = useState<File | null>(null);
    const [uploadMessage, setUploadMessage] = useState<string>('');

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = event.target.files?.[0];
        if (selectedFile) {
            setFile(selectedFile);
        }
    };

    const handleUpload = async () => {
        if (!file) {
            setUploadMessage('Please select a PDF file to upload.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();
            setUploadMessage(data.message || 'Upload successful!');
        } catch (error) {
            setUploadMessage('Upload failed. Please try again.');
        }
    };

    return (
        <div>
            <input type="file" accept="application/pdf" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload PDF</button>
            {uploadMessage && <p>{uploadMessage}</p>}
        </div>
    );
};

export default PdfUpload;