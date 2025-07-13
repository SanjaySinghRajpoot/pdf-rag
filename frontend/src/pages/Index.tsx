import { useState } from 'react';
import { FileText, MessageSquare, Sparkles, CheckCircle } from 'lucide-react';
import { PDFUpload } from '@/components/PDFUpload';
import { QueryInterface } from '@/components/QueryInterface';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';

const Index = () => {
  const [uploadCount, setUploadCount] = useState(0);
  const [uploadedFile, setUploadedFile] = useState<string | null>(null);
  const [activeStep, setActiveStep] = useState<string>("step1");

  const handleUploadSuccess = (fileName?: string) => {
    setUploadCount(prev => prev + 1);
    if (fileName) {
      setUploadedFile(fileName);
    }
    setActiveStep("step2");
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <FileText className="h-8 w-8 text-primary" />
              <h1 className="text-2xl font-bold bg-gradient-primary bg-clip-text text-transparent">
                PDF Query App
              </h1>
            </div>
            <Sparkles className="h-5 w-5 text-primary-glow animate-pulse-glow" />
          </div>
          <p className="text-muted-foreground mt-1">
            Upload PDFs and query their content with AI
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto space-y-8">
          {/* Welcome Section */}
          <div className="text-center space-y-4">
            <h2 className="text-3xl font-bold text-foreground">
              Intelligent Document Query System
            </h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Upload your PDF documents and ask questions about their content. 
              Our AI will analyze the documents and provide accurate answers.
            </p>
          </div>

          {/* Step-by-Step Process */}
          <Accordion 
            type="single" 
            value={activeStep} 
            onValueChange={setActiveStep}
            className="w-full space-y-4"
          >
            {/* Step 1: Upload Document */}
            <AccordionItem value="step1" className="border border-border rounded-lg bg-card">
              <AccordionTrigger className="px-6 py-4 hover:no-underline">
                <div className="flex items-center gap-3">
                  {uploadedFile ? (
                    <CheckCircle className="h-5 w-5 text-success" />
                  ) : (
                    <FileText className="h-5 w-5 text-primary" />
                  )}
                  <div className="text-left">
                    <h3 className="text-xl font-semibold text-foreground">
                      Step 1: Upload Document
                    </h3>
                    {uploadedFile && (
                      <p className="text-sm text-muted-foreground mt-1">
                        Document uploaded: {uploadedFile}
                      </p>
                    )}
                  </div>
                </div>
              </AccordionTrigger>
              <AccordionContent className="px-6 pb-6">
                <div className="space-y-4">
                  <PDFUpload onUploadSuccess={handleUploadSuccess} />
                  
                  {uploadCount > 0 && (
                    <div className="flex items-center gap-2 text-success text-sm">
                      <div className="w-2 h-2 bg-success rounded-full animate-pulse" />
                      {uploadCount} document{uploadCount > 1 ? 's' : ''} uploaded successfully
                    </div>
                  )}
                </div>
              </AccordionContent>
            </AccordionItem>

            {/* Step 2: Query Document */}
            <AccordionItem 
              value="step2" 
              className="border border-border rounded-lg bg-card"
            >
              <AccordionTrigger 
                className="px-6 py-4 hover:no-underline"
                disabled={!uploadedFile}
              >
                <div className="flex items-center gap-3">
                  <MessageSquare 
                    className={`h-5 w-5 ${uploadedFile ? 'text-primary' : 'text-muted-foreground'}`} 
                  />
                  <div className="text-left">
                    <h3 className={`text-xl font-semibold ${uploadedFile ? 'text-foreground' : 'text-muted-foreground'}`}>
                      Step 2: Ask Questions
                    </h3>
                    {!uploadedFile && (
                      <p className="text-sm text-muted-foreground mt-1">
                        Upload a document first to enable queries
                      </p>
                    )}
                  </div>
                </div>
              </AccordionTrigger>
              <AccordionContent className="px-6 pb-6">
                <QueryInterface />
              </AccordionContent>
            </AccordionItem>
          </Accordion>

          {/* Features Info */}
          <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-6 rounded-lg bg-card border border-border">
              <FileText className="h-8 w-8 text-primary mx-auto mb-3" />
              <h4 className="font-semibold text-foreground mb-2">PDF Upload</h4>
              <p className="text-sm text-muted-foreground">
                Securely upload and process PDF documents
              </p>
            </div>
            
            <div className="text-center p-6 rounded-lg bg-card border border-border">
              <MessageSquare className="h-8 w-8 text-primary mx-auto mb-3" />
              <h4 className="font-semibold text-foreground mb-2">Smart Queries</h4>
              <p className="text-sm text-muted-foreground">
                Ask natural language questions about your documents
              </p>
            </div>
            
            <div className="text-center p-6 rounded-lg bg-card border border-border">
              <Sparkles className="h-8 w-8 text-primary mx-auto mb-3" />
              <h4 className="font-semibold text-foreground mb-2">AI Responses</h4>
              <p className="text-sm text-muted-foreground">
                Get accurate, contextual answers instantly
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;
