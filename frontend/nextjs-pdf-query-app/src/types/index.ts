export interface UploadResponse {
  success: boolean;
  message: string;
}

export interface QueryRequest {
  query: string;
}

export interface QueryResponse {
  success: boolean;
  response: string;
}