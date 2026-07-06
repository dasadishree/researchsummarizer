'use client';

import { useRef, useState } from "react";

export default function Home() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const handleUploadClick = () => {
    fileInputRef.current?.click();
  }

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>)=>{
    const file = e.target.files?.[0];
    if (!file) return;
    console.log("Selected file:", file.name);
    const formData = new FormData();
    formData.append("file", file);
    const res = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    setUploadResult(data);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold">ResearchOS</h1>
          <button onClick={handleUploadClick} className="bg-black text-white px-4 py-2 rounded-lg">
            Upload Paper
          </button>


          <input
            type="file"
            accept="application/pdf"
            ref={fileInputRef}
            onChange={handleFileChange}
            className="hidden"
          />
        </div>

        {uploadResult && (
          <div className="mt-4 p-4 bg-green-100 rounded-lg">
            <p><b>Status:</b> {uploadResult.status}</p>
            <p><b>Paper ID:</b> {uploadResult.paper_id}</p>
            <p><b>Pages:</b> {uploadResult.metadata.page_count}</p>
            <p><b>Words:</b> {uploadResult.metadata.word_count}</p>
          </div>
        )}
          <input
            type="file"
            accept="application/pdf"
            ref={fileInputRef}
            onChange={handleFileChange}
            className="hidden"
          />
        </div>

        <div className="grid grid-cols-3 gap-4">
          
          <div className="col-span-1 bg-white p-4 rounded-xl shadow">
            <h2 className="font-semibold mb-2">Your Papers</h2>
            <p className="text-gray-500 text-sm">
              No papers uploaded yet
            </p>
          </div>

          <div className="col-span-2 bg-white p-4 rounded-xl shadow">
            <h2 className="font-semibold mb-2">Knowledge Graph</h2>
            <div className="h-64 flex items-center justify-center text-gray-400">
              Graph will appear here
            </div>
      
      </div>      

      <div className="mt-4 bg-white p-4 rounded-xl shadow">
        <h2 className="font-semibold mb-2">AI Research Assistant</h2>
        <p className="text-gray-500 text-sm">
          Ask questions about your papers
        </p>
      </div>


    </div>
  </div>
  );
}