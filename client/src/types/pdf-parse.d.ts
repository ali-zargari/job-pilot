declare module 'pdf-parse' {
  function pdfParse(buffer: Buffer): Promise<{
    text: string;
    numpages: number;
    info: any;
    metadata: any;
    version: string;
  }>;
  
  export = pdfParse;
} 